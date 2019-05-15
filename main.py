import speech_recognition as sr
import subprocess
import os


# Language selector
languages = {
    '1': 'es-ES',
    '2': 'en-US'
}

languageSelected = None
while languageSelected == None:
    languageSelected = languages.get(input("Elige un idioma:\n1) Español\n2) Inglés\nSelección: "))


# Convert the audio to WAV and ignore ffmpeg output
audioFileInput = 'media/fallin.mp3'

if audioFileInput.endswith('.wav'):
    audioFileOutput = audioFileInput
else:
    print('Convirtiendo audio...')
    FNULL = open(os.devnull, 'w')
    subprocess.call(['ffmpeg', '-y', '-i', audioFileInput,
                    'media/prueba.wav'], stdout=FNULL, stderr=subprocess.STDOUT)
    audioFileOutput = 'media/prueba.wav'
    print('Audio convertido!')
r = sr.Recognizer()
file = sr.AudioFile(audioFileOutput)


# Listen to the audio and recognize voice
with file as source:
    audio = r.listen(source)
    try:
        print('Transcribiendo audio...')
        text = r.recognize_google(audio, language=languageSelected)
        print('Audio transcrito con éxito!')
        result = "Transcripción: {}".format(text)
    except:
        result = "No se ha podido transcribir el audio"

print(result)
