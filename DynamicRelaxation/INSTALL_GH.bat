@echo off

:: - Copy python files to GH component folder of current user

copy *.py %userprofile%\AppData\Roaming\Grasshopper\Libraries
  
:: - Copy the workshop folder to the Desktop

mkdir %userprofile%\Desktop\CITA_workshop_2014
xcopy examples %userprofile%\Desktop\CITA_workshop_2014 /E

pause