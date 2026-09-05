@echo off
title Unisoc FRP Bypass
color 0A
cls

echo ============================================
echo   unisoc FRP bypass tool
echo   CVE-2022-38694 exploit
echo ============================================
echo.
echo this removes FRP (google account lock)
echo from unisoc/spreadtrum phones
echo.
echo WARNING: this erases the persist partition
echo backup your IMEI data first if you can
echo.
echo ============================================
echo.

if not exist "tools\spd_dump.exe" (
    echo [ERROR] tools\spd_dump.exe not found!
    echo make sure you extracted all the files
    pause
    exit /b 1
)

set FDL_DIR=
if exist "exploit\ums9230\fdl1-dl.bin" (
    set FDL_DIR=exploit\ums9230
    set EXEC_ADDR=0x65015f08
    set FDL1_ADDR=0x65000800
    set FDL2_ADDR=0x9efffe00
    echo [INFO] found UMS9230 (T606) files
) else if exist "exploit\ums512\fdl1.bin" (
    set FDL_DIR=exploit\ums512
    set EXEC_ADDR=0x3EE8
    set FDL1_ADDR=0x28007000
    set FDL2_ADDR=0x9efffe00
    echo [INFO] found UMS512 (T610) files
) else if exist "exploit\sc9863a\fdl1.bin" (
    set FDL_DIR=exploit\sc9863a
    set EXEC_ADDR=0x4EE8
    set FDL1_ADDR=0x28007000
    set FDL2_ADDR=0x9efffe00
    echo [INFO] found SC9863A files
) else (
    echo [ERROR] no exploit files found!
    echo.
    echo download them from:
    echo https://github.com/TomKing062/CVE-2022-38694_unlock_bootloader/releases/tag/1.72
    echo.
    echo put fdl1-dl.bin fdl2-dl.bin and custom_exec_no_verify_*.bin
    echo in the exploit\CHIPSET folder
    pause
    exit /b 1
)

echo.
echo ============================================
echo   how to do this
echo ============================================
echo.
echo 1. make sure your phone is plugged in via USB
echo 2. it should show as SPRD U2S Diag in device manager
echo 3. when you click a key the tool will wait for your phone
echo 4. turn OFF your phone completely
echo 5. hold VOLUME UP + VOLUME DOWN at the same time
echo 6. while holding both buttons plug in the USB cable
echo 7. keep holding until you see stuff happening below
echo.
echo ============================================
echo.
pause

echo.
echo [WAITING] looking for your phone... 300 second timeout
echo [HINT] if nothing happens try again make sure phone is OFF
echo.

cd tools
spd_dump.exe --wait 300 --kick exec_addr %EXEC_ADDR% fdl ..\%FDL_DIR%\fdl1-dl.bin %FDL1_ADDR% fdl ..\%FDL_DIR%\fdl2-dl.bin %FDL2_ADDR% exec erase_part persist reset

echo.
if %errorlevel% equ 0 (
    echo ============================================
    echo   DONE! FRP is gone
    echo ============================================
    echo.
    echo your phone should restart without asking
    echo for a google account
    echo.
    echo if it doesnt restart just turn it on manually
) else (
    echo ============================================
    echo   something went wrong
    echo ============================================
    echo.
    echo try this:
    echo   - make sure SPRD USB driver is installed
    echo   - try installing WinUSB driver with Zadig
    echo   - make sure phone is fully OFF
    echo   - try holding buttons longer when plugging in
    echo.
)

pause
