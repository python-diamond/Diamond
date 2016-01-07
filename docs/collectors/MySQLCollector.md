<!--This file was generated from the python source
Please edit the source to make changes
-->
MySQLCollector
=====


#### Grants

 * Normal usage
```
GRANT REPLICATION CLIENT on *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

 * For innodb engine status
```
GRANT SUPER ON *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

 * For innodb engine status on MySQL versions 5.1.24+
```
GRANT PROCESS ON *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

#### Dependencies

 * MySQLdb


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
hosts | , | List of hosts to collect from. Format is yourusername:yourpassword@host:port/db[/nickname]use db "None" to avoid connecting to a particular db | list
innodb | False | Collect SHOW ENGINE INNODB STATUS | bool
master | False | Collect SHOW MASTER STATUS | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
publish |  | Which rows of '[SHOW GLOBAL STATUS](http://dev.mysql.com/doc/refman/5.1/en/show-status.html)' you would like to publish. Leave unset to publish all | 
slave | False | Collect SHOW SLAVE STATUS | bool

#### Example Output

```
servers.hostname.mysql.Aborted_clients 1.0
servers.hostname.mysql.Aborted_connects 2.0
servers.hostname.mysql.Binlog_cache_disk_use 3.0
servers.hostname.mysql.Binlog_cache_use 4.0
servers.hostname.mysql.Bytes_received 5.0
servers.hostname.mysql.Bytes_sent 6.0
servers.hostname.mysql.Com_admin_commands 7.0
servers.hostname.mysql.Com_alter_db 9.0
servers.hostname.mysql.Com_alter_db_upgrade 10.0
servers.hostname.mysql.Com_alter_event 11.0
servers.hostname.mysql.Com_alter_function 12.0
servers.hostname.mysql.Com_alter_procedure 13.0
servers.hostname.mysql.Com_alter_server 14.0
servers.hostname.mysql.Com_alter_table 15.0
servers.hostname.mysql.Com_alter_tablespace 16.0
servers.hostname.mysql.Com_analyze 17.0
servers.hostname.mysql.Com_assign_to_keycache 8.0
servers.hostname.mysql.Com_backup_table 18.0
servers.hostname.mysql.Com_begin 19.0
servers.hostname.mysql.Com_binlog 20.0
servers.hostname.mysql.Com_call_procedure 21.0
servers.hostname.mysql.Com_change_db 22.0
servers.hostname.mysql.Com_change_master 23.0
servers.hostname.mysql.Com_check 24.0
servers.hostname.mysql.Com_checksum 25.0
servers.hostname.mysql.Com_commit 26.0
servers.hostname.mysql.Com_create_db 27.0
servers.hostname.mysql.Com_create_event 28.0
servers.hostname.mysql.Com_create_function 29.0
servers.hostname.mysql.Com_create_index 30.0
servers.hostname.mysql.Com_create_procedure 31.0
servers.hostname.mysql.Com_create_server 32.0
servers.hostname.mysql.Com_create_table 33.0
servers.hostname.mysql.Com_create_trigger 34.0
servers.hostname.mysql.Com_create_udf 35.0
servers.hostname.mysql.Com_create_user 36.0
servers.hostname.mysql.Com_create_view 37.0
servers.hostname.mysql.Com_dealloc_sql 38.0
servers.hostname.mysql.Com_delete 39.0
servers.hostname.mysql.Com_delete_multi 40.0
servers.hostname.mysql.Com_do 41.0
servers.hostname.mysql.Com_drop_db 42.0
servers.hostname.mysql.Com_drop_event 43.0
servers.hostname.mysql.Com_drop_function 44.0
servers.hostname.mysql.Com_drop_index 45.0
servers.hostname.mysql.Com_drop_procedure 46.0
servers.hostname.mysql.Com_drop_server 47.0
servers.hostname.mysql.Com_drop_table 48.0
servers.hostname.mysql.Com_drop_trigger 49.0
servers.hostname.mysql.Com_drop_user 50.0
servers.hostname.mysql.Com_drop_view 51.0
servers.hostname.mysql.Com_empty_query 52.0
servers.hostname.mysql.Com_execute_sql 53.0
servers.hostname.mysql.Com_flush 54.0
servers.hostname.mysql.Com_grant 55.0
servers.hostname.mysql.Com_ha_close 56.0
servers.hostname.mysql.Com_ha_open 57.0
servers.hostname.mysql.Com_ha_read 58.0
servers.hostname.mysql.Com_help 59.0
servers.hostname.mysql.Com_insert 60.0
servers.hostname.mysql.Com_insert_select 61.0
servers.hostname.mysql.Com_install_plugin 62.0
servers.hostname.mysql.Com_kill 63.0
servers.hostname.mysql.Com_load 64.0
servers.hostname.mysql.Com_load_master_data 65.0
servers.hostname.mysql.Com_load_master_table 66.0
servers.hostname.mysql.Com_lock_tables 67.0
servers.hostname.mysql.Com_optimize 68.0
servers.hostname.mysql.Com_preload_keys 69.0
servers.hostname.mysql.Com_prepare_sql 70.0
servers.hostname.mysql.Com_purge 71.0
servers.hostname.mysql.Com_purge_before_date 72.0
servers.hostname.mysql.Com_release_savepoint 73.0
servers.hostname.mysql.Com_rename_table 74.0
servers.hostname.mysql.Com_rename_user 75.0
servers.hostname.mysql.Com_repair 76.0
servers.hostname.mysql.Com_replace 77.0
servers.hostname.mysql.Com_replace_select 78.0
servers.hostname.mysql.Com_reset 79.0
servers.hostname.mysql.Com_restore_table 80.0
servers.hostname.mysql.Com_revoke 81.0
servers.hostname.mysql.Com_revoke_all 82.0
servers.hostname.mysql.Com_rollback 83.0
servers.hostname.mysql.Com_rollback_to_savepoint 84.0
servers.hostname.mysql.Com_savepoint 85.0
servers.hostname.mysql.Com_select 86.0
servers.hostname.mysql.Com_set_option 87.0
servers.hostname.mysql.Com_show_authors 88.0
servers.hostname.mysql.Com_show_binlog_events 89.0
servers.hostname.mysql.Com_show_binlogs 90.0
servers.hostname.mysql.Com_show_charsets 91.0
servers.hostname.mysql.Com_show_collations 92.0
servers.hostname.mysql.Com_show_column_types 93.0
servers.hostname.mysql.Com_show_contributors 94.0
servers.hostname.mysql.Com_show_create_db 95.0
servers.hostname.mysql.Com_show_create_event 96.0
servers.hostname.mysql.Com_show_create_func 97.0
servers.hostname.mysql.Com_show_create_proc 98.0
servers.hostname.mysql.Com_show_create_table 99.0
servers.hostname.mysql.Com_show_create_trigger 100.0
servers.hostname.mysql.Com_show_databases 101.0
servers.hostname.mysql.Com_show_engine_logs 102.0
servers.hostname.mysql.Com_show_engine_mutex 103.0
servers.hostname.mysql.Com_show_engine_status 104.0
servers.hostname.mysql.Com_show_errors 106.0
servers.hostname.mysql.Com_show_events 105.0
servers.hostname.mysql.Com_show_fields 107.0
servers.hostname.mysql.Com_show_function_status 108.0
servers.hostname.mysql.Com_show_grants 109.0
servers.hostname.mysql.Com_show_keys 110.0
servers.hostname.mysql.Com_show_master_status 111.0
servers.hostname.mysql.Com_show_new_master 112.0
servers.hostname.mysql.Com_show_open_tables 113.0
servers.hostname.mysql.Com_show_plugins 114.0
servers.hostname.mysql.Com_show_privileges 115.0
servers.hostname.mysql.Com_show_procedure_status 116.0
servers.hostname.mysql.Com_show_processlist 117.0
servers.hostname.mysql.Com_show_profile 118.0
servers.hostname.mysql.Com_show_profiles 119.0
servers.hostname.mysql.Com_show_slave_hosts 120.0
servers.hostname.mysql.Com_show_slave_status 121.0
servers.hostname.mysql.Com_show_status 122.0
servers.hostname.mysql.Com_show_storage_engines 123.0
servers.hostname.mysql.Com_show_table_status 124.0
servers.hostname.mysql.Com_show_tables 125.0
servers.hostname.mysql.Com_show_triggers 126.0
servers.hostname.mysql.Com_show_variables 127.0
servers.hostname.mysql.Com_show_warnings 128.0
servers.hostname.mysql.Com_slave_start 129.0
servers.hostname.mysql.Com_slave_stop 130.0
servers.hostname.mysql.Com_stmt_close 131.0
servers.hostname.mysql.Com_stmt_execute 132.0
servers.hostname.mysql.Com_stmt_fetch 133.0
servers.hostname.mysql.Com_stmt_prepare 134.0
servers.hostname.mysql.Com_stmt_reprepare 135.0
servers.hostname.mysql.Com_stmt_reset 136.0
servers.hostname.mysql.Com_stmt_send_long_data 137.0
servers.hostname.mysql.Com_truncate 138.0
servers.hostname.mysql.Com_uninstall_plugin 139.0
servers.hostname.mysql.Com_unlock_tables 140.0
servers.hostname.mysql.Com_update 141.0
servers.hostname.mysql.Com_update_multi 142.0
servers.hostname.mysql.Com_xa_commit 143.0
servers.hostname.mysql.Com_xa_end 144.0
servers.hostname.mysql.Com_xa_prepare 145.0
servers.hostname.mysql.Com_xa_recover 146.0
servers.hostname.mysql.Com_xa_rollback 147.0
servers.hostname.mysql.Com_xa_start 148.0
servers.hostname.mysql.Compression 149.0
servers.hostname.mysql.Connections 150.0
servers.hostname.mysql.Created_tmp_disk_tables 151.0
servers.hostname.mysql.Created_tmp_files 152.0
servers.hostname.mysql.Created_tmp_tables 153.0
servers.hostname.mysql.Delayed_errors 154.0
servers.hostname.mysql.Delayed_insert_threads 155.0
servers.hostname.mysql.Delayed_writes 156.0
servers.hostname.mysql.Exec_Master_Log_Pos 200
servers.hostname.mysql.Flush_commands 157.0
servers.hostname.mysql.Handler_commit 158.0
servers.hostname.mysql.Handler_delete 159.0
servers.hostname.mysql.Handler_discover 160.0
servers.hostname.mysql.Handler_prepare 161.0
servers.hostname.mysql.Handler_read_first 162.0
servers.hostname.mysql.Handler_read_key 163.0
servers.hostname.mysql.Handler_read_next 164.0
servers.hostname.mysql.Handler_read_prev 165.0
servers.hostname.mysql.Handler_read_rnd 166.0
servers.hostname.mysql.Handler_read_rnd_next 167.0
servers.hostname.mysql.Handler_rollback 168.0
servers.hostname.mysql.Handler_savepoint 169.0
servers.hostname.mysql.Handler_savepoint_rollback 170.0
servers.hostname.mysql.Handler_update 171.0
servers.hostname.mysql.Handler_write 172.0
servers.hostname.mysql.Innodb_buffer_pool_pages_data 173.0
servers.hostname.mysql.Innodb_buffer_pool_pages_dirty 174.0
servers.hostname.mysql.Innodb_buffer_pool_pages_flushed 175.0
servers.hostname.mysql.Innodb_buffer_pool_pages_free 176.0
servers.hostname.mysql.Innodb_buffer_pool_pages_misc 177.0
servers.hostname.mysql.Innodb_buffer_pool_pages_total 178.0
servers.hostname.mysql.Innodb_buffer_pool_read_ahead_rnd 179.0
servers.hostname.mysql.Innodb_buffer_pool_read_ahead_seq 180.0
servers.hostname.mysql.Innodb_buffer_pool_read_requests 181.0
servers.hostname.mysql.Innodb_buffer_pool_reads 182.0
servers.hostname.mysql.Innodb_buffer_pool_wait_free 183.0
servers.hostname.mysql.Innodb_buffer_pool_write_requests 184.0
servers.hostname.mysql.Innodb_data_fsyncs 185.0
servers.hostname.mysql.Innodb_data_pending_fsyncs 186.0
servers.hostname.mysql.Innodb_data_pending_reads 187.0
servers.hostname.mysql.Innodb_data_pending_writes 188.0
servers.hostname.mysql.Innodb_data_read 189.0
servers.hostname.mysql.Innodb_data_reads 190.0
servers.hostname.mysql.Innodb_data_writes 191.0
servers.hostname.mysql.Innodb_data_written 192.0
servers.hostname.mysql.Innodb_dblwr_pages_written 193.0
servers.hostname.mysql.Innodb_dblwr_writes 194.0
servers.hostname.mysql.Innodb_log_waits 195.0
servers.hostname.mysql.Innodb_log_write_requests 196.0
servers.hostname.mysql.Innodb_log_writes 197.0
servers.hostname.mysql.Innodb_os_log_fsyncs 198.0
servers.hostname.mysql.Innodb_os_log_pending_fsyncs 199.0
servers.hostname.mysql.Innodb_os_log_pending_writes 200.0
servers.hostname.mysql.Innodb_os_log_written 201.0
servers.hostname.mysql.Innodb_page_size 202.0
servers.hostname.mysql.Innodb_pages_created 203.0
servers.hostname.mysql.Innodb_pages_read 204.0
servers.hostname.mysql.Innodb_pages_written 205.0
servers.hostname.mysql.Innodb_row_lock_current_waits 206.0
servers.hostname.mysql.Innodb_row_lock_time 207.0
servers.hostname.mysql.Innodb_row_lock_time_avg 208.0
servers.hostname.mysql.Innodb_row_lock_time_max 209.0
servers.hostname.mysql.Innodb_row_lock_waits 210.0
servers.hostname.mysql.Innodb_rows_deleted 211.0
servers.hostname.mysql.Innodb_rows_inserted 212.0
servers.hostname.mysql.Innodb_rows_read 213.0
servers.hostname.mysql.Innodb_rows_updated 214.0
servers.hostname.mysql.Key_blocks_not_flushed 215.0
servers.hostname.mysql.Key_blocks_unused 216.0
servers.hostname.mysql.Key_blocks_used 217.0
servers.hostname.mysql.Key_read_requests 218.0
servers.hostname.mysql.Key_reads 219.0
servers.hostname.mysql.Key_write_requests 220.0
servers.hostname.mysql.Key_writes 221.0
servers.hostname.mysql.Last_query_cost 222.0
servers.hostname.mysql.Max_used_connections 223.0
servers.hostname.mysql.Not_flushed_delayed_rows 224.0
servers.hostname.mysql.Open_files 225.0
servers.hostname.mysql.Open_streams 226.0
servers.hostname.mysql.Open_table_definitions 227.0
servers.hostname.mysql.Open_tables 228.0
servers.hostname.mysql.Opened_files 229.0
servers.hostname.mysql.Opened_table_definitions 230.0
servers.hostname.mysql.Opened_tables 231.0
servers.hostname.mysql.Position 100
servers.hostname.mysql.Prepared_stmt_count 232.0
servers.hostname.mysql.Qcache_free_blocks 233.0
servers.hostname.mysql.Qcache_free_memory 234.0
servers.hostname.mysql.Qcache_hits 235.0
servers.hostname.mysql.Qcache_inserts 236.0
servers.hostname.mysql.Qcache_lowmem_prunes 237.0
servers.hostname.mysql.Qcache_not_cached 238.0
servers.hostname.mysql.Qcache_queries_in_cache 239.0
servers.hostname.mysql.Qcache_total_blocks 240.0
servers.hostname.mysql.Queries 241.0
servers.hostname.mysql.Questions 242.0
servers.hostname.mysql.Read_Master_Log_Pos 200
servers.hostname.mysql.Relay_Log_Pos 2000
servers.hostname.mysql.Relay_Log_Space 2000
servers.hostname.mysql.Rpl_status 243.0
servers.hostname.mysql.Seconds_Behind_Master 28
servers.hostname.mysql.Select_full_join 244.0
servers.hostname.mysql.Select_full_range_join 245.0
servers.hostname.mysql.Select_range 246.0
servers.hostname.mysql.Select_range_check 247.0
servers.hostname.mysql.Select_scan 248.0
servers.hostname.mysql.Slave_open_temp_tables 249.0
servers.hostname.mysql.Slave_retried_transactions 250.0
servers.hostname.mysql.Slave_running 251.0
servers.hostname.mysql.Slow_launch_threads 252.0
servers.hostname.mysql.Slow_queries 253.0
servers.hostname.mysql.Sort_merge_passes 254.0
servers.hostname.mysql.Sort_range 255.0
servers.hostname.mysql.Sort_rows 256.0
servers.hostname.mysql.Sort_scan 257.0
servers.hostname.mysql.Ssl_accept_renegotiates 258.0
servers.hostname.mysql.Ssl_accepts 259.0
servers.hostname.mysql.Ssl_callback_cache_hits 260.0
servers.hostname.mysql.Ssl_cipher 261.0
servers.hostname.mysql.Ssl_cipher_list 262.0
servers.hostname.mysql.Ssl_client_connects 263.0
servers.hostname.mysql.Ssl_connect_renegotiates 264.0
servers.hostname.mysql.Ssl_ctx_verify_depth 265.0
servers.hostname.mysql.Ssl_ctx_verify_mode 266.0
servers.hostname.mysql.Ssl_default_timeout 267.0
servers.hostname.mysql.Ssl_finished_accepts 268.0
servers.hostname.mysql.Ssl_finished_connects 269.0
servers.hostname.mysql.Ssl_session_cache_hits 270.0
servers.hostname.mysql.Ssl_session_cache_misses 271.0
servers.hostname.mysql.Ssl_session_cache_mode 272.0
servers.hostname.mysql.Ssl_session_cache_overflows 273.0
servers.hostname.mysql.Ssl_session_cache_size 274.0
servers.hostname.mysql.Ssl_session_cache_timeouts 275.0
servers.hostname.mysql.Ssl_sessions_reused 276.0
servers.hostname.mysql.Ssl_used_session_cache_entries 277.0
servers.hostname.mysql.Ssl_verify_depth 278.0
servers.hostname.mysql.Ssl_verify_mode 279.0
servers.hostname.mysql.Ssl_version 280.0
servers.hostname.mysql.Table_locks_immediate 281.0
servers.hostname.mysql.Table_locks_waited 282.0
servers.hostname.mysql.Tc_log_max_pages_used 283.0
servers.hostname.mysql.Tc_log_page_size 284.0
servers.hostname.mysql.Tc_log_page_waits 285.0
servers.hostname.mysql.Threads_cached 286.0
servers.hostname.mysql.Threads_connected 287.0
servers.hostname.mysql.Threads_created 288.0
servers.hostname.mysql.Threads_running 289.0
servers.hostname.mysql.Uptime 290.0
servers.hostname.mysql.Uptime_since_flush_status 291.0
```

