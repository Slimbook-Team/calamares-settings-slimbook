# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 Slimbook <dev@slimbook.es>
# SPDX-License-Identifier: GPL-3.0-only

import os
import shutil
import configparser

import libcalamares
from libcalamares.utils import check_target_env_call

def run():
    global status

    status = "Disabling OEM mode..."
    libcalamares.utils.debug(status)
    check_target_env_call(["slimbook-installer", "--disable-oem"])

    username = libcalamares.globalstorage.value("autoLoginUser")
    if username is not None:
        status = "Setting up autologin for user {!s}.".format(username)
        libcalamares.utils.debug(status)

        config = configparser.ConfigParser()
        config.optionxform = str
        config.read("/etc/gdm3/custom.conf")
        config["daemon"]["AutomaticLogin"] = username
        config["daemon"]["AutomaticLoginEnable"] = "True"
        with open("/etc/gdm3/custom.conf","w") as f:
            config.write(f)

    if (os.path.exists("/usr/bin/slimbook-ai-tools-install")):
        status = "Installing AI tools, It may take a while..."
        libcalamares.utils.debug(status)
        check_target_env_call(["slimbook-ai-tools-install", "--oem"])

        # this workaround is needed because we are too late and skel is already deployed at recently created user home
        username = libcalamares.globalstorage.value("username")
        if username:
            check_target_env_call(["cp", "-r","/etc/skel/.var","/home/{0}".format(username)])
            check_target_env_call(["chown", "-R","{0}:{1}".format(username,username),"/home/{0}/.var".format(username)])

    return None
