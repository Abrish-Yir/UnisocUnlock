@echo off
title Install SPRD Driver
color 0B
cls

echo ============================================
echo   SPRD USB driver installer
echo ============================================
echo.
echo this installs the spreadtrum/unisoc driver
echo you need this for the FRP bypass to work
echo.
echo ============================================
echo.

if exist "tools\zadig.exe" (
    echo [INFO] zadig found opening it now...
    echo.
    echo WHAT TO DO:
    echo 1. in zadig go to Options then List All Devices
    echo 2. select SPRD U2S Diag from the dropdown
    echo 3. click Replace Driver (WinUSB)
    echo 4. wait for it to finish
    echo.
    start "" "tools\zadig.exe"
    pause
) else (
    echo [INFO] zadig not found
    echo.
    echo OPTION 1 - get Zadig:
    echo download from https://zadig.akeo.ie/
    echo save it in the tools\ folder as zadig.exe
    echo.
    echo OPTION 2 - manual driver:
    echo 1. download SPRD driver from https://androiddatahost.com/dsa6h
    echo 2. extract and run the installer
    echo.
    echo OPTION 3 - windows update:
    echo 1. plug in your phone
    echo 2. open device manager
    echo 3. right click the unknown device
    echo 4. select update driver
    echo 5. choose search automatically
    echo.
    pause
)

echo.
echo after installing the driver plug in your phone
echo and check device manager for SPRD U2S Diag
echo.
pause
