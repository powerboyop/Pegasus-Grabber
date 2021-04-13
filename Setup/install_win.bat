@echo off
title Pegasus Installer
cls

echo Installing modules....
echo If you have any problems you can create issue on github https://github.com/Its-Vichy/Pegasus-Grabber

npm i -g asar
pip install -r requirements.txt
echo Install Successfully
pause