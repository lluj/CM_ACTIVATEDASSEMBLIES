@echo off
for /d /r %%a in (*) do (
 del %%a%\DynamicRelaxation.py
 del %%a%\DynamicRelaxationComponentCode.py
 del %%a%\DynamicRelaxationPreSpecMaterials.py
 del %%a%\*.3dmbak
)
  
