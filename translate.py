import pytesseract
from PIL import ImageGrab
from deep_translator import GoogleTranslator, exceptions
import pyperclip
from tqdm import tqdm
import time
import hashlib
from colorama import Fore, Style, init
from langdetect import detect, LangDetectException

init(autoreset=True)

# Configuration
TESSERACT_PATH = r'C:\tesseract\tesseract.exe'
CHECK_INTERVAL = 2

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def get_text_from_image(image):
    """
    Extract text from a given image using OCR.
    
    Args:
        image (PIL.Image.Image): The image to process.
        
    Returns:
        str: The text extracted from the image.
    """
    try:
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        print(Fore.RED + f"Error during OCR process: {e}")
        return None

def translate_text(text, target_language='en'):
    """
    Translate the given text to the specified target language.
    
    Args:
        text (str): The text to translate.
        target_language (str): The language code for the target language (default is English).
    
    Returns:
        str: The translated text.
    """
    try:
        try:
            detected_language = detect(text)
            print(Fore.YELLOW + f"\nDetected source language: {detected_language}")
        except LangDetectException:
            print(Fore.RED + "Could not detect the language of the text.")
            detected_language = 'auto'

        translator = GoogleTranslator(source=detected_language, target=target_language)
        translated_text = translator.translate(text)

        if translated_text.strip().lower() == text.strip().lower() and detected_language != 'en':
            print(Fore.YELLOW + "Retrying translation with automatic language detection...")
            translator = GoogleTranslator(source='auto', target=target_language)
            translated_text = translator.translate(text)

        return translated_text
    except exceptions.ServerException as e:
        print(Fore.RED + f"Translation error: {e}")
        return None

def display_progress_bar(duration=1):
    """
    Display a progress bar for a given duration to simulate processing time.
    
    Args:
        duration (int): The duration in seconds for the progress bar to complete.
    """
    for _ in tqdm(range(100), desc="Processing", ncols=100, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET)):
        time.sleep(duration / 100)

def monitor_clipboard():
    """
    Monitor the clipboard for new images and process them if detected.
    """
    last_image_hash = None
    
    while True:
        image = ImageGrab.grabclipboard()
        
        if isinstance(image, ImageGrab.Image.Image):
            image_hash = hashlib.md5(image.tobytes()).hexdigest()
            
            if image_hash != last_image_hash:
                print(Fore.YELLOW + "\nNew image detected. Extracting text...")
                
                last_image_hash = image_hash
                
                text = get_text_from_image(image)
                
                if text:
                    print(Fore.GREEN + "\nExtracted Text:\n", Fore.RESET + text)
                    
                    print(Fore.YELLOW + "\nTranslating the text...")
                    display_progress_bar(duration=1)
                    
                    translated_text = translate_text(text)
                    if translated_text:
                        print(Fore.CYAN + "\nTranslated Text:\n", Fore.RESET + translated_text)
                        
                        pyperclip.copy(translated_text)
                        print(Fore.GREEN + "\nTranslated text copied to the clipboard.")
                    else:
                        print(Fore.RED + "\nFailed to translate the text.")
                else:
                    print(Fore.RED + "No text was extracted from the image.")
                
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    print(Fore.CYAN + "Monitoring the clipboard for new images. Press Ctrl+C to exit.")
    try:
        monitor_clipboard()
    except KeyboardInterrupt:
        print(Fore.RED + "\nMonitoring stopped.")
