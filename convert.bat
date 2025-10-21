SETLOCAL
del /Q output\*.*

::Random resolution
CALL :RandomFloat "0.90", "1.10", RAND_RESOLUTION

::Random volume
CALL :RandomFloat "0.90", "1.10", RAND_VOLUME

::Random gamma. The value must be a float in range 0.1 to 10.0. The default value is "1".
CALL :RandomFloat "0.90", "1.10", RAND_GAMMA

::Random saturation. The value must be a float in range 0.0 to 3.0. The default value is "1".
CALL :RandomFloat "0.90", "1.10", RAND_SATURATION

::Random brightness. The value must be a float value in range -1.0 to 1.0. The default value is "0".
CALL :RandomFloat "0.00", "0.10", RAND_BRIGHTNESS

echo "RAND_RESOLUTION: %RAND_RESOLUTION%, RAND_VOLUME: %RAND_VOLUME%, RAND_GAMMA: %RAND_GAMMA%, RAND_SATURATION: %RAND_SATURATION%, RAND_BRIGHTNESS: %RAND_BRIGHTNESS%"

for %%f in (input\*) do (
    ffmpeg -i "%%f" -vf scale="ceil(iw*%RAND_RESOLUTION%/2)*2:ceil(ih*%RAND_RESOLUTION%/2)*2" -af "volume=%RAND_VOLUME%" -vf eq=gamma=%RAND_GAMMA%:saturation=%RAND_SATURATION%:brightness=%RAND_BRIGHTNESS% "output/%%~nf.mp4"
)

EXIT /B 0

:RandomFloat
SET MIN=%~1
SET MAX=%~2
for /f "delims=" %%a in ('powershell -Command "((%MAX%-%MIN%)*%RANDOM%/32768 + %MIN%)"') do set result=%%a
SET result=%result:,=.%
SET "%~3=%result%"
EXIT /B 0