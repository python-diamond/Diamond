# coding=utf-8
"""
IcingaStats collector - collect statistics exported by Icinga/Nagios
via status.dat file.
"""
import diamond.collector
import re
import time

RE_LSPACES = re.compile("^[\s\t]*")
RE_TSPACES = re.compile("[\s\t]*$")


class IcingaStatsCollector(diamond.collector.Collector):
    """
    Collect Icinga Stats
    """

    def collect(self):
        """
        Collect and publish metrics
        """
        stats = self.parse_stats_file(self.config["status_path"])
        if len(stats) == 0:
            return {}
        elif "info" not in stats.keys():
            return {}
        elif "programstatus" not in stats.keys():
            return {}

        metrics = self.get_icinga_stats(stats["programstatus"])
        if "hoststatus" in stats.keys():
            metrics = dict(
                metrics.items() + self.get_host_stats(
                    stats["hoststatus"]).items())

        if "servicestatus" in stats.keys():
            metrics = dict(
                metrics.items() + self.get_svc_stats(
                    stats["servicestatus"]).items())

        for metric in metrics.keys():
            self.log.debug("Publishing '%s %s'.", metric, metrics[metric])
            self.publish(metric, metrics[metric])

    def get_default_config_help(self):
        """
        Return help text
        """
        config_help = super(IcingaStatsCollector,
                            self).get_default_config_help()
        config_help.update({
            "status_path": "Path to Icinga status.dat file"
        })
        return config_help

    def get_default_config(self):
        """
        Returns default settings for collector
        """
        config = super(IcingaStatsCollector, self).get_default_config()
        config.update({
            "path": "icinga_stats",
            "status_path": "/var/lib/icinga/status.dat",
        })
        return config

    def get_icinga_stats(self, app_stats):
        """ Extract metrics from 'programstatus' """
        stats = {}
        stats = dict(stats.items() + self._get_active_stats(app_stats).items())
        stats = dict(stats.items() + self._get_cached_stats(app_stats).items())
        stats = dict(
            stats.items() + self._get_command_execution(app_stats).items())
        stats = dict(
            stats.items() + self._get_externalcmd_stats(app_stats).items())
        stats["uptime"] = self._get_uptime(app_stats)
        return stats

    def parse_stats_file(self, file_name):
        """ Read and parse given file_name, return config as a dictionary """
        stats = {}
        try:
            with open(file_name, "r") as fhandle:
                fbuffer = []
                save_buffer = False
                for line in fhandle:
                    line = line.rstrip("\n")
                    line = self._trim(line)
                    if line == "" or line.startswith("#"):
                        continue
                    elif line.endswith("{"):
                        save_buffer = True
                        fbuffer.append(line)
                        continue
                    elif line.endswith("}"):
                        tmp_dict = self._parse_config_buffer(fbuffer)
                        fbuffer = None
                        fbuffer = list()
                        if len(tmp_dict) < 1:
                            continue

                        if tmp_dict["_type"] == "info":
                            stats["info"] = tmp_dict
                        elif tmp_dict["_type"] == "programstatus":
                            stats["programstatus"] = tmp_dict
                        else:
                            entity_type = tmp_dict["_type"]
                            if entity_type not in stats.keys():
                                stats[entity_type] = []

                            stats[entity_type].append(tmp_dict)

                        continue
                    elif save_buffer is True:
                        fbuffer.append(line)

        except Exception as exception:
            self.log.info("Caught exception: %s", exception)

        return stats

    def get_host_stats(self, hosts):
        """ Get statistics for Hosts, resp. Host entities """
        stats = {
            "hosts.total": 0,
            "hosts.ok": 0,
            "hosts.down": 0,
            "hosts.unreachable": 0,
            "hosts.flapping": 0,
            "hosts.in_downtime": 0,
            "hosts.checked": 0,
            "hosts.scheduled": 0,
            "hosts.active_checks": 0,
            "hosts.passive_checks": 0,
        }
        for host in list(hosts):
            if type(host) is not dict:
                continue

            sane = self._sanitize_entity(host)
            stats["hosts.total"] += 1
            stats["hosts.flapping"] += self._trans_binary(sane["flapping"])
            stats[
                "hosts.in_downtime"] += self._trans_dtime(sane["in_downtime"])
            stats["hosts.checked"] += self._trans_binary(sane["checked"])
            stats["hosts.scheduled"] += self._trans_binary(sane["scheduled"])
            stats["hosts.active_checks"] += sane["active_checks"]
            stats["hosts.passive_checks"] += sane["passive_checks"]
            state_key = self._trans_host_state(sane["state"])
            stats["hosts.%s" % (state_key)] += 1

        return stats

    def get_svc_stats(self, svcs):
        """ Get statistics for Services, resp. Service entities """
        stats = {
            "services.total": 0,
            "services.ok": 0,
            "services.warning": 0,
            "services.critical": 0,
            "services.unknown": 0,
            "services.flapping": 0,
            "services.in_downtime": 0,
            "services.checked": 0,
            "services.scheduled": 0,
            "services.active_checks": 0,
            "services.passive_checks": 0,
        }
        for svc in svcs:
            if type(svc) is not dict:
                continue

            sane = self._sanitize_entity(svc)
            stats["services.total"] += 1
            stats["services.flapping"] += self._trans_binary(sane["flapping"])
            stats["services.in_downtime"] += self._trans_dtime(
                sane["in_downtime"])
            stats["services.checked"] += self._trans_binary(sane["checked"])
            stats[
                "services.scheduled"] += self._trans_binary(sane["scheduled"])
            stats["services.active_checks"] += sane["active_checks"]
            stats["services.passive_checks"] += sane["passive_checks"]
            state_key = self._trans_svc_state(sane["state"])
            stats["services.%s" % (state_key)] += 1

        return stats

    def _convert_tripplet(self, tripplet):
        """ Turn '10,178,528' into tuple of integers """
        splitted = tripplet.split(",")
        if len(splitted) != 3:
            self.log.debug("Got %i chunks, expected 3.", len(splitted))
            return (0, 0, 0)

        try:
            x01 = int(splitted[0])
            x05 = int(splitted[1])
            x15 = int(splitted[2])
        except Exception as exception:
            self.log.warning("Caught exception: %s", exception)
            x01 = 0
            x05 = 0
            x15 = 0

        return (x01, x05, x15)

    def _get_active_stats(self, app_stats):
        """
        Process:
          * active_scheduled_host_check_stats
          * active_scheduled_service_check_stats
          * active_ondemand_host_check_stats
          * active_ondemand_service_check_stats
        """
        stats = {}
        app_keys = [
            "active_scheduled_host_check_stats",
            "active_scheduled_service_check_stats",
            "active_ondemand_host_check_stats",
            "active_ondemand_service_check_stats",
        ]
        for app_key in app_keys:
            if app_key not in app_stats.keys():
                continue

            splitted = app_key.split("_")
            metric = "%ss.%s_%s" % (splitted[2], splitted[0], splitted[1])
            (x01, x05, x15) = self._convert_tripplet(app_stats[app_key])
            stats["%s.01" % (metric)] = x01
            stats["%s.05" % (metric)] = x05
            stats["%s.15" % (metric)] = x15

        return stats

    def _get_cached_stats(self, app_stats):
        """
        Process:
         * cached_host_check_stats
         * cached_service_check_stats
        """
        stats = {}
        app_keys = [
            "cached_host_check_stats",
            "cached_service_check_stats",
        ]
        for app_key in app_keys:
            if app_key not in app_stats.keys():
                continue

            (x01, x05, x15) = self._convert_tripplet(app_stats[app_key])
            scratch = app_key.split("_")[1]
            stats["%ss.cached.01" % (scratch)] = x01
            stats["%ss.cached.05" % (scratch)] = x05
            stats["%ss.cached.15" % (scratch)] = x15

        return stats

    def _get_command_execution(self, app_stats):
        """
        Process:
         * serial_host_check_stats
         * parallel_host_check_stats
        """
        stats = {}
        app_keys = [
            "serial_host_check_stats",
            "parallel_host_check_stats",
        ]
        for app_key in app_keys:
            if app_key not in app_stats.keys():
                continue

            scratch = app_key.split("_")[0]
            (x01, x05, x15) = self._convert_tripplet(app_stats[app_key])
            stats["hosts.executed_%s.01" % scratch] = x01
            stats["hosts.executed_%s.05" % scratch] = x05
            stats["hosts.executed_%s.15" % scratch] = x15

        return stats

    def _get_externalcmd_stats(self, app_stats):
        """
        Process:
         * high_external_command_buffer_slots
         * total_external_command_buffer_slots
         * used_external_command_buffer_slots
         * external_command_stats=
        """
        khigh = "high_external_command_buffer_slots"
        ktotal = "total_external_command_buffer_slots"
        kused = "used_external_command_buffer_slots"
        kstats = "external_command_stats"
        aliases = {
            khigh: "external_command.buffer_high",
            ktotal: "external_command.buffer_total",
            kused: "external_command.buffer_used",
            "x01": "external_command.01",
            "x05": "external_command.05",
            "x15": "external_command.15",
        }
        stats = {}
        if khigh in app_stats.keys() and str(app_stats[khigh]).isdigit():
            key = aliases[khigh]
            stats[key] = int(app_stats[khigh])

        if ktotal in app_stats.keys() and str(app_stats[ktotal].isdigit()):
            key = aliases[ktotal]
            stats[key] = int(app_stats[ktotal])

        if kused in app_stats.keys() and str(app_stats[kused].isdigit()):
            key = aliases[kused]
            stats[key] = int(app_stats[ktotal])

        if kstats in app_stats.keys():
            (x01, x05, x15) = self._convert_tripplet(app_stats[kstats])
            stats[aliases["x01"]] = x01
            stats[aliases["x05"]] = x05
            stats[aliases["x01"]] = x15

        return stats

    def _get_uptime(self, app_stats):
        """ Return Icinga's uptime """
        if "program_start" not in app_stats.keys():
            return 0

        if not app_stats["program_start"].isdigit():
            return 0

        uptime = int(time.time()) - int(app_stats["program_start"])
        if uptime < 0:
            return 0

        return uptime

    def _parse_config_buffer(self, fbuffer):
        """ Parse buffered chunk of config into dict """
        if len(fbuffer) < 1 or not fbuffer[0].endswith("{"):
            # Invalid input
            return {}

        entity = {}
        entity_type = fbuffer.pop(0)
        entity_type = entity_type.rstrip("{")
        entity["_type"] = self._trim(entity_type)
        for chunk in fbuffer:
            splitted = chunk.split("=")
            if len(splitted) < 2:
                # If there is no '=', then it's an invalid line
                continue

            key = self._trim(splitted[0])
            value = self._trim("=".join(splitted[1:]))
            entity[key] = value

        return entity

    def _sanitize_entity(self, entity):
        """
        Make given entity 'sane' for further use.
        """
        aliases = {
            "current_state": "state",
            "is_flapping": "flapping",
            "scheduled_downtime_depth": "in_downtime",
            "has_been_checked": "checked",
            "should_be_scheduled": "scheduled",
            "active_checks_enabled": "active_checks",
            "passive_checks_enabled": "passive_checks",
        }
        sane = {}
        for akey in aliases.keys():
            sane[aliases[akey]] = None

        aliases_keys = aliases.keys()
        for key in entity.keys():
            if key not in aliases_keys:
                continue

            alias = aliases[key]
            try:
                sane[alias] = int(entity[key])
            except Exception:
                sane[alias] = None

        if sane["active_checks"] not in [0, 1]:
            sane["active_checks"] = 0
        elif sane["active_checks"] == 1:
            sane["passive_checks"] = 0

        if sane["passive_checks"] not in [0, 1]:
            sane["passive_checks"] = 0

        return sane

    def _trans_binary(self, value):
        """ Given value is expected to be a binary - 0/1 """
        try:
            conv = int(value)
        except ValueError:
            return 0

        if conv not in [0, 1]:
            return 0

        return conv

    def _trans_dtime(self, value):
        """ Translate scheduled downtime """
        try:
            conv = int(value)
        except ValueError:
            return 0

        if conv < 1:
            return 0

        return conv

    def _trans_host_state(self, state):
        """ Translate/validate Host state """
        if state == 0:
            return "ok"
        elif state == 1:
            return "down"
        else:
            return "unreachable"

    def _trans_svc_state(self, state):
        """ Translate/validate Service state """
        if state == 0:
            return "ok"
        elif state == 1:
            return "warning"
        elif state == 2:
            return "critical"
        else:
            return "unknown"

    def _trim(self, somestr):
        """ Trim left-right given string """
        tmp = RE_LSPACES.sub("", somestr)
        tmp = RE_TSPACES.sub("", tmp)
        return str(tmp)
