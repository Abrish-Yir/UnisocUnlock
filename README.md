# UnisocUnlock

free FRP bypass for unisoc phones. no paid tools no BS.

uses CVE-2022-38694 exploit to erase the persist partition and remove google account lock.

## supported chips

| chip | common devices |
|------|----------------|
| T606 (UMS9230) | realme C31/C33/C35, moto E13/G04, tecno spark 8C, itel S23, most tablets |
| T610 (UMS512) | realme C21y/C25y, moto G20 |
| T618 (UMS9620) | retroid pocket, anbernic handhelds |
| SC9863A | ZTE blade, nokia C3, itel vision 3 |
| T310 (UMS312) | qin F21 pro |

does NOT work on qualcomm mediatek exynos or tensor

## how to use

1. download this repo (code > download zip)
2. extract to C:\UnisocUnlock
3. run install_driver.bat to get the SPRD driver
4. run remove_frp.bat
5. follow instructions on screen

## entering bootrom mode

1. turn off phone completely
2. hold volume up + volume down
3. while holding plug in usb
4. keep holding until you see output

## common errors

| error | fix |
|-------|-----|
| device removed | hold buttons longer |
| handshake failed | install driver or use zadig |
| COM port appears then disappears | thats normal |

## how it works

1. connects to phone in bootrom mode
2. sends CVE-2022-38694 exploit to bypass signature check
3. loads custom FDL1/FDL2 into RAM
4. erases persist partition (where FRP lives)
5. reboots clean no google account

## credits

- TomKing062 - CVE-2022-38694 exploit and spd_dump
- NCC Group - vulnerability research
- ilyakurdyukov - spreadtrum flash protocol reverse engineering

## license

MIT do whatever you want just keep the license file
