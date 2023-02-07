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

    prompt = user_name + ": " + user_input + "\n" + "Buddee :"

    conversation += prompt

    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)
    response_str = response["choices"][0]["text"].replace("\n", "")
    resposnse_str = response_str.split(user_name + ": ", 1)[0].split("Buddee" + ": ", 1)[0]


    conversation +=  response_str + "\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()