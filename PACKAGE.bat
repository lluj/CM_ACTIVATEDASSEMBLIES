@echo off

:: - Copy python files to GH component folder of current user


    set TEMPDIR=%userprofile%\Desktop\CITA_workshop_2014
    rmdir %TEMPDIR%
    mkdir %TEMPDIR%
    mkdir %TEMPDIR%\examples
	
    cd DynamicRelaxation
    copy INSTALL_GH.bat %TEMPDIR%
    copy *.py %TEMPDIR%
	xcopy 04_workshop2014 %TEMPDIR%\examples /Y 
	
	cd ..
	
	echo %~p0%CITA_workshop_2014.zip
	
	CScript zip.vbs %TEMPDIR%  %~p0\CITA_workshop_2014.zip
	
    pause