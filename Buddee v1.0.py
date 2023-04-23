import openai
import pyttsx3
import speech_recognition as sr

from api_secrets import API_KEY

openai.api_key = API_KEY

engine = pyttsx3.init()

r = sr.Recognizer()
# Sets variable mic to microphone device.
mic = sr.Microphone(device_index=1)
# print(sr.Microphone.list_microphone_names())

# Allows integration of context into the conversation.
conversation = ""
user_name = "Mahir"

engine.say("Hi, I'm Buddee, your artifical intelligent friend! Please speak clearly into your microphone so I can hear you.")
engine.runAndWait()

#While true loop to listen to mic source and transcribe the audio to text. The transcription is then stored in user input variable.
while True:
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("No longer listening.")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

# Creates the prompt for the AI using user name and input variables.
    prompt = user_name + ": " + user_input + "\n" + "Buddee :"
# Adds prompt to conversation variable to build history of chat.
    conversation += prompt

#Uses openai method to set engine to 'davinci-003', prompt to conversation and max tokens.
    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
#Formats response as string.
    response_str = response["choices"][0]["text"].replace("\n", "")
#Removes username and bot name from response string.
    resposnse_str = response_str.split(user_name + ": ", 1)[0].split("Buddee" + ": ", 1)[0]

#Adds reponse string to conversation to build history of chat.
    conversation +=  response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()