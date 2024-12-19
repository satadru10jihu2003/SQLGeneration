import sounddevice as sd
import numpy as np
import wave
from openai import OpenAI
import psycopg2
import os
import requests

duration = 5
sample_rate = 44100
channels = 1

print ("Recording ...")
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype = np.int16)
sd.wait()
print("Recording completed.")

filename = "output.wav"
with wave.open(filename, 'w') as waveFile:
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(2)
    waveFile.setframerate(sample_rate)
    waveFile.writeframes(audio_data.tobytes())
    waveFile.close()

print("Audio saved")

# make a restapi post call here with filename as the audio file
url = 'http://localhost:8001/process-audio' 

# Make a POST request with the file
with open(filename, 'rb') as f:
    files = {'file': (filename, f)}
    response = requests.post(url, files=files)

# Check the response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error making api call: {response.status_code}")

if os.path.exists(filename):
        os.remove(filename)

        