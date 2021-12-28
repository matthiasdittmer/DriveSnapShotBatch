![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/matthiasdittmer/DriveSnapShotBatch)
![GitHub](https://img.shields.io/github/license/matthiasdittmer/DriveSnapShotBatch)

# DriveSnapShotBatch
Windows batch / Python script to easily backup complete drives with Drive SnapShot [1] at runtime with VSS [2].

## Batch (old version in /batch/)
* Place your Drive SnapShot executable in the same folder (name it snapshot64_reg.exe)
* Start the script, Configuration
	* Backup placed in subfolder [machine]\\[machine][drive][date][time]\\[backup files]
	* Creates chunks of 10 GB
	* Backup is encrypted from Drive SnapShot (using AES)

## Python (new version in /python/)
* Better version with a keep count and auto deletion of old backup folders
* Run superb_backup.bat to call Python script superb_backup.py

### Usage
The script uses extern modules of which some are not included in the default Python installation:
```
datetime
time
socket
os
sys
shutil
subprocess
getpass
win32api    # hint: install over "pip install pywin32"
```

Install them over your preferred package manager (e.g. "pip install &lt;module name&gt;").

# Version History
## 1.0.0 (2019-12-01)
* First version of pure batch and Python version.
## 1.1.0 (2021-12-28)
* Added a list of available drives with information.
* Added a list of backups in the current folder with size information.
* Added information about the backup drive and backup config.
* Added more general sanity checking for user inputs.
* Changed backup name. The Drive label is included now.

# Sample screenshot
![sample screenshot](/screenshot_cmd.png)

# References
* [1] http://www.drivesnapshot.de/en/index.htm
* [2] https://en.wikipedia.org/wiki/Volume_Shadow_Copy_Service
