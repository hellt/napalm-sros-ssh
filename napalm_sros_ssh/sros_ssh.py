# -*- coding: utf-8 -*-
# Copyright 2020 Roman Dodin (dodin.roman@gmail.com). All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""
Napalm driver for Nokia SR OS SSH.

https://github.com/hellt/napalm-sros-ssh
"""

from napalm.base import NetworkDriver


class NokiaSROSSSHDriver(NetworkDriver):
    """Napalm driver for Nokia SR OS.
       Uses Netmiko for interacting with the SR OS device.
       Limited functionality - configuration commands only.
    """

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.device = None
        self.netmiko_device_type = "nokia_sros"
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.force_no_enable = True  # disable enable mode trigger in _netmiko_open()

        if optional_args is None:
            optional_args = {}
        self.opt_args = optional_args
        self.port = optional_args.get("port", 22)

    def open(self):
        self.device = self._netmiko_open(
            device_type=self.netmiko_device_type, netmiko_optional_args=self.opt_args
        )

    def close(self):
        self._netmiko_close()

    def load_merge_candidate(self, filename=None, config=None):
        """
        Populates the candidate configuration. You can populate it from a file or from a string.
        If you send both a filename and a string containing the configuration,
        the file takes precedence.

        If you use this method the existing configuration will be merged
        with the candidate configuration once you commit the changes.
        This method will not change the configuration by itself.

        :param filename: Path to the file containing the desired configuration. By default is None.
        :param config: String containing the desired configuration.
        """
        if filename:
            self.device.send_config_from_file(config_file=filename)
        else:
            self.device.send_config_set(config)

    def load_replace_candidate(self, filename=None, config=None):
        """
        Populates the candidate configuration. You can populate it from a file or from a string.
        If you send both a filename and a string containing the configuration, the file takes
        precedence.

        If you use this method the existing configuration will be merged with the candidate
        configuration once you commit the changes. This method will not change the configuration
        by itself.

        :param filename: Path to the file containing the desired configuration. By default is None.
        :param config: String containing the desired configuration.
        """

        self.device.send_config_set(["delete configure"])

        if filename:
            self.device.send_config_from_file(config_file=filename)
        else:
            self.device.send_config_set(config)

    def commit_config(self, message=""):
        """
        Commits the changes requested by the method load_replace_candidate or load_merge_candidate.
        """
        self.device.commit()

    def discard_config(self):
        """
        Discards the configuration loaded into the candidate.
        """
        self.device.send_command("discard")

    def compare_config(self):
        """
        :return: A string showing the difference between the running configuration and the candidate
        configuration. The running_config is loaded automatically just before doing the comparison
        so there is no need for you to do it.
        """
        return self.device.send_command("compare")

    def get_config(self, retrieve="all", full=False):
        """
            Return the configuration of a device.
            Parameters:
                retrieve (string) – Which configuration type you want to populate, default is all of
                them.
                The rest will be set to “”.
                full (bool) – Not applicable to SR OS.
            Returns:
                running(string) - Representation of the native running configuration

                candidate(string) - Representation of the native candidate configuration.
                Not implemented.

                startup(string) - Representation of the native startup configuration.
                Not implemented.

            Return type:
            The object returned is a dictionary with a key for each configuration store
        """
        cfg = {}

        cfg["running"] = self.device.send_command("admin show configuration")
        cfg["cadidate"] = ""
        cfg["startup"] = ""
        return cfg
