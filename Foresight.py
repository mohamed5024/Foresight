#Foresight project for MakeUofT 2020
#Developed by Mohamed Mahmoud, Ahmed Kagzi and Amanjot Gulshi
#February 15-16, 2020

#MAKE SURE Google CLoud PATH is set to json credentials file location/working directory
#Download libraries (pip install) google cloud, opencv 
from google.cloud import vision
from google.cloud.vision import types
import serial
import math
import array
import cv2
import time
import io
import os

#Use CV2 Library to connect to system default camera and set the capture range
#Starts timer for frame capture
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)
img_counter = 0
frame_set = []
start_time = time.time()

#initialize google cloud text to speech client API connection
from google.cloud import texttospeech
client_speech = texttospeech.TextToSpeechClient()

#Using the serial port to connect to ultrasonic sensory data for distance values
ard = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_7533432393535181B1A0-if00',9600)

#repeats while camera is running
while True:

    #Using the cv2 library, read in the frame
    ret, frame = capture.read()
    rgb = cv2.cvtColor(frame, 1)
    cv2.imshow('frame', rgb)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #Wait for 5 seconds to take snapshot to be sent to the API
    if time.time() - start_time >= 5: #<---- Check if 5 sec passed
        img_name = "opencv_frame_{}.png".format(1)
        cv2.imwrite(img_name, frame)
        
        #Print out that the frame shot has been taken and written to the file (or overwrites the old one if already exists)
        #to the working directory as a png file to be used in google client connection
        print("{} written.".format(img_counter))
        file_name = os.path.join(
            os.path.dirname(__file__),
            'opencv_frame_1.png')

        #setting the content to the png file just created
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        #intialize the google cloud vision client API connection and passing the snapshot photo
        client_vision = vision.ImageAnnotatorClient()
        image = vision.types.Image(content=content)

        #Receiving response from the API and only pulling the object annotations method (only method from the class we need)
        objects = client_vision.object_localization(image=image).localized_object_annotations
        print('Number of objects found: {}'.format(len(objects)))
        x=[]

        #loop through all objects found from the vision API response and print out metadata
        for object_ in objects:
            distance = 0
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            
            #Use the serial communication to get the distance value from the sensors
            distance = ard.readline().decode().strip()
            print(distance)
            
            #We will only take the objects that are of use to the user such as Person, Chair etc... 
            #and if the confidence interval (score) from the API returns a number above a threshold
            if object_.name == (r'Person') and object_.score > 0.6:
                
                #Build a string with how far the object is from the user to be sent to API
                speech = "Ahmed, there is a person %s metres in front of you!" % str(int(distance)/100)
                
                #Send the speech string to the google text-to-speech API
                #Sets language and gender of the audio file voice
                #Sets encoding to MP3 type
                synthesis_input = texttospeech.types.SynthesisInput(text=speech)
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                
                #Calls the client speech API
                response = client_speech.synthesize_speech(synthesis_input, voice, audio_config)
                
                #Uses reponse to write the mp3 to a file 
                #Plays the audio file to the user via audio output
                with open('output.mp3', 'wb') as out:
                    out.write(response.audio_content)
                    file = "output.mp3"
                    os.system("mpg123 " + file)
                    print('Audio content written to file "output.mp3"')
            
            #If object_.name = Chair        
            if object_.name == (r'Chair') and object_.score > 0.8:
                speech = "Ahmed, there is a chair %s metres in front of you!" % str(int(distance)/100)
                synthesis_input = texttospeech.types.SynthesisInput(text=speech)
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                response = client_speech.synthesize_speech(synthesis_input, voice, audio_config)
                with open('output.mp3', 'wb') as out:
                    out.write(response.audio_content)
                    file = "output.mp3"
                    os.system("mpg123 " + file)
                    print('Audio content written to file "output.mp3"')
            
            #If object_.name = Table
            if object_.name == (r'Table') and object_.score > 0.8:
                speech = "Ahmed, there is a table %s metres in front of you!" % str(int(distance)/100)
                synthesis_input = texttospeech.types.SynthesisInput(text=speech)
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                response = client_speech.synthesize_speech(synthesis_input, voice, audio_config)
                with open('output.mp3', 'wb') as out:
                    out.write(response.audio_content)
                    file = "output.mp3"
                    os.system("mpg123 " + file)
                    print('Audio content written to file "output.mp3"')
            
            #If object_.name = Door
            if object_.name == (r'Door') and object_.score > 0.7:
                speech = "Ahmed, there is a door %s metres in front of you!" % str(int(distance)/100)
                synthesis_input = texttospeech.types.SynthesisInput(text=speech)
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                response = client_speech.synthesize_speech(synthesis_input, voice, audio_config)
                with open('output.mp3', 'wb') as out:
                    out.write(response.audio_content)
                    file = "output.mp3"
                    os.system("mpg123 " + file)
                    print('Audio content written to file "output.mp3"')
        
        #Reset timer for snapshot   
        start_time = time.time()
    
    #While loop counter
    img_counter += 1

#Release the camera back to the OS, will throw an error otherwise and destory open camera capture window
capture.release()
cv2.destroyAllWindows()
