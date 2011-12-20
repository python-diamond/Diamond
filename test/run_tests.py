#!/usr/bin/python

from common import *

from test_cpu_collector import *
from test_disk import *
from test_disk_space_collector import *
from test_disk_usage_collector import *
from test_filestat_collector import *
from test_load_average_collector import *
from test_memory_collector import *
from test_network_collector import *
from test_sockstat_collector import *
from test_tcp_collector import *
from test_vmstat_collector import *

################################################################################
if __name__ == "__main__":
    unittest.main()

