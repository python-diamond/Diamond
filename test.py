#!/usr/bin/env python
################################################################################

import os
import sys
import unittest
import inspect
import traceback
import optparse
import logging
import configobj

try:
    import cPickle as pickle
except ImportError:
    import pickle as pickle

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'src', 'collectors')))

from diamond.collector import Collector


def get_collector_config(key, value):
    config = configobj.ConfigObj()
    config['server'] = {}
    config['server']['collectors_config_path'] = ''
    config['collectors'] = {}
    config['collectors']['default'] = {}
    config['collectors']['default']['hostname_method'] = "uname_short"
    config['collectors'][key] = value
    return config


class CollectorTestCase(unittest.TestCase):

    def setDocExample(self, collector, metrics, defaultpath=None):
        if not len(metrics):
            return False

        filePath = os.path.join('docs', 'collectors-' + collector + '.md')

        if not os.path.exists(filePath):
            return False

        if not os.access(filePath, os.W_OK):
            return False

        if not os.access(filePath, os.R_OK):
            return False

        try:
            fp = open(filePath, 'Ur')
            content = fp.readlines()
            fp.close()

            fp = open(filePath, 'w')
            for line in content:
                if line.strip() == '__EXAMPLESHERE__':
                    for metric in sorted(metrics.iterkeys()):
                        
                        metricPath  = 'servers.hostname.'
                        
                        if defaultpath :
                            metricPath += defaultpath + '.'
                        
                        metricPath += metric
                        
                        metricPath = metricPath.replace('..', '.')
                        fp.write(metricPath + ' ' + str(metrics[metric]) + '\n')
                else:
                    fp.write(line)
            fp.close()

        except IOError:
            return False
        return True

    def getFixturePath(self, fixture_name):
        file = os.path.join(os.path.dirname(inspect.getfile(self.__class__)),
                            'fixtures',
                            fixture_name)
        if not os.access(file, os.R_OK):
            print "Missing Fixture " + file
        return file

    def getFixture(self, fixture_name):
        file = open(self.getFixturePath(fixture_name), 'r')
        data = StringIO(file.read())
        file.close()
        return data

    def getPickledResults(self, results_name):
        file = open(self.getFixturePath(results_name), 'r')
        data = pickle.load(file)
        file.close()
        return data

    def setPickledResults(self, results_name, data):
        pickle.dump(data, open(self.getFixturePath(results_name), "wb"))

    def assertPublished(self, mock, key, value):
        calls = filter(lambda x: x[0][0] == key, mock.call_args_list)

        actual_value = len(calls)
        expected_value = 1
        message = '%s: actual number of calls %d, expected %d' % (
            key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        actual_value = calls[0][0][1]
        expected_value = value
        precision = 0

        if isinstance(value, tuple):
            expected_value, precision = expected_value

        message = '%s: actual %r, expected %r' % (key,
                                                  actual_value,
                                                  expected_value)
        #print message

        if precision is not None:
            self.assertAlmostEqual(float(actual_value),
                                   float(expected_value),
                                   places=precision,
                                   msg=message)
        else:
            self.assertEqual(actual_value, expected_value, message)

    def assertPublishedMany(self, mock, dict):
        for key, value in dict.iteritems():
            self.assertPublished(mock, key, value)

        mock.reset_mock()

    def assertPublishedMetric(self, mock, key, value):
        calls = filter(lambda x: x[0][0].path.find(key) != -1,
                       mock.call_args_list)

        actual_value = len(calls)
        expected_value = 1
        message = '%s: actual number of calls %d, expected %d' % (
            key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        actual_value = calls[0][0][0].value
        expected_value = value
        precision = 0

        if isinstance(value, tuple):
            expected_value, precision = expected_value

        message = '%s: actual %r, expected %r' % (key,
                                                  actual_value,
                                                  expected_value)
        #print message

        if precision is not None:
            self.assertAlmostEqual(float(actual_value),
                                   float(expected_value),
                                   places=precision,
                                   msg=message)
        else:
            self.assertEqual(actual_value, expected_value, message)

    def assertPublishedMetricMany(self, mock, dict):
        for key, value in dict.iteritems():
            self.assertPublishedMetric(mock, key, value)

        mock.reset_mock()

collectorTests = {}


def getCollectorTests(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if (os.path.isfile(cPath)
                and len(f) > 3
                and f[-3:] == '.py'
                and f[0:4] == 'test'):
            sys.path.append(os.path.dirname(cPath))
            sys.path.append(os.path.dirname(os.path.dirname(cPath)))
            modname = f[:-3]
            try:
                # Import the module
                collectorTests[modname] = __import__(modname,
                                                     globals(),
                                                     locals(),
                                                     ['*'])
                #print "Imported module: %s" % (modname)
            except Exception:
                print "Failed to import module: %s. %s" % (
                    modname, traceback.format_exc())
                continue

    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getCollectorTests(cPath)


class BaseCollectorTest(unittest.TestCase):

    def test_SetCustomHostname(self):
        config = configobj.ConfigObj()
        config['server'] = {}
        config['server']['collectors_config_path'] = ''
        config['collectors'] = {}
        config['collectors']['default'] = {
            'hostname': 'custom.localhost',
        }
        c = Collector(config, [])
        self.assertEquals('custom.localhost', c.get_hostname())

################################################################################

if __name__ == "__main__":

    # Disable log output for the unit tests
    log = logging.getLogger("diamond")
    log.disabled = True

    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c",
                      "--collector",
                      dest="collector",
                      default="",
                      help="Run a single collector's unit tests")
    parser.add_option("-v",
                      "--verbose",
                      dest="verbose",
                      default=1,
                      action="count",
                      help="verbose")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    cPath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'src',
                                         'collectors',
                                         options.collector))
    getCollectorTests(cPath)

    tests = []
    for test in collectorTests:
        for attr in dir(collectorTests[test]):
            if not attr.startswith('Test') or not attr.endswith('Collector'):
                continue
            c = getattr(collectorTests[test], attr)
            tests.append(unittest.TestLoader().loadTestsFromTestCase(c))
    tests.append(unittest.TestLoader().loadTestsFromTestCase(BaseCollectorTest))
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=options.verbose).run(suite)
