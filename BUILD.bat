REM Running this will build the star classifier from the code
REM Pre-requisite, you will need Python 3.5 to 3.7 and Pip command set in the PATH variable

SET directory_name=Star-Classifier-v0.96

mkdir python-build-venv
python -m venv ./python-build-venv
CALL .\python-build-venv\Scripts\activate
pip install wheel
pip install pillow
pip install pyautogui
pip install mss
pip install pypiwin32
pip install pynput
pip install tensorflow==1.14
pip install keras==2.2.5
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
pyinstaller  --windowed --icon=images\icon-ico.ico __init__.py
del __init__.spec
rmdir /Q /S build
rmdir /Q /S %directory_name% REM delete any previously created builds with same name
move dist/__init__ %directory_name%
rmdir /Q /S dist
mkdir %directory_name%\images
mkdir %directory_name%\routes
mkdir %directory_name%\models
Xcopy /E /I images %directory_name%\images
Xcopy /E /I routes %directory_name%\routes
Xcopy /E /I models %directory_name%\models
move %directory_name%\__init__.exe %directory_name%\Star-Classifier.exe

rmdir /Q /S python-build-venv