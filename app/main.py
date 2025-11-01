"""
python -m app.main \
    --input_file gaeilge.txt

---

This script takes a pipe delimited input file and creates a spreadsheet for bulk load into Anki.
"""

import argparse
import logging
from collections import defaultdict

import pandas as pd

from app.anki import get_fields_split, note_as_list
from app.enums import NoteTypes
from app.file_utils import write_df
from app.scrape import handle_audio
from app.static import AUDIO_PATH, DELIMITER, OUTPUT_PATH

logger = logging.getLogger(__name__)


def run(args):
    logger.info("Starting anki card creation...")
    logger.info(f"{OUTPUT_PATH=}")
    logger.info(f"{AUDIO_PATH=}")

    notes = defaultdict(list)
    errors = []
    df = pd.read_csv(args.input_file, delimiter=DELIMITER)
    for _, row in df.iterrows():
        if row.empty or row["NoteType"][0] == "#":
            continue

        try:
            logger.info(f"Processing: {row['Foreign']}")
            note_type, foreign, native, extra, tags = get_fields_split(row)
            audio_file_name = (
                handle_audio(note_type, foreign)
                if note_type in [NoteTypes.BASIC, NoteTypes.BASIC_TYPING, NoteTypes.CLOZE_TYPING]
                else ""
            )
            notes[note_type].append(note_as_list(foreign, native, audio_file_name, extra, tags))
        except Exception:
            logger.exception(f"Exception thrown processing {row=}")
            errors.append(row)

    for note_type, note_list in notes.items():
        df = pd.DataFrame(data=note_list)
        path = OUTPUT_PATH / f"{note_type.name}.txt"
        write_df(df=df, path=path, index=False, header=False, sep=DELIMITER)

    if errors:
        logger.warning("The following lines threw an exception...")
        for err in errors:
            logger.warning(err)

    logger.info("Done!")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Path to anki card inputs.", required=True)
    args = parser.parse_args()
    run(args)
