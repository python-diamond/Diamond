# coding=utf-8

"""
Send metrics to [Google Pub/Sub](https://cloud.google.com/pubsub/).

#### Copyright

Copyright 2016 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: dcochran@google.com

#### Dependencies

 * [ApiClient](https://github.com/google/google-api-python-client/).
 * [Oauth2Client](https://github.com/google/oauth2client/).

 In addition if you are not running this on a host in your GCE project you will need to have the
 GOOGLE_APPLICATION_CREDENTIALS environment variable pointing to a credentials file for the user
 you are running diamond as.

#### Configuration

Add `diamond.handler.pubsub.PubsubHandler` to your handlers.
It has these options:

 * `topic` - The Pub/Sub topic to publish to.
 * `scopes` - Comma separated list of Pub/Sub scopes to use.
 * `retries` - Number of retries for failed publish attempts.
 * `batch` - Whether to batch msgs or not.  Values:
                - None
                - count (batch by count of msgs...i.e 7 to batch in 7 msgs increments.
                - size (batch by total size of batch in bytes...i.e 64000 to send in 64K increments.
 * `batch_size` - If msgs are to be batched this will contain either the count number or size in bytes.

"""

from Handler import Handler
import logging
import base64
import json
try:
    from apiclient import discovery
    from oauth2client.client import GoogleCredentials
except ImportError:
    discovery = None
    GoogleCredentials = None


class PubsubHandler(Handler):

    def __init__(self, config=None):
        # Initialize Handler
        Handler.__init__(self, config)

        if discovery is None:
            logging.error("Failed to load apiclient.discovery")
            return
        elif GoogleCredentials is None:
            logging.error("Failed to load oauth2client.client.GoogleCredentials")
            return

        # Initialize options
        self.topic = self.config['topic']
        self.scopes = self.config['scopes'].split(',')
        self.retries = int(self.config['retries'])
        self.batch = self.config['batch']
        self.batch_size = int(self.config['batch_size'])
        self.metrics = []

        # Initialize client
        credentials = GoogleCredentials.get_application_default()
        if credentials.create_scoped_required():
            credentials = credentials.create_scoped(self.scopes)
        self.client = discovery.build('pubsub', 'v1', credentials=credentials)

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(PubsubHandler, self).get_default_config_help()

        config.update({
            'topic': 'Pub/Sub Topic',
            'scopes': 'Pub/Sub Scopes',
            'retries': 'Number of retries to publish a metric',
            'batch': 'Should msgs be batched.  Values: None, count, or size',
            'batch_size': 'If batch msgs, will contain the count number or size in bytes',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(PubsubHandler, self).get_default_config()

        config.update({
            'topic': 'projects/my-project/topics/default-topic',
            'scopes': 'https://www.googleapis.com/auth/pubsub',
            'retries': 3,
            'batch': None,
            'batch_size': 0,
        })

        return config

    def process(self, metric):
        """
        Process a metric by sending it to pub/sub
        :param metric: metric to process
        """
        if self.batch is None:
            self.metrics.append(self._convert_to_pubsub(metric))
            self._send()
        else:
            if self.batch == 'count':
                # batch up by number of msgs
                self.metrics.append(self._convert_to_pubsub(metric))
                if len(self.metrics) >= self.batch_size:
                    self._send()
            else:
                # batch up by size of msgs
                tmp_msg = self._convert_to_pubsub(metric)
                avg_size = len(json.dumps(self.metrics)) / (len(self.metrics) + 1)

                # TODO: see if there is a better way than json.dumps to get byte size.
                next_bytecount = len(tmp_msg) + len(json.dumps(self.metrics))
                logging.debug("Next dataframe size: %s | Avg size: %s" % (next_bytecount, avg_size))
                # add additional avg message size to cover msg envelope overhead
                if next_bytecount >= ((self.batch_size - len(tmp_msg)) - avg_size):
                    self._send()

                self.metrics.append(tmp_msg)


    def _convert_to_pubsub(self, metric):
        """
        Convert a metric to a dictionary representing a Pub/Sub event.
        Each metric should be loaded into a separate data slot
        """
        # Using separate "host" field, so remove from the path.  This was taken from the Riemann Handler.
        path = '%s.%s.%s' % (
            metric.getPathPrefix(),
            metric.getCollectorPath(),
            metric.getMetricPath()
        )

        payload = {
            'host': metric.host,
            'service': path,
            'time': metric.timestamp,
            'metric': float(metric.value),
            'ttl': metric.ttl,
            }
        data = base64.b64encode(json.dumps(payload))

        return {'data': data}

    def _send(self):
        """
        Send data to pub/sub.
        """
        body = {'messages': self.metrics}
        logging.debug("Number of messages being sent: %s", len(self.metrics))
        logging.debug("Size of message batch being sent: %s", len(json.dumps(body)))
        try:
            resp = self.client.projects().topics().publish(
                topic=self.topic, body=body).execute(num_retries=self.retries)
            logging.debug("Acknowledgements: %s", resp)
            del self.metrics[:]
        except Exception, e:
            logging.error("Error sending event to Pub/Sub: %s", e)

    def _close(self):
        """
        Nothing to do since Pub/Sub publishes to a Rest API
        """
        self.client = None

    def __del__(self):
        self._close()
