# DriveSnapShotBatch
Windows batch script to easily backup complete drives with Drive SnapShot [1] at runtime with VSS [2].

# Usage
* Place your Drive SnapShot executable in the same folder (name it snapshot64_reg.exe)
* Start the script, Configuration
	* Backup placed in subfolder [machine]\[machine][drive][date][time]\[backup files]
	* Creates chunks of 10 GB 
	* Backup is encrypted from Drive SnapShot (using AES)
	
[1] http://www.drivesnapshot.de/en/index.htm
[2] https://de.wikipedia.org/wiki/Volume_Shadow_Copy_Service
