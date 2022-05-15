#!/usr/bin/env python3

import os
import shutil
import sys
import socket
import psutil

def check_reboot():
    """Returns True if the computer has a pending reboot"""
    return os.path.exists("run/reboot.required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk space. False otherwise"""
    du = shutil.disk_usage(disk)
    # Calculates the percentage of the free space
    percent_free = 100 * du.free / du.total
    # Calculates how many free gigabytes
    gigabytes_free = du.free / 2 **30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, false otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_cpu_constraint():
    """Returns True if the cpu is having too much usage, False otherwise."""
    return psutil.cpu_percent(1) > 75

def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main():
    checks = [
        (check_reboot, "Pending Reboot"), 
        (check_root_full, "Root partition full"),
        (check_no_network, "No working network."),
        (check_cpu_constraint, "Fails to resolve Google URL.")
    ]

    everything_ok = True

    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False
    
    if not everything_ok:
        sys.exit(1)


# ----------------------
# To avoid code repetition we create a list containing the names of the functions that we want to call
# and the message to print if the function succeeds.


#     if check_reboot():
#         print("Pending Reboot!")
#         sys.exit(1)
# 
#     if check_root_full():
#         print("Root partition full.")
#         sys.exit(1)

    print("Everything ok.")
    sys.exit()
main()

