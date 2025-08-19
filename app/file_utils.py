import logging
from hashlib import md5
from pathlib import Path

import pandas as pd

from app.static import AUDIO_PATH

logger = logging.getLogger(__name__)


def write_audio_content(text, audio_content, audio_path, file_name=None):
    if file_name is None:
        file_name = get_hash(text)

    file_path = Path(f"{audio_path}/{file_name}.mp3")
    with open(file_path, "wb") as out:
        out.write(audio_content)
        logger.info(f"Audio content written to {file_path}")

    return file_path


def check_cache(file_name):
    for ext in ["wav", "mp3"]:
        file_path = AUDIO_PATH / f"{file_name}.{ext}"
        if file_path.exists():
            return Path(file_path)


def write_df(df, path, index=True, header=True, sep=","):
    df.to_csv(path, index=index, header=header, sep=sep)


def read_df(path, index_col=None):
    return pd.read_csv(path) if index_col is None else pd.read_csv(path, index_col=index_col)


def get_hash(text):
    return md5(text.encode("utf-8")).hexdigest()
