@echo off
setlocal

:: Define the path to the ADB executable
set ADB_PATH="C:\Program Files\Netease\MuMuPlayerGlobal-12.0\shell"

:: List of device ports to connect to
set DEVICE_PORTS=(16448 16480 16512 16544 16576 16608 16640 16672 16704 16736 16768 16800 16832 16864 16896 16928)

:: Change to the ADB directory
cd /d %ADB_PATH%

:: Kill the ADB server and wait for 2 seconds
start cmd /c "adb kill-server"
start cmd /c "adb devices"
timeout /t 2 >nul

:: Open a new command prompt for each ADB connect command
for %%p in %DEVICE_PORTS% do (
    start cmd /c "adb connect 127.0.0.1:%%p"
)
timeout /t 5 >nul
adb devices
:: Indicate completion of script execution
echo Connection attempts made to all devices.
pause
endlocal
