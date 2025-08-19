import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


# URLS
TTS_URL = "https://www.abair.tcd.ie/ga/synthesis"
GA_MP3_URL = "https://www.teanglann.ie/CanC/{text}.mp3"

# PATHS
OUTPUT_PATH = Path(os.environ["OUTPUT_PATH"])
DOWNLOAD_PATH = Path(os.environ["DOWNLOAD_PATH"])
AUDIO_PATH = Path(os.environ["AUDIO_PATH"])

# ETC
DELIMITER = "|"
PUNCTUATION = [".", "?", "!"]
STRIP_TOKENS = ["▪"]
