@echo off
echo converting .po files to .mo files
echo if you experience problems with this version of msgfmt.exe try the win32.crt
version from http://home.a-city.de/franco.bez/gettext/gettext_win32_en.html
dir /B *.po > trans.txt
for /F "tokens=1,* delims=. " %%i in (trans.txt) do (
   echo Input: %%i.%%j
   echo Output: %%i.mo
   msgfmt %%i -o %%i.mo
)
del trans.txt

