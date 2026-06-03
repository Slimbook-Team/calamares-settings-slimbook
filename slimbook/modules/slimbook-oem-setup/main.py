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

    sddm_conf = "/etc/sddm.conf"

    try:
        if (os.path.exists(sddm_conf)):
            status = "Configure SDDM with wayland..."
            libcalamares.utils.debug(status)

            config = configparser.ConfigParser()
            config.optionxform = str
            config.read(sddm_conf)
            config["General"] = {}
            config["General"]["DisplayServer"] = "wayland"
            with open(sddm_conf,"w") as f:
                config.write(f)
    except Exception as e:
        libcalamares.utils.debug(e)

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

    return None
