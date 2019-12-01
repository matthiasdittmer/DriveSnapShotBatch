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

VERSION = "1.0.0"

# config below
BACKUP_EXE = "snapshot64_reg.exe"
CHUNK_SIZE_MB = 10000
KEEP_COUNT = 2

def build_backup_name(drive, with_datetime):
    # format computername_drive_date_time
    str = socket.gethostname().upper()
    str = str + "_" + drive.upper()
    
    if with_datetime:
        ts = int(time.time())
        date = datetime.fromtimestamp(ts)
        date_time_suffix = date.strftime('%Y_%m_%d_%H_%M_%S')
        str = str + "_" + date_time_suffix
    
    return str
    
if __name__ == "__main__":
    
    print("Superb Backup " + VERSION + " started ... ")
    
    # check for exe
    if not os.path.exists(BACKUP_EXE):
        print(BACKUP_EXE + " not found.")
        input("Press ENTER to close window.")
        sys.exit()
    
    # enter drive letter
    drive = input("Drive letter to backup: ")
    
    # check drive letter
    if not os.path.exists(drive + ":\\"):
        print("Drive " + drive + " not found.")
        input("Press ENTER to close window.")
        sys.exit()
    
    # show prompt to enter pw
    pw = getpass.getpass("Enter encryption password: ")
    
    # get old backups in path
    backup_name = build_backup_name(drive, False)
    list_folders = os.listdir("./")
    list_folders_filtered = list(filter(lambda x: x.startswith(backup_name), list_folders))
    if len(list_folders_filtered) > 0:
        print("Old backups found. Current count: " + str(len(list_folders_filtered)))
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
        print("No old backups found.")
    
    # check size of backup drive and space on own drive
    total_src, used_src, free_src = shutil.disk_usage(drive + ":\\")
    total_dest, used_dst, free_dst = shutil.disk_usage(os.getcwd()[:3])
    
    # do space logic
    # backup will be compressed by tool (checking for uncompressed size only)
    if free_dst < used_src:
        print("Error: not enough space on destination drive. Needed / Free: {:.3f} GB / {:.3f} GB".format(used_src / 2**30, free_dst / 2**30))
        input("Press ENTER to close window.")
        sys.exit()
    else:
        print("Enough space on destination drive. Needed / Free: {:.3f} GB / {:.3f} GB".format(used_src / 2**30, free_dst / 2**30))

    # do backup
    backup_name = build_backup_name(drive, True)
    print("Starting backup to folder: " + backup_name)
    res = subprocess.call([BACKUP_EXE, drive + ":", "./" + backup_name + "/" + backup_name, "-L" + str(CHUNK_SIZE_MB), "-pw=" + pw, "--CreateDir"], shell = True)
    
    # print finish message
    print("Finished successfully.")
    input("Press ENTER to close window.")
    