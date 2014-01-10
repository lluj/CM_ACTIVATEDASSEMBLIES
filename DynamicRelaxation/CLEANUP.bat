@echo off
for /d /r %%a in (*) do (
 del %%a%\*.py
 del %%a%\*.3dmbak
)
  
