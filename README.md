# Prerequisites
```
sudo apt install python3 pip python3-pyaudio portaudio19-dev
pip3 install Unidecode SpeechRecognition google-cloud-texttospeech playsound pynput google-api-python-client oauth2client

patch ~/.local/lib/python3.8/site-packages/speech_recognition/__init__.py speech_recognition.patch
```

# Google API

Copy your Google API JSON key in the project folder. The key must have the name `key.json`.

# Usage
```
python3 theater_review -f <text> (-n) (-v)
```

The `<text>` value corresponds to the path to the file containing the text of the scene to review.
The `-n` option enables the narrator. The `-v` option enables the voice recognition option.

If you use the voice recognition, **press the space bar** just after saying your text to send it to the API.

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

# Docker version

A Docker version is available to avoid any change on the host system. This version does not support narration and speech recognition.
To use it, you need to build the image first by running the following command in the same directory of the `Dockerfile` file:
```
docker build -t theater_review .
```
Then, you can run the application by mounting the `text` folder in the container:
```
docker run -it -v <path_to_your_text_folder>:/theater_review/text theater_review python3 theater_review.py -f text/<path_to_your_text_file>
```
For instance, using the text examples in this repository:
```
docker run -it -v ./text/:/theater_review/text theater_review python3 theater_review.py -f text/avare/2.txt
```
