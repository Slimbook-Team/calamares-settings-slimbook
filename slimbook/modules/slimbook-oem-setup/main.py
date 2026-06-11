# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 Slimbook <dev@slimbook.es>
# SPDX-License-Identifier: GPL-3.0-only

import slimbook.kbd
import slimbook.info

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

        if (os.path.exists("/usr/sbin/gdm3")):
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read("/etc/gdm3/custom.conf")
            config["daemon"]["AutomaticLogin"] = username
            config["daemon"]["AutomaticLoginEnable"] = "True"
            with open("/etc/gdm3/custom.conf","w") as f:
                config.write(f)

    status = "Turn on keyboard backlight (where available)..."
    libcalamares.utils.debug(status)
    
    try:
        model = slimbook.info.get_model()
        max_brightness = slimbook.kbd.brightness_max(model)
        slimbook.kbd.brightness_set(model, max_brightness)
        slimbook.kbd.backlight_set(model, 0x16ff16)
    except:
        libcalamares.utils.debug("Something went wrong with backlight")

    return None
