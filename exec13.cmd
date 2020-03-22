@ECHO OFF
set s5=8300
set s1=6158
set e=9100
python js9.py -s %s1% -e %e%
python sql10.py --auto
python update11.py -s 7600 -e %e%
ECHO.
ECHO UPDATE FINISHED
ECHO START DOWNLOADING
ECHO.
python 5.py -s %s5% -e %e%