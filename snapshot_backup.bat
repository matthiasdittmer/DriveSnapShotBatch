@echo off

:: ask for drive letter
set /p source=Enter drive to backup: %=%
set /p pw=Enter password (cleared after entered): %=%
cls

:: options (use 1 GB chunks)
set options=-L10000 -pw=%pw% --CreateDir
set backupname=$computername_$disk_$year_$month_$day_$hour_$minute_$second
set destination=$computername\%backupname%\%backupname%

:: do the backup
snapshot64_reg.exe %source%: %destination% %options%

pause