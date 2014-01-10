@echo off
for /d /r %%a in (*) do (
 @echo "%%a"
 copy *.py %%a
)
  
