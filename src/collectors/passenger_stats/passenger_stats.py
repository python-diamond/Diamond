# coding=utf-8

"""
The PasengerCollector collects CPU and memory utilization of apache, nginx
and passenger processes.

Four key attributes to be published:

 * phusion_passenger_cpu
 * total_apache_memory
 * total_passenger_memory
 * total_nginx_memory

#### Dependencies

 * passenger-memory-stats

"""
import diamond.collector
import os
import re
import subprocess
from diamond.collector import str_to_bool


class PassengerCollector(diamond.collector.Collector):
    """
    Collect Memory and CPU Utilization for Passenger
    """

    def get_default_config_help(self):
        """
        Return help text
        """
        config_help = super(PassengerCollector, self).get_default_config_help()
        config_help.update({
            "bin":         "The path to the binary",
            "use_sudo":    "Use sudo?",
            "sudo_cmd":    "Path to sudo",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PassengerCollector, self).get_default_config()
        config.update({
            "path":         "passenger_stats",
            "bin":          "/usr/lib/ruby-flo/bin/passenger-memory-stats",
            "use_sudo":     False,
            "sudo_cmd":     "/usr/bin/sudo",
        })
        return config

    def get_passenger_memory_stats(self):
        """
        Execute passenger-memory-stats, parse its output, return dictionary with
        stats.
        """
        command = [self.config["bin"]]
        if str_to_bool(self.config["use_sudo"]):
            command.insert(0, self.config["sudo_cmd"])

        try:
            proc1 = subprocess.Popen(command, stdout=subprocess.PIPE)
            (std_out, std_err) = proc1.communicate()
        except OSError:
            return {}

        if std_out is None:
            return {}

        dict_stats = {
            "apache_procs": [],
            "nginx_procs": [],
            "passenger_procs": [],
            "apache_mem_total": 0.0,
            "nginx_mem_total": 0.0,
            "passenger_mem_total": 0.0,
        }
        #
        re_colour = re.compile("\x1B\[([0-9]{1,3}((;[0-9]{1,3})*)?)?[m|K]")
        re_digit = re.compile("^\d")
        #
        apache_flag = 0
        nginx_flag = 0
        passenger_flag = 0
        for raw_line in std_out.splitlines():
            line = re_colour.sub("", raw_line)
            if "Apache processes" in line:
                apache_flag = 1
            elif "Nginx processes" in line:
                nginx_flag = 1
            elif "Passenger processes" in line:
                passenger_flag = 1
            elif re_digit.match(line):
                # If line starts with digit, then store PID and memory consumed
                line_splitted = line.split()
                if apache_flag == 1:
                    dict_stats["apache_procs"].append(line_splitted[0])
                    dict_stats["apache_mem_total"] += float(line_splitted[4])
                elif nginx_flag == 1:
                    dict_stats["nginx_procs"].append(line_splitted[0])
                    dict_stats["nginx_mem_total"] += float(line_splitted[4])
                elif passenger_flag == 1:
                    dict_stats["passenger_procs"].append(line_splitted[0])
                    dict_stats[
                        "passenger_mem_total"] += float(line_splitted[3])

            elif "Processes:" in line:
                passenger_flag = 0
                apache_flag = 0
                nginx_flag = 0

        return dict_stats

    def get_passenger_cpu_usage(self, dict_stats):
        """
        Execute % top; and return STDOUT.
        """
        try:
            proc1 = subprocess.Popen(
                ["top", "-b", "-n", "2"],
                stdout=subprocess.PIPE)
            (std_out, std_err) = proc1.communicate()
        except OSError:
            return (-1)

        re_lspaces = re.compile("^\s*")
        re_digit = re.compile("^\d")
        overall_cpu = 0
        for raw_line in std_out.splitlines():
            line = re_lspaces.sub("", raw_line)
            if not re_digit.match(line):
                continue

            line_splitted = line.split()
            if line_splitted[0] in dict_stats["apache_procs"]:
                overall_cpu += float(line_splitted[8])
            elif line_splitted[0] in dict_stats["nginx_procs"]:
                overall_cpu += float(line_splitted[8])
            elif line_splitted[0] in dict_stats["passenger_procs"]:
                overall_cpu += float(line_splitted[8])

        return overall_cpu

    def collect(self):
        """
        Collector Passenger stats
        """
        if not os.access(self.config["bin"], os.X_OK):
            self.log.error("Path %s does not exist or is not executable",
                           self.config["bin"])
            return {}

        dict_stats = self.get_passenger_memory_stats()
        if len(dict_stats.keys()) == 0:
            return {}

        overall_cpu = self.get_passenger_cpu_usage(dict_stats)
        if overall_cpu >= 0:
            self.publish("phusion_passenger_cpu", overall_cpu)

        self.publish("total_apache_memory", dict_stats["apache_mem_total"])
        self.publish("total_nginx_memory", dict_stats["nginx_mem_total"])
        self.publish("total_passenger_memory",
                     dict_stats["passenger_mem_total"])
