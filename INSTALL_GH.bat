@echo off

:: - Copy python files to GH component folder of current user

cd DynamicRelaxation
copy *.py %userprofile%\AppData\Roaming\Grasshopper\Libraries
  
:: - Copy the workshop folder to the Desktop

mkdir %userprofile%\Desktop\CITA_workshop_2014
xcopy 04_workshop2014 %userprofile%\Desktop\CITA_workshop_2014 /E

cd ..
