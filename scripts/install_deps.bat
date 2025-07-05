@echo off
echo Installing Python dependencies...
pip install pyautogui
pip install pytesseract
pip install Pillow
echo.
echo Dependencies installed!
echo.
echo NOTE: You also need to install Tesseract OCR software
echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
echo Install to: C:\Program Files\Tesseract-OCR\
echo.
pause