@echo off
setlocal enabledelayedexpansion
set count=100
for %%f in (*.mp3) do (
    set "oldname=%%f"
    set "newname=000!count!.mp3"
    set "newname=!newname:~-7!"
    ren "!oldname!" "!newname!"
    set /a count+=1
)
