import pytesseract
from PIL import ImageGrab
from deep_translator import GoogleTranslator
import pyperclip
from tqdm import tqdm
import time
import hashlib

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
        print(f"Error during OCR process: {e}")
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
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def display_progress_bar(duration=1):
    """
    Display a progress bar for a given duration to simulate processing time.
    
    Args:
        duration (int): The duration in seconds for the progress bar to complete.
    """
    for _ in tqdm(range(100), desc="Processing", ncols=100):
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
                print("\nNew image detected. Extracting text...")
                
                last_image_hash = image_hash
                
                text = get_text_from_image(image)
                
                if text:
                    print("\nExtracted Text:\n", text)
                    
                    print("\nTranslating the text...")
                    display_progress_bar(duration=1)
                    
                    translated_text = translate_text(text)
                    if translated_text:
                        print("\nTranslated Text:\n", translated_text)
                        
                        pyperclip.copy(translated_text)
                        print("\nTranslated text copied to the clipboard.")
                    else:
                        print("\nFailed to translate the text.")
                else:
                    print("No text was extracted from the image.")
                
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    print("Monitoring the clipboard for new images. Press Ctrl+C to exit.")
    try:
        monitor_clipboard()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
