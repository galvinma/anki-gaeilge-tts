# Anki Gaeilge TTS

A semi-automated workflow for bulk upload of Gaeilge TTS Anki cards.

1. Manually curate an input file of Gaeilge content.
2. Execute the script to fetch audio files and generate anki spreadsheet.
3. Use the bulk import functionality in anki to add notes to a deck.

# Configuration

Place a file called .env in the root of the repo with the following variables:

```
OUTPUT_PATH=demo/output # Path the output spreadsheet for bulk anki upload.
AUDIO_PATH=demo/audio # Path to anki media collection.
DOWNLOAD_PATH=demo/download # Path to dir where browser will download audio.
```

# Usage

```
python -m venv .ve && \
source .ve/bin/activate && \
pip install -r requirements.txt && \
python -m app.main \
    --input_file demo/input/gaeilge.txt
```

## Sample input file

```
NoteType|Foreign|Native|Extra|Tags
basic_typing|Cá bhfuil tú i do chónaí ?|Where are you living?||Phrase
cloze_typing|Feicim madra i {{c1::bpáirc}}.|I see a dog in a park.|b eclipses p when preceded by i|Eclipsis
```

# TTS

This app leverages Trinity College Dublin's [ABAIR](https://www.abair.tcd.ie/ga/synthesis) TTS.
