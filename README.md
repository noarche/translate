
![translate](https://github.com/user-attachments/assets/1c666adc-7c38-4549-b7c3-9ad5f09d8ad0)


# translate
Translate to english locally, fast and easily. 

This script monitors your clipboard for images and automatically translates them to English 100% locally on your machine.

You will need a software to take screenshots of parts of the screen that automatically copies to clip board.

Run the script and after taking a screen capture check the console for the translated text.

In most screen capture software settings this is an option instead of saving every file.


# How to use

Get Translate Local Script

Download Tesseract from the link below and when installing select all the extra options to download. It should be 800mb-900mb installation size.


https://github.com/UB-Mannheim/tesseract/wiki


Update the install path on line 31 of the script.


Download LLM Model mBart50 from huggingface. It should be ~2.5GB. Use bin for CPU and Safetensors for CUDA. Save in './facebook/mbart-large-50-many-to-many-mmt/'


https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt/tree/main


Update the install path on line 32 of the script.


pip install pytesseract Pillow transformers torch sentencepiece pyperclip tqdm colorama langdetect
