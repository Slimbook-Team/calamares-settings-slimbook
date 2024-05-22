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

    status = "Enabling OEM mode..."
    libcalamares.utils.debug(status)
    check_target_env_call(["slimbook-installer", "--enable-oem"])

    status = "Preparing Grub..."
    libcalamares.utils.debug(status)
    target = libcalamares.globalstorage.value("rootMountPoint")
    efi_path = "{0}/boot/efi/EFI/".format(target)

    try :
        os.makedirs(efi_path + "ubuntu", exist_ok = True)
        shutil.copyfile(efi_path + "slimbookos/grub.cfg",efi_path + "ubuntu/grub.cfg")
    except Exception as e:
        libcalamares.utils.debug(e)

    status = "Installing extra packages..."
    libcalamares.utils.debug(status)
    check_target_env_call(["slimbook-installer", "--install-extra-packages"])

    status = "Installing extra drivers..."
    libcalamares.utils.debug(status)
    check_target_env_call(["ubuntu-drivers", "install"])

    return None
