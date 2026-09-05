# how to contribute

thanks for wanting to help

## add device support

if you have a phone that isnt supported yet

1. get the .pac firmware for your phone
2. extract FDL1 and FDL2 files
3. figure out the exec_addr for your chip
4. put the files in exploit/your_chipset/
5. make a pull request

## test on your phone

if you used this on a phone thats not in the list

- open an issue with your phone model and chip
- include any errors you got
- note what android version youre on

## find your chip

1. go to settings > about phone
2. look for processor or SoC
3. if it says unisoc/spreadtrum T6xx or UMSxxxx you're good
4. if it says qualcomm mediatek exynos or tensor this wont work

## exec addresses by chip

| chip | exec_addr |
|------|-----------|
| UMS9230 | 0x65015f08 |
| UMS512 | 0x3EE8 |
| UMS9620 | 0x65012F48 |
| SC9863A | 0x4EE8 |
| UMS312 | 0x3EE8 |
| UDX710 | 0x3F28 |

## code style

- python: follow PEP 8 i guess
- batch files: just make it work lol
- comments: explain why not what

## license

by contributing you agree your stuff will be under MIT license
