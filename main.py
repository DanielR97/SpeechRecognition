import speech_recognition as sr
import subprocess
import os


# Language selector
languages = {
    '1': 'es-ES',
    '2': 'en-US'
}

# Topics I'd like to find in the audio transcription
keywords = []
keywordToAdd = ""
print("¿Qué temas quieres buscar en la grabación?\nIntroduce - para borrar el tema anterior y . para terminar")
while keywordToAdd != ".":
    keywordToAdd = input()
    if (keywordToAdd == "-") and (len(keywords) > 0):
        print(("{} ha sido borrado").format(keywords[-1]))
        keywords.pop()
    elif (keywordToAdd != ".") and (keywordToAdd != ""):
        if keywordToAdd in keywords:
            print("Este tema ya fue añadido anteriormente")
        else:
            keywords.append(keywordToAdd.lower())
            print("Tema añadido")
    elif keywordToAdd == "":
        pass
        
        


languageSelected = None
while languageSelected == None:
    languageSelected = languages.get(
        input("Elige el idioma del audio:\n1) Español\n2) Inglés\nSelección: "))


# Convert the audio to WAV and ignore ffmpeg output
audioFileInput = 'media/canarias-corto.mp3'

if audioFileInput.endswith('.wav'):
    audioFileOutput = audioFileInput
    converted = False
else:
    print('Convirtiendo audio...')
    FNULL = open(os.devnull, 'w')
    subprocess.call(['ffmpeg', '-y', '-i', audioFileInput,
                     'media/prueba.wav'], stdout=FNULL, stderr=subprocess.STDOUT)
    audioFileOutput = 'media/prueba.wav'
    converted = True
    print('Audio convertido!')


r = sr.Recognizer()
file = sr.AudioFile(audioFileOutput)


# Retrieve audio duration
test = str(subprocess.check_output(['ffmpeg', '-hide_banner', '-y', '-i', audioFileOutput,
                                    '-f', 'null', '-'], stderr=subprocess.STDOUT))
searchIndex = test.find('Duration')
hours = test[searchIndex+10:searchIndex+12]
minutes = test[searchIndex+13:searchIndex+15]
seconds = test[searchIndex+16:searchIndex+21]
totalDurationInSeconds = int(hours * 3600) + int(minutes * 60) + float(seconds)
print(('Duración: {}').format(test[searchIndex+10:searchIndex+21]))


# Listen to the audio and recognize voice
with file as source:
    transcripted = 0.00
    secondsToRecord = 4
    text = ""
    moments = False
    print(('Se van a buscar las siguientes palabras en la grabación indicada: {}').format(', '.join(keywords)))
    print('Transcribiendo...')
    while transcripted < totalDurationInSeconds:
        audio = r.record(source, duration=secondsToRecord, offset=transcripted)
        try:
            text += (r.recognize_google(audio, language=languageSelected)).lower()
            if any(ext in text for ext in keywords):
                print('En el segundo {} están hablando de un tema de interés: "{}"\n'.format(int(transcripted),text))
                text = ""
                moments = True
            transcripted += secondsToRecord
        except:
            print("Segundos {}-{}: Fallo al transcribir esta parte del audio\n".format(int(transcripted),int(transcripted+secondsToRecord)))
            text = ""
            transcripted += secondsToRecord

    print('Transcripción finalizada!')


if text != "":
    print(text)

if moments:
    pass
else:
    print("No han hablado de ningún tema de interés")


# Remove converted file
if converted:
    os.remove(audioFileOutput)
