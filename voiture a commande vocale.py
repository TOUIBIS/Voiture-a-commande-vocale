import pyaudio
import wave
from watson_developer_cloud import SpeechToTextV1
from os.path import join, dirname
import json
from StringIO import StringIO
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 
Moteur1A = 3      ## premiere sortie du premier moteur, pin 16
Moteur1B = 5      ## deuxieme sortie de premier moteur, pin 18
Moteur1E = 8      ## enable du premier moteur, pin 22

Moteur2A = 40      ## premiere sortie du deuxieme moteur, pin 16
Moteur2B = 38      ## deuxieme sortie de deuxieme moteur, pin 18
Moteur2E = 36      ## enable du deuxieme moteur, pin 22

GPIO.setup(Moteur1A,GPIO.OUT)  ## ces 6 pins du Raspberry Pi sont des sorties
GPIO.setup(Moteur1B,GPIO.OUT)
GPIO.setup(Moteur1E,GPIO.OUT)
GPIO.setup(Moteur2A,GPIO.OUT) 
GPIO.setup(Moteur2B,GPIO.OUT)
GPIO.setup(Moteur2E,GPIO.OUT)

def avant ():
    print "Marche avnat"
    GPIO.output(Moteur1A,GPIO.HIGH)
    GPIO.output(Moteur1B,GPIO.LOW)
    GPIO.output(Moteur1E,GPIO.HIGH)
def arierre():
    print ("Marche arierre")
    GPIO.output(Moteur1A,GPIO.LOW)
    GPIO.output(Moteur1B,GPIO.HIGH)
    GPIO.output(Moteur1E,GPIO.HIGH)
    
def droite ():
    print ("Direction Droite")
    GPIO.output(Moteur2A,GPIO.LOW)
    GPIO.output(Moteur2B,GPIO.HIGH)
    GPIO.output(Moteur2E,GPIO.HIGH)
def stopper ():
    print ("Arret des moteurs")
    GPIO.output(Moteur1E,GPIO.LOW)
    GPIO.output(Moteur2E,GPIO.LOW)
    
def gauche ():
    print ("Direction Gauche")
    GPIO.output(Moteur2A,GPIO.HIGH)
    GPIO.output(Moteur2B,GPIO.LOW)
    GPIO.output(Moteur2E,GPIO.HIGH)



form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 3 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = 'test.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans,input_device_index = dev_index,input = True,frames_per_buffer=chunk)
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for ii in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()


#*********************************************************************



speech_to_text = SpeechToTextV1(
    iam_apikey='mXk-pC-SDBAwPxf-ZxxVjIZB_YmcQ3wctGqMKewji57m',
    url='https://gateway-syd.watsonplatform.net/speech-to-text/api'
)

files = ['test.wav']
for file in files:
    with open(join(dirname(__file__), '/home/pi', file),
                   'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/wav',
            timestamps=True,
            word_alternatives_threshold=0.9,
            keywords=['go', 'back','hello'],
            keywords_threshold=0.5
        ).get_result()
    x= str(json.dumps(speech_recognition_results['results'][0]['alternatives'][0]['transcript']))
print(x)    	

#***********************************************************************



cmd = input ("donner une commande\n")
while (True):
    if cmd== avant:
		avant()
		cmd = input ("donner une commande\n")
    elif cmd == arierre:    
        arierre()
        cmd = input ("donner une commande\n")
    elif cmd == 'avant droite':    
        avant()
        droite()
        cmd = input ("donner une commande\n")
    elif cmd== avantgauche:    
        avant()
        gauche()
        cmd = input ("donner une commande\n")
    elif cmd == arierredroite:
        arierre()
        droite()
        cmd = input ("donner une commande\n")
    elif cmd == arierregauche:
        arierre()
        gauche()
        cmd = input ("donner une commande\n")
    elif cmd == stop:
        stopper()
        cmd = input ("donner une commande\n")
    elif cmd == stopp:
        break
    else:
        cmd = input ("donner une commande\n")
        
GPIO.cleanup()
