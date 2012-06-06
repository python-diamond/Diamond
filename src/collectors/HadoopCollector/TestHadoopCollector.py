#!/usr/bin/python
################################################################################

from test import *

from diamond.collector import Collector
from HadoopCollector import HadoopCollector

import os

################################################################################

class TestHadoopCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('HadoopCollector', {
            'metrics':  [os.path.dirname(__file__)+'/fixtures/*metrics.log'],
        })

        self.collector = HadoopCollector(config, {})

    @patch.object(Collector, 'publish_metric')
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.collect()

        self.assertPublishedMetricMany(publish_mock, {
            'dfs.datanode.blockReports_avg_time' : 0.0,
            'dfs.datanode.blockReports_num_ops' : 1.0,
            'dfs.datanode.block_verification_failures' : 0.0,
            'dfs.datanode.blocks_read' : 0.0,
            'dfs.datanode.blocks_removed' : 0.0,
            'dfs.datanode.blocks_replicated' : 0.0,
            'dfs.datanode.blocks_verified' : 0.0,
            'dfs.datanode.blocks_written' : 44.0,
            'dfs.datanode.bytes_written' : 64223.0,
            'dfs.datanode.copyBlockOp_avg_time' : 0.0,
            'dfs.datanode.copyBlockOp_num_ops' : 0.0,
            'dfs.datanode.heartBeats_avg_time' : 1.0,
            'dfs.datanode.heartBeats_num_ops' : 7.0,
            'dfs.datanode.readBlockOp_avg_time' : 0.0,
            'dfs.datanode.readBlockOp_num_ops' : 0.0,
            'dfs.datanode.readMetadataOp_avg_time' : 0.0,
            'dfs.datanode.readMetadataOp_num_ops' : 0.0,
            'dfs.datanode.reads_from_local_client' : 0.0,
            'dfs.datanode.reads_from_remote_client' : 0.0,
            'dfs.datanode.replaceBlockOp_avg_time' : 0.0,
            'dfs.datanode.replaceBlockOp_num_ops' : 0.0,
            'dfs.datanode.writeBlockOp_avg_time' : 5.0,
            'dfs.datanode.writeBlockOp_num_ops' : 44.0,
            'dfs.datanode.writes_from_local_client' : 44.0,
            'dfs.datanode.writes_from_remote_client' : 0.0,
            'jvm.metrics.gcCount' : 15.0,
            'jvm.metrics.gcTimeMillis' : 58.0,
            'jvm.metrics.logError' : 0.0,
            'jvm.metrics.logFatal' : 0.0,
            'jvm.metrics.logInfo' : 159.0,
            'jvm.metrics.logWarn' : 0.0,
            'jvm.metrics.memHeapCommittedM' : 7.4375,
            'jvm.metrics.memHeapUsedM' : 5.5513763,
            'jvm.metrics.memNonHeapCommittedM' : 23.1875,
            'jvm.metrics.memNonHeapUsedM' : 16.977356,
            'jvm.metrics.threadsBlocked' : 0.0,
            'jvm.metrics.threadsNew' : 0.0,
            'jvm.metrics.threadsRunnable' : 7.0,
            'jvm.metrics.threadsTerminated' : 0.0,
            'jvm.metrics.threadsTimedWaiting' : 8.0,
            'jvm.metrics.threadsWaiting' : 6.0,
            'mapred.shuffleInput.shuffle_failed_fetches' : 0.0,
            'mapred.shuffleInput.shuffle_fetchers_busy_percent' : 0.0,
            'mapred.shuffleInput.shuffle_input_bytes' : 190.0,
            'mapred.shuffleInput.shuffle_success_fetches' : 5.0,
            'rpc.metrics.port' : 50905.0,
            'rpc.metrics.RpcProcessingTime_avg_time' : 0.0,
            'rpc.metrics.RpcProcessingTime_num_ops' : 0.0,
            'rpc.metrics.RpcQueueTime_avg_time' : 0.0,
            'rpc.metrics.RpcQueueTime_num_ops' : 0.0
        })

################################################################################
if __name__ == "__main__":
    unittest.main()
