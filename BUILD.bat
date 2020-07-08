REM Running this will build the star classifier from the code
REM Pre-requisite, you will need Python and Pip command set in the PATH variable

SET directory_name=Star-Classifier-v0.96

mkdir python-build-venv
python -m venv ./python-build-venv
CALL .\python-build-venv\Scripts\activate
pip install pillow
pip install pyautogui
pip install mss
pip install pypiwin32
pip install pynput
pip install tensorflow
pip install keras
pip install pyinstaller
pyinstaller __init__.py --windowed
rmdir /Q /S build
move dist/__init__ %foo%
rmdir /Q /S dist
mkdir %foo%\images
mkdir %foo%\routes
mkdir %foo%\models
Xcopy /E /I images %foo%\images
Xcopy /E /I routes %foo%\routes
Xcopy /E /I models %foo%\models
move %foo%\__init__.exe %foo%\Star-Classifier.exe

rmdir /Q /S python-build-venv