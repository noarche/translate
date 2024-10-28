import pytesseract
from PIL import ImageGrab, Image
import pyperclip
from tqdm import tqdm
import time
import hashlib
from colorama import Fore, Style, init
from langdetect import detect, LangDetectException
import threading
import logging
from transformers import MBartForConditionalGeneration, MBart50Tokenizer
import torch
import argparse
import sys


init(autoreset=True)


parser = argparse.ArgumentParser(description="Clipboard Translator Script")
parser.add_argument('-debug', action='store_true', help="Enable debug messages")
args = parser.parse_args()


logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)


logging.getLogger("PIL").setLevel(logging.WARNING)


MODEL_PATH = "F:/Code/python/translate/facebook/mbart-large-50-many-to-one-mmt"
TESSERACT_PATH = r'C:\tesseract\tesseract.exe'
CHECK_INTERVAL = 2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def get_text_from_image(image):
    """
    Extract text from a given image using OCR.
    """
    try:
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text.strip()
    except Exception as e:
        logging.error(f"Error during OCR process: {e}")
        return None

def load_mbart50_model():
    """
    Load the mBART50 model and tokenizer for multilingual translation from a local path.
    """
    tokenizer = MBart50Tokenizer.from_pretrained(MODEL_PATH)
    model = MBartForConditionalGeneration.from_pretrained(MODEL_PATH).to(DEVICE)
    return model, tokenizer

def translate_with_mbart50(text, source_language, model, tokenizer):
    """
    Translate the given text using the mBART50 model.
    """

    tokenizer.src_lang = source_language


    encoded_text = tokenizer(text, return_tensors="pt", padding=True).to(DEVICE)


    generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])


    translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    return translated_text

def display_progress_bar(duration=1):
    """
    Display a progress bar for a given duration to simulate processing time.
    """
    for _ in tqdm(range(100), desc="Processing", ncols=100, bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.CYAN, Fore.RESET), leave=True):
        time.sleep(duration / 100)

def perform_translation(text, model, tokenizer):
    """
    Perform the translation in a separate thread to avoid blocking.
    """
    try:

        source_lang = detect(text)
        source_lang_code = f"{source_lang}_XX"
        logging.info(f"Detected source language: {source_lang}")


        translated_text = translate_with_mbart50(text, source_lang_code, model, tokenizer)

        print(Fore.CYAN + "\nTranslated Text:\n", Fore.RESET + translated_text)
    except LangDetectException:
        print(Fore.RED + "Could not detect the language of the text.")
    except Exception as e:
        logging.error(f"Failed to translate the text: {e}")
        print(Fore.RED + "\nFailed to translate the text.")

def monitor_clipboard(model, tokenizer):
    """
    Monitor the clipboard for new images or text and process them if detected.
    """
    last_data_hash = None

    while True:

        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            image_hash = hashlib.md5(image.tobytes()).hexdigest()

            if image_hash != last_data_hash:
                logging.info("New image detected. Extracting text...")
                last_data_hash = image_hash

                text = get_text_from_image(image)
                if text:
                    print(Fore.GREEN + "\nExtracted Text:\n", Fore.RESET + text)

                    print(Fore.YELLOW + "\nTranslating the text...")
                    display_progress_bar(duration=1)


                    translation_thread = threading.Thread(target=perform_translation, args=(text, model, tokenizer))
                    translation_thread.start()
                else:
                    print(Fore.RED + "No text was extracted from the image.")
        else:

            clipboard_text = pyperclip.paste()
            if clipboard_text:
                text_hash = hashlib.md5(clipboard_text.encode()).hexdigest()
                if text_hash != last_data_hash:
                    logging.info("New text detected in clipboard.")
                    last_data_hash = text_hash

                    print(Fore.YELLOW + "\nTranslating the text...")
                    display_progress_bar(duration=1)


                    translation_thread = threading.Thread(target=perform_translation, args=(clipboard_text, model, tokenizer))
                    translation_thread.start()

        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    print(Fore.CYAN + "Monitoring the clipboard for new images or text. Press Ctrl+C to exit.")

    model, tokenizer = load_mbart50_model()
    try:
        monitor_clipboard(model, tokenizer)
    except KeyboardInterrupt:
        print(Fore.RED + "\nMonitoring stopped.")
