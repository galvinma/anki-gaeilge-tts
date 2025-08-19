import glob
import logging
import os
import time
from pathlib import Path
from sys import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from app.enums import NoteTypes
from app.file_utils import check_cache, get_hash
from app.static import AUDIO_PATH, DOWNLOAD_PATH, PUNCTUATION, TTS_URL

logger = logging.getLogger(__name__)


def handle_audio(note_type, text):
    clean_text = tts_prep(note_type, text)
    hash = get_hash(clean_text)
    audio_file_path = check_cache(hash) if check_cache(hash) else get_ga_audio(clean_text)
    return audio_file_path.name


def get_ga_audio(text):
    logger.info(f"Getting audio for {text=}.")

    file_name = get_hash(text)
    return get_abair_audio(text, get_driver(), AUDIO_PATH / f"{file_name}.wav")


def get_abair_audio(text, driver, file_path):
    logger.info(f"Trying {TTS_URL} ...")
    logger.info(f"Target path is {file_path=}")
    audio_path = None

    # For some reason abair likes punctuation at the end of the input, even for \
    # incomplete sentences. Without a '.' the audio is often cutoff.
    if not text[-1] in PUNCTUATION:
        text = text + "."

    with driver as driver:
        try:
            driver.implicitly_wait(10)
            driver.get(TTS_URL)

            text_area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
            text_area.send_keys(text)
            time.sleep(2)

            synthesis_buttons = driver.find_elements(By.CSS_SELECTOR, "button[class*='synthesis']")
            record_btn = synthesis_buttons[-1]
            record_btn.click()
            time.sleep(2)

            sleep_count = 7
            while sleep_count >= 0:
                time.sleep(1)
                audio_el = driver.find_element(By.TAG_NAME, "audio")
                audio_src = audio_el.get_attribute("src")
                sleep_count -= 1

            old_files = glob.glob(str(DOWNLOAD_PATH / "*"))
            driver.execute_script(f"window.open('{audio_src}')")
            download_count = 10
            while download_count >= 0:
                logger.info(f"Waiting for file {download_count=}")
                time.sleep(1)
                current_files = glob.glob(str(DOWNLOAD_PATH / "*"))
                difference = set(current_files).difference(set(old_files))
                if difference:
                    download_file_name = difference.pop()
                    if ".part" not in download_file_name:
                        break

                download_count -= 1

            logger.info(f"Found {download_file_name=}")

            download_path = DOWNLOAD_PATH / download_file_name
            logger.info(f"Moving {download_path} to {file_path}.")
            os.system(f"mv '{str(download_path)}' '{str(file_path)}'")
            audio_path = Path(file_path)
        except Exception as e:
            logger.exception("Exception thrown creating audio file...")
            raise e
        finally:
            driver.close()
    return audio_path


def tts_prep(note_type, text):
    if note_type in [NoteTypes.CLOZE_TYPING, NoteTypes.CLOZE_TYPING_NO_AUDIO]:
        if "{{" not in text or "}}" not in text or "::" not in text:
            logging.error(f"{text=}")
            raise Exception("Found cloze card type without curly bracket!")

        if "{" in text:
            text = text.replace("{", "")

        if "}" in text:
            text = text.replace("}", "")

        for i in range(100):
            if f"c{i}::" in text:  # noqa E701
                text = text.replace(f"c{i}::", "")  # noqa E231

        for i in range(100):
            if f"c{i}:" in text:  # noqa E701
                text = text.replace(f"c{i}:", "")  # noqa E701

    return text


def get_driver():
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", str(DOWNLOAD_PATH))
    if platform == "linux" or platform == "linux2":
        geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
        driver_service = Service(executable_path=geckodriver_path)
        driver = webdriver.Firefox(options=options, service=driver_service)
    elif platform == "darwin":
        driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(10)
    return driver
