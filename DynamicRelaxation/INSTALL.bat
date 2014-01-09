@echo off
for /d /r %%a in (*) do (
 @echo "%%a"
 copy DynamicRelaxation.py %%a
 copy DynamicRelaxationComponentCode.py %%a
 copy DynamicRelaxationPreSpecMaterials.py %%a
)
  
