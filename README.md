# Prerequisites
```
sudo apt install python3 pip python3-pyaudio portaudio19-dev
pip3 install Unidecode SpeechRecognition google-cloud-texttospeech playsound pynput google-api-python-client oauth2client

patch ~/.local/lib/python3.8/site-packages/speech_recognition/ speech_recognition.patch
```

# Google API

Copy your Google API JSON key in the project folder. The key must have the name `key.json`.

# Usage
```
python3 theater_review -f <text> (-n) (-v)
```

The `<text>` value corresponds to the path to the file containing the text of the scene to review.
The `-n` option enables the narrator. The `-v` option enable the voice recognition option.

# File format

The format of the file that must be given to the `-f` option is the following:
```
=CHARACTER 1=
Text of the character 1.
=CHARACTER 2=
Text of the character 2.
=CHARACTER 1=
Reply of the character 1.
```

You can find examples in the `text` folder of this project.