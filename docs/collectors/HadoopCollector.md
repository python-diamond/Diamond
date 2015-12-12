<!--This file was generated from the python source
Please edit the source to make changes
-->
HadoopCollector
=====

Diamond collector for Hadoop metrics, see:

 * [http://www.cloudera.com/blog/2009/03/hadoop-metrics/](http://bit.ly/NKBcFm)

#### Dependencies

 * hadoop


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics | /var/log/hadoop/*-metrics.out, | List of paths to process metrics from | list
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
truncate | False | Truncate the metrics files after reading them. | bool

#### Example Output

```
servers.hostname.hadoop.dfs.FSNamesystem.BlocksTotal 44.0
servers.hostname.hadoop.dfs.FSNamesystem.CapacityRemainingGB 78.0
servers.hostname.hadoop.dfs.FSNamesystem.CapacityTotalGB 201.0
servers.hostname.hadoop.dfs.FSNamesystem.CapacityUsedGB 0.0
servers.hostname.hadoop.dfs.FSNamesystem.FilesTotal 60.0
servers.hostname.hadoop.dfs.FSNamesystem.PendingReplicationBlocks 0.0
servers.hostname.hadoop.dfs.FSNamesystem.ScheduledReplicationBlocks 0.0
servers.hostname.hadoop.dfs.FSNamesystem.TotalLoad 1.0
servers.hostname.hadoop.dfs.FSNamesystem.UnderReplicatedBlocks 44.0
servers.hostname.hadoop.dfs.datanode.blockReports_avg_time 0.0
servers.hostname.hadoop.dfs.datanode.blockReports_num_ops 1.0
servers.hostname.hadoop.dfs.datanode.block_verification_failures 0.0
servers.hostname.hadoop.dfs.datanode.blocks_read 0.0
servers.hostname.hadoop.dfs.datanode.blocks_removed 0.0
servers.hostname.hadoop.dfs.datanode.blocks_replicated 0.0
servers.hostname.hadoop.dfs.datanode.blocks_verified 0.0
servers.hostname.hadoop.dfs.datanode.blocks_written 44.0
servers.hostname.hadoop.dfs.datanode.bytes_written 64223.0
servers.hostname.hadoop.dfs.datanode.copyBlockOp_avg_time 0.0
servers.hostname.hadoop.dfs.datanode.copyBlockOp_num_ops 0.0
servers.hostname.hadoop.dfs.datanode.heartBeats_avg_time 1.0
servers.hostname.hadoop.dfs.datanode.heartBeats_num_ops 7.0
servers.hostname.hadoop.dfs.datanode.readBlockOp_avg_time 0.0
servers.hostname.hadoop.dfs.datanode.readBlockOp_num_ops 0.0
servers.hostname.hadoop.dfs.datanode.readMetadataOp_avg_time 0.0
servers.hostname.hadoop.dfs.datanode.readMetadataOp_num_ops 0.0
servers.hostname.hadoop.dfs.datanode.reads_from_local_client 0.0
servers.hostname.hadoop.dfs.datanode.reads_from_remote_client 0.0
servers.hostname.hadoop.dfs.datanode.replaceBlockOp_avg_time 0.0
servers.hostname.hadoop.dfs.datanode.replaceBlockOp_num_ops 0.0
servers.hostname.hadoop.dfs.datanode.writeBlockOp_avg_time 5.0
servers.hostname.hadoop.dfs.datanode.writeBlockOp_num_ops 44.0
servers.hostname.hadoop.dfs.datanode.writes_from_local_client 44.0
servers.hostname.hadoop.dfs.datanode.writes_from_remote_client 0.0
servers.hostname.hadoop.dfs.namenode.AddBlockOps 44.0
servers.hostname.hadoop.dfs.namenode.CreateFileOps 44.0
servers.hostname.hadoop.dfs.namenode.DeleteFileOps 0.0
servers.hostname.hadoop.dfs.namenode.FilesCreated 59.0
servers.hostname.hadoop.dfs.namenode.FilesRenamed 0.0
servers.hostname.hadoop.dfs.namenode.GetBlockLocations 0.0
servers.hostname.hadoop.dfs.namenode.GetListingOps 1.0
servers.hostname.hadoop.dfs.namenode.SafemodeTime 102.0
servers.hostname.hadoop.dfs.namenode.Syncs_avg_time 0.0
servers.hostname.hadoop.dfs.namenode.Syncs_num_ops 100.0
servers.hostname.hadoop.dfs.namenode.Transactions_avg_time 0.0
servers.hostname.hadoop.dfs.namenode.Transactions_num_ops 148.0
servers.hostname.hadoop.dfs.namenode.blockReport_avg_time 0.0
servers.hostname.hadoop.dfs.namenode.blockReport_num_ops 1.0
servers.hostname.hadoop.dfs.namenode.fsImageLoadTime 98.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.gcCount 15.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.gcTimeMillis 58.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.logError 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.logFatal 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.logInfo 159.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.logWarn 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.memHeapCommittedM 7.4375
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.memHeapUsedM 5.551376
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.memNonHeapCommittedM 23.1875
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.memNonHeapUsedM 16.977356
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsBlocked 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsNew 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsRunnable 7.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsTerminated 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsTimedWaiting 8.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.DataNode.threadsWaiting 6.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.gcCount 13.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.gcTimeMillis 54.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.logError 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.logFatal 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.logInfo 27.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.logWarn 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.memHeapCommittedM 7.4375
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.memHeapUsedM 4.306557
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.memNonHeapCommittedM 23.1875
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.memNonHeapUsedM 17.360031
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsBlocked 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsNew 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsRunnable 6.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsTerminated 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsTimedWaiting 8.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.JobTracker.threadsWaiting 16.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.gcCount 16.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.gcTimeMillis 56.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.logError 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.logFatal 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.logInfo 133.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.logWarn 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.memHeapCommittedM 7.4375
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.memHeapUsedM 5.778725
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.memNonHeapCommittedM 23.1875
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.memNonHeapUsedM 17.679695
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsBlocked 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsNew 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsRunnable 6.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsTerminated 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsTimedWaiting 10.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.NameNode.threadsWaiting 14.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.gcCount 11.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.gcTimeMillis 53.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.logError 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.logFatal 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.logInfo 12.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.logWarn 3.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.memHeapCommittedM 7.4375
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.memHeapUsedM 4.345642
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.memNonHeapCommittedM 23.1875
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.memNonHeapUsedM 16.32586
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsBlocked 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsNew 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsRunnable 5.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsTerminated 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsTimedWaiting 4.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.SecondaryNameNode.threadsWaiting 2.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.gcCount 11.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.gcTimeMillis 37.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.logError 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.logFatal 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.logInfo 18.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.logWarn 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.memHeapCommittedM 7.4375
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.memHeapUsedM 3.176979
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.memNonHeapCommittedM 23.1875
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.memNonHeapUsedM 13.792732
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsBlocked 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsNew 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsRunnable 5.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsTerminated 0.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsTimedWaiting 5.0
servers.hostname.hadoop.jvm.metrics.doorstop_local.TaskTracker.threadsWaiting 7.0
servers.hostname.hadoop.mapred.job.doorstop_local.File_Systems.HDFS_bytes_read.value 1180.0
servers.hostname.hadoop.mapred.job.doorstop_local.File_Systems.Local_bytes_written.value 860.0
servers.hostname.hadoop.mapred.job.doorstop_local.Job_Counters.Data-local_map_tasks.value 10.0
servers.hostname.hadoop.mapred.job.doorstop_local.Job_Counters.Launched_map_tasks.value 10.0
servers.hostname.hadoop.mapred.job.doorstop_local.Job_Counters.Launched_reduce_tasks.value 1.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Combine_input_records.value 0.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Combine_output_records.value 0.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Map_input_bytes.value 240.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Map_input_records.value 10.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Map_output_bytes.value 320.0
servers.hostname.hadoop.mapred.job.doorstop_local.Map-Reduce_Framework.Map_output_records.value 20.0
servers.hostname.hadoop.mapred.jobtracker.jobs_completed 0.0
servers.hostname.hadoop.mapred.jobtracker.jobs_submitted 1.0
servers.hostname.hadoop.mapred.jobtracker.maps_completed 10.0
servers.hostname.hadoop.mapred.jobtracker.maps_launched 10.0
servers.hostname.hadoop.mapred.jobtracker.reduces_completed 0.0
servers.hostname.hadoop.mapred.jobtracker.reduces_launched 1.0
servers.hostname.hadoop.mapred.shuffleInput.shuffle_failed_fetches 0.0
servers.hostname.hadoop.mapred.shuffleInput.shuffle_fetchers_busy_percent 0.0
servers.hostname.hadoop.mapred.shuffleInput.shuffle_input_bytes 190.0
servers.hostname.hadoop.mapred.shuffleInput.shuffle_success_fetches 5.0
servers.hostname.hadoop.mapred.shuffleOutput.shuffle_failed_outputs 0.0
servers.hostname.hadoop.mapred.shuffleOutput.shuffle_handler_busy_percent 0.0
servers.hostname.hadoop.mapred.shuffleOutput.shuffle_output_bytes 342.0
servers.hostname.hadoop.mapred.shuffleOutput.shuffle_success_outputs 9.0
servers.hostname.hadoop.mapred.tasktracker.mapTaskSlots 2.0
servers.hostname.hadoop.mapred.tasktracker.maps_running 0.0
servers.hostname.hadoop.mapred.tasktracker.reduceTaskSlots 2.0
servers.hostname.hadoop.mapred.tasktracker.reduces_running 1.0
servers.hostname.hadoop.mapred.tasktracker.tasks_completed 10.0
servers.hostname.hadoop.mapred.tasktracker.tasks_failed_ping 0.0
servers.hostname.hadoop.mapred.tasktracker.tasks_failed_timeout 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50020.RpcProcessingTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50020.RpcProcessingTime_num_ops 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50020.RpcQueueTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50020.RpcQueueTime_num_ops 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.RpcProcessingTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.RpcProcessingTime_num_ops 21.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.RpcQueueTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.RpcQueueTime_num_ops 21.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.getBuildVersion_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.getBuildVersion_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.getProtocolVersion_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.getProtocolVersion_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.heartbeat_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50030.heartbeat_num_ops 19.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50905.RpcProcessingTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50905.RpcProcessingTime_num_ops 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50905.RpcQueueTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.50905.RpcQueueTime_num_ops 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.RpcProcessingTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.RpcProcessingTime_num_ops 28.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.RpcQueueTime_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.RpcQueueTime_num_ops 28.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.blockReport_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.blockReport_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.delete_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.delete_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.getProtocolVersion_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.getProtocolVersion_num_ops 4.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.mkdirs_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.mkdirs_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.register_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.register_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.sendHeartbeat_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.sendHeartbeat_num_ops 18.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.setPermission_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.setPermission_num_ops 1.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.versionRequest_avg_time 0.0
servers.hostname.hadoop.rpc.metrics.doorstop_local.8020.versionRequest_num_ops 1.0
```

