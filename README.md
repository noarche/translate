
![translate](https://github.com/user-attachments/assets/1c666adc-7c38-4549-b7c3-9ad5f09d8ad0)


# translate
Translate to english locally, fast and easily. 

This script monitors your clipboard for images and automatically translates them to English 100% locally on your machine.

You will need a software to take screenshots of parts of the screen that automatically copies to clip board.

Run the script and after taking a screen capture check the console for the translated text.

In most screen capture software settings this is an option instead of saving every file.


# How to use

Download Tesseract from the link below and when installing select all the extra options to download. It should be 800mb-900mb installation size.


https://github.com/UB-Mannheim/tesseract/wiki


Update the install path on line 10 of the script.


pip install pytesseract Pillow googletrans==4.0.0-rc1 deep-translator pyperclip tqdm colorama


Run the script
