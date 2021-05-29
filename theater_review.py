#!/usr/bin/python3

import string;
import difflib;
import unidecode;
import pathlib;
import speech_recognition as sr;
import json;
import os;
import re;
import getopt;
import sys;

from google.cloud import texttospeech;
from playsound import playsound;

def to_list(sentence):
    original = [];
    processed = [];

    current_original = "";
    current_processed = "";

    for char, next_char in zip(sentence, list(sentence[1:]) + [None]):
        current_original += str(char);
        is_char = lambda x: x and x not in string.punctuation and x not in string.whitespace;
        if(is_char(char)):
            current_processed += str(char);
        if(not(is_char(char)) and is_char(next_char) and current_processed or not(next_char)):
            original.append(current_original);
            processed.append(unidecode.unidecode(current_processed.lower()));
            current_original = "";
            current_processed = "";

    return (original, processed);

def load(filename):
    characters = set();
    text = [];

    with open(filename) as file_handle:
        content = file_handle.readlines();

        current_character = "";
        current_text = "";

        for line in content:
            line = line.strip();
            if(line[0] == '=' and line[-1] == '='):
                if(current_character and current_text):
                    text.append((current_character, current_text));
                    current_text = "";
                current_character = line[1:-1];
                characters.add(current_character);
            else:
                current_text += "\n" + line;

        if(current_character and current_text):
            text.append((current_character, current_text));

    return (characters, text);

def select_character(characters):
    selected_character = "";

    while not(selected_character):
        print("Quel personnage souhaitez-vous interpréter ?");
        for idx in range(len(characters)):
            print(str(idx+1) + " - " + list(characters)[idx]);
        selected_idx = input("> ");

        try:
            selected_character = list(characters)[int(selected_idx)-1];
        except ValueError:
            print("Veuillez saisir un nombre entier");
        except IndexError:
            print("Veuillez saisir un nombre entre 1 et " + str(len(characters)));

    return selected_character;

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(pathlib.Path().absolute() / "key.json");

voice_params = texttospeech.VoiceSelectionParams(language_code='fr-FR');
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16);
client = texttospeech.TextToSpeechClient();

def read_text(text):
    text_input = texttospeech.SynthesisInput(text=text);
    response = client.synthesize_speech(input=text_input, voice=voice_params, audio_config=audio_config);
    filename = '/tmp/' + str(hash(text)) + '.wav';
    with open(filename, "wb") as out:
        out.write(response.audio_content)
    playsound(filename);
    os.remove(filename);

def get_n_grams(text):
    n_grams = set();
    text = text.strip();
    text = re.sub("\n", '', text);
    for part in re.split("[.!?:,;\"]", text):
        part = part.strip();
        if not(part):
            continue;
        punct = re.sub("['-]", '', string.punctuation);
        part = re.sub("[" + punct + "]", '', part);
        words = part.split(' ');
        for idx in range(len(words)):
            n_grams.add(words[idx]);
            if idx+1 < len(words):
                n_grams.add(' '.join(words[idx:idx+2]));
                if idx+2 < len(words):
                    n_grams.add(' '.join(words[idx:idx+3]));
    return list(n_grams);

narrator=False;
voice_recognition=False;
text_file='';

opts, args = getopt.getopt(sys.argv[1:], "nvf:");

for o, a in opts:
    if o == '-n':
        narrator=True;
    elif o == '-v':
        voice_recognition=True;
    elif o == '-f':
        text_file = a;

credentials = '';

with open('key.json', 'r') as f:
    credentials = f.read().replace('\n', '');

r = sr.Recognizer();
r.operation_timeout = 120;

mic = sr.Microphone();

characters, text = load(text_file);
reviewer = select_character(characters);

for sentence in text:
    if(sentence[0] == reviewer):
        with mic as source:
            if voice_recognition:
                print(reviewer + ' > ', end='', flush=True);
                audio = r.record(source);
                print('... ', end='', flush=True);
                preferred_phrases = get_n_grams(sentence[1]);
                guess = r.recognize_google_cloud(audio, language='fr-FR', credentials_json=credentials, preferred_phrases=preferred_phrases);
                print(guess);
            else:
                guess = input(reviewer + ' > ');

            solution_list = to_list(sentence[1]);
            guess_list = to_list(guess);
            seqmatch = difflib.SequenceMatcher(None, solution_list[1], guess_list[1]);
    
            for opcode in seqmatch.get_opcodes():
                if(opcode[0] == 'equal'):
                    print('\033[92m' + ''.join(guess_list[0][opcode[3]:opcode[4]]) + '\033[0m', end='');
                elif(opcode[0] == 'insert'):
                    print('\033[91m\033[9m' + ''.join(guess_list[0][opcode[3]:opcode[4]]) + '\033[0m', end='');
                elif(opcode[0] == 'delete'):
                    print('\033[91m' + ''.join(solution_list[0][opcode[1]:opcode[2]]) + '\033[0m', end='');
                else:
                    print('\033[91m\033[9m' + ''.join(guess_list[0][opcode[3]:opcode[4]]) + '\033[29m' + ''.join(solution_list[0][opcode[1]:opcode[2]])  + '\033[0m', end='');
            print();
    else:
        print(sentence[0] + ' > ' + sentence[1]);
        if narrator:
            read_text(sentence[1]);

