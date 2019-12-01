# DriveSnapShotBatch
Windows batch / Python script to easily backup complete drives with Drive SnapShot [1] at runtime with VSS [2].

# Batch (old version in /batch/)
* Place your Drive SnapShot executable in the same folder (name it snapshot64_reg.exe)
* Start the script, Configuration
	* Backup placed in subfolder [machine]\\[machine][drive][date][time]\\[backup files]
	* Creates chunks of 10 GB 
	* Backup is encrypted from Drive SnapShot (using AES)
	
# Python (new version in /python/)
* Better version with a keep count and auto deletion of old backup folders
* Run superb_backup.bat to call Python script superb_backup.py

[1] http://www.drivesnapshot.de/en/index.htm
[2] https://en.wikipedia.org/wiki/Volume_Shadow_Copy_Service
