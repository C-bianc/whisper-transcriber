# MP3 Transcriber using Whisper

This program transcribes MP3 audio files into text using the Whisper model. By default, it provides segmented transcriptions without punctuation. The program can process individual MP3 files or all MP3 files in a specified directory.

## Features:
- **Segmented Transcriptions**: By default, the transcription is split into segments without punctuation.
- **Retain Punctuation**: You can use the `--with-punct` flag to retain punctuation in the transcription.
- **Continuous Text**: Use the `--continued-text` flag to combine the transcription into a continuous block of text.
- **Directory Processing**: With the `-dir` flag, the program can process all MP3 files in a directory.
- **Save or Print Output**: The output is saved as a `.txt` file with the same name as the audio file if the `-save` parameter is given; otherwise, it prints the transcription on the console.

## Requirements:
- Python 3.x
- `openai-whisper` library

To install the required dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```
## Usage
```bash
python generate_transcr.py [filename.mp3] -save -dir input_directory --with-punct --continued-text 
```
