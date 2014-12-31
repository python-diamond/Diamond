#!/usr/bin/env python
# coding=utf-8
###############################################################################

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

try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'src', 'collectors')))


def run_only(func, predicate):
    if predicate():
        return func
    else:
        def f(arg):
            pass
        return f


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

        filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'docs', 'collectors-' + collector + '.md')

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

                        metricPath = 'servers.hostname.'

                        if defaultpath:
                            metricPath += defaultpath + '.'

                        metricPath += metric

                        metricPath = metricPath.replace('..', '.')
                        fp.write('%s %s\n' % (metricPath, metrics[metric]))
                else:
                    fp.write(line)
            fp.close()

        except IOError:
            return False
        return True

    def getFixtureDirPath(self):
        path = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            'fixtures')
        return path

    def getFixturePath(self, fixture_name):
        path = os.path.join(self.getFixtureDirPath(),
                            fixture_name)
        if not os.access(path, os.R_OK):
            print "Missing Fixture " + path
        return path

    def getFixture(self, fixture_name):
        try:
            f = open(self.getFixturePath(fixture_name), 'r')
            data = StringIO(f.read())
            return data
        finally:
            f.close()

    def getFixtures(self):
        fixtures = []
        for root, dirnames, filenames in os.walk(self.getFixtureDirPath()):
            fixtures.append(os.path.join(root, dirnames, filenames))
        return fixtures

    def getPickledResults(self, results_name):
        try:
            f = open(self.getFixturePath(results_name), 'r')
            data = pickle.load(f)
            return data
        finally:
            f.close()

    def setPickledResults(self, results_name, data):
        pickle.dump(data, open(self.getFixturePath(results_name), "w+b"))

    def assertUnpublished(self, mock, key, value, expected_value=0):
        return self.assertPublished(mock, key, value, expected_value)

    def assertPublished(self, mock, key, value, expected_value=1):
        if type(mock) is list:
            for m in mock:
                calls = (filter(lambda x: x[0][0] == key, m.call_args_list))
                if len(calls) > 0:
                    break
        else:
            calls = filter(lambda x: x[0][0] == key, mock.call_args_list)

        actual_value = len(calls)
        message = '%s: actual number of calls %d, expected %d' % (
            key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        if expected_value:
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

    def assertUnpublishedMany(self, mock, dict, expected_value=0):
        return self.assertPublishedMany(mock, dict, expected_value)

    def assertPublishedMany(self, mock, dict, expected_value=1):
        for key, value in dict.iteritems():
            self.assertPublished(mock, key, value, expected_value)

        if type(mock) is list:
            for m in mock:
                m.reset_mock()
        else:
            mock.reset_mock()

    def assertUnpublishedMetric(self, mock, key, value, expected_value=0):
        return self.assertPublishedMetric(mock, key, value, expected_value)

    def assertPublishedMetric(self, mock, key, value, expected_value=1):
        calls = filter(lambda x: x[0][0].path.find(key) != -1,
                       mock.call_args_list)

        actual_value = len(calls)
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

    def assertUnpublishedMetricMany(self, mock, dict, expected_value=0):
        return self.assertPublishedMetricMany(mock, dict, expected_value)

    def assertPublishedMetricMany(self, mock, dict, expected_value=1):
        for key, value in dict.iteritems():
            self.assertPublishedMetric(mock, key, value, expected_value)

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

###############################################################################

if __name__ == "__main__":
    if setproctitle:
        setproctitle('test.py')

    # Disable log output for the unit tests
    log = logging.getLogger("diamond")
    log.addHandler(logging.StreamHandler(sys.stderr))
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

    dPath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'src',
                                         'diamond'))

    getCollectorTests(cPath)
    getCollectorTests(dPath)

    loader = unittest.TestLoader()
    tests = []
    for test in collectorTests:
        for name, c in inspect.getmembers(collectorTests[test],
                                          inspect.isclass):
            if not issubclass(c, unittest.TestCase):
                continue
            tests.append(loader.loadTestsFromTestCase(c))
    suite = unittest.TestSuite(tests)
    results = unittest.TextTestRunner(verbosity=options.verbose).run(suite)

    results = str(results)
    results = results.replace('>', '').split()[1:]
    resobj = {}
    for result in results:
        result = result.split('=')
        resobj[result[0]] = int(result[1])

    if resobj['failures'] > 0:
        sys.exit(1)
    if resobj['errors'] > 0:
        sys.exit(2)

    sys.exit(0)
