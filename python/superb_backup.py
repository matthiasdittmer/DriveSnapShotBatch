"""
Script to backup an entire partition under windows.
"""

from datetime import datetime
import time
import socket
import os
import sys
import shutil
import subprocess
import getpass
import win32api

VERSION = "1.1.0"

# config below
BACKUP_EXE = "snapshot64_reg.exe"
CHUNK_SIZE_MB = 10000
KEEP_COUNT = 2

# global variables
backup_dest_drive = ""
backup_src_drive = ""
backup_path = ""
backup_dest_free_space = ""
list_drives = []
list_folders = []

def build_backup_name(drive, with_datetime):
    global list_drives
    global backup_src_drive

    # get computer name
    str = socket.gethostname().upper()
    str = str + "_" + drive.upper()

    # add drive label
    for drive in list_drives:
        if drive[:1].upper() == backup_src_drive.upper():
            drive_info = win32api.GetVolumeInformation(drive)
            str = str + "_" + drive_info[0]
            break

    # add datetime
    if with_datetime:
        ts = int(time.time())
        date = datetime.fromtimestamp(ts)
        date_time_suffix = date.strftime('%Y_%m_%d_%H_%M_%S')
        str = str + "_" + date_time_suffix

    return str

def display_drives():
    global list_drives
    global backup_dest_drive
    global backup_dest_free_space

    # get all drives over WINAPI
    list_drives = win32api.GetLogicalDriveStrings()
    list_drives = list_drives.split('\000')[:-1]

    print("\nLIST OF DRIVES")
    # table header, use format with length
    print("{:6s}{:20s} {:9s}/ {:10s} {:8s} {:6s} {:20s}".format("DRIVE", "LABEL", "Used GB", "Total GB", "Free GB", "Filesystem", "Comment"))

    for drive in list_drives:
        try:
            # get additional drive information over WINAPI
            drive_info = win32api.GetVolumeInformation(drive)

            # get free space, used, total for current drive
            total, used, free = shutil.disk_usage(drive)
            total_str_gb = "{:5.2f}".format(total / 2**30).rjust(8)
            used_str_gb = "{:5.2f}".format(used/ 2**30).rjust(8)
            free_str_gb = "{:5.2f}".format(free / 2**30).rjust(8)

            # print table row with: drive letter, label, used/total GB, free GB, file system
            comment = ""
            if drive[:1] == backup_dest_drive:
                # mark backup destination drive, not useable as source
                comment = "backup destination drive, not useable as source"
                backup_dest_free_space = free_str_gb
            print("{:6s}{:20s}{:9s} / {:8s}  {:8s}  {:10s} {:20s}".format(drive[:1], drive_info[0], used_str_gb, total_str_gb, free_str_gb, drive_info[4], comment))

        except:
            print("{:6s}Error, no information available".format(drive[:1]))

def getSizeOfFolder(path):
    directory_size = 0
    for (path, dirs, files) in os.walk(path):
        for file in files:
            filename = os.path.join(path, file)
            directory_size += os.path.getsize(filename)
    return directory_size

def display_backups():
    global list_folders

    print("\nLIST OF BACKUPS")

    # search for all old backups (matching folder name COMPNAME_X_LABEL_ ...)
    list_folders = os.listdir("./")
    list_folders_filtered_all_backups = []
    for folder in list_folders:
        folder_split = folder.split("_")
        # check for at least three elements
        if len(folder_split) >= 3:
            # check if second element is single drive letter
            if len(folder_split[1]) == 1 and folder_split[1].isalpha():
                list_folders_filtered_all_backups.append(folder)

    if len(list_folders_filtered_all_backups) > 0:
        # print table with path, size GB
        print("{:50s} {:8s}".format("NAME", "SIZE GB"))
        for folder in list_folders_filtered_all_backups:
            size = getSizeOfFolder(folder)
            size_str = "{:5.2f}".format(size / 2**30).rjust(8)
            print("{:50s}{:8s}".format(folder, size_str))
    else:
        print("No backups found.")

def display_backup_config():
    global backup_dest_free_space
    global backup_path

    print("\nBACKUP CONFIGURATION")
    print("CHUNK SIZE: {} MB".format(CHUNK_SIZE_MB))
    print("KEEP COUNT: {}".format(KEEP_COUNT))
    print("FREE SPACE ON BACKUP DRIVE: {} GB".format(backup_dest_free_space))
    print("PATH OF BACKUP: {}\\".format(backup_path))

if __name__ == "__main__":

    print("Superb Backup " + VERSION + " started ... ")

    # check for exe
    if not os.path.exists(BACKUP_EXE):
        print(BACKUP_EXE + " not found.")
        input("Press ENTER to close window.")
        sys.exit()

    # backup destination information
    backup_dest_drive = os.getcwd()[:1]
    backup_path = os.getcwd()

    # display all drives
    display_drives()

    # display all found backups
    display_backups()

    # display backup config
    display_backup_config()

    # enter drive letter
    backup_src_drive = input("\nDrive letter to backup: ")

    # check drive letter
    if not os.path.exists(backup_src_drive + ":\\"):
        print("\nDrive " + backup_src_drive + " not found.")
        input("Press ENTER to close window.")
        sys.exit()

     # check for invalid drive choice
    if backup_src_drive.upper() == backup_dest_drive.upper():
        print("\nInvalid backup drive " + backup_src_drive + ". Same as destination drive.")
        input("Press ENTER to close window.")
        sys.exit()

    # show prompt to enter pw
    pw = getpass.getpass("Enter encryption password: ")

    # get all backups for current source drive (matching computer name and drive letter)
    backup_name = build_backup_name(backup_src_drive, False)
    list_folders_filtered = list(filter(lambda x: x.startswith(backup_name), list_folders))

    # get old backups in path
    if len(list_folders_filtered) > 0:
        print("\nOld backups found. Current count: " + str(len(list_folders_filtered)))
        # sort by date
        list_folders_filtered.sort(reverse = False)
        # do keep / delete logic
        if len(list_folders_filtered) >= KEEP_COUNT:
            # delete the oldest backup to make space for one new
            print("Deleting old backup: " + list_folders_filtered[0])
            shutil.rmtree("./" + list_folders_filtered[0])
        else:
            print("No old backups to delete.")
    else:
        print("\nNo old backups found.")

    # check size of backup drive and space on own drive
    total_src, used_src, free_src = shutil.disk_usage(backup_src_drive + ":\\")
    total_dest, used_dst, free_dst = shutil.disk_usage(backup_dest_drive + ":\\")

    # do space logic
    # backup will be compressed by tool (checking for uncompressed size only)
    if free_dst < used_src:
        print("\nError: not enough space on destination drive. Needed / Free: {:.3f} GB / {:.3f} GB".format(used_src / 2**30, free_dst / 2**30))
        input("Press ENTER to close window.")
        sys.exit()
    else:
        print("\nEnough space on destination drive. Needed / Free: {:.3f} GB / {:.3f} GB".format(used_src / 2**30, free_dst / 2**30))

    # do backup
    backup_name = build_backup_name(backup_src_drive, True)
    print("Starting backup to folder: " + backup_name)
    res = subprocess.call([BACKUP_EXE, backup_src_drive + ":", "./" + backup_name + "/" + backup_name, "-L" + str(CHUNK_SIZE_MB), "-pw=" + pw, "--CreateDir"], shell = True)

    # print finish message
    print("\nFinished successfully.")
    input("Press ENTER to close window.")
