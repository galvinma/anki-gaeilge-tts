import logging

from app.enums import NoteTypes

logger = logging.getLogger(__name__)


def get_fields_split(row):
    """
    Parse the input file row into card content
    """
    note_type = NoteTypes(row["NoteType"])
    foreign = row["Foreign"]
    native = row["Native"]
    extra = row["Extra"]
    tags = row["Tags"]
    return note_type, foreign, native, extra, tags


def note_as_list(target, native, audio_file_name, extra, tags):
    return (
        [target, native, f"[sound:{audio_file_name}]", extra, tags]
        if audio_file_name
        else [target, native, extra, tags]
    )
