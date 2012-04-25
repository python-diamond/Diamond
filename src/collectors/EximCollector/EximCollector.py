from diamond import *
import diamond.collector
import subprocess
import os

class EximCollector(diamond.collector.Collector):
  """
  Shells out to get the exim queue length
  """

  COMMAND = ['/usr/sbin/exim', '-bpc']

  def collect(self):
    if not os.access(EximCollector.COMMAND[0], os.X_OK):
      return
    queuesize = subprocess.Popen(EximCollector.COMMAND, stdout=subprocess.PIPE).communicate()[0][:-1]
    self.publish('queuesize', queuesize)
