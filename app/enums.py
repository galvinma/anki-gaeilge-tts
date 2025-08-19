from enum import Enum


class NoteTypes(Enum):
    CONCEPT = "concept"  # front/back, no audio
    BASIC = "basic"  # native/target, with audio
    BASIC_TYPING = "basic_typing"  # native/target, typing, with audio
    CLOZE_TYPING = "cloze_typing"  # native/target, cloze, with audio
    CLOZE_TYPING_NO_AUDIO = "cloze_typing_no_audio"  # native/target, cloze, no audio
