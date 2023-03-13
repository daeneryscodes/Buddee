import tkinter as tk
import openai
import pyttsx3
import speech_recognition as sr
from api_secrets import API_KEY

openai.api_key = API_KEY

engine = pyttsx3.init()

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Mahir"


# Set up tkinter GUI
root = tk.Tk()
root.geometry("500x500")
root.title("Buddee Chatbot")

# Create text box to display conversation
conversation_box = tk.Text(root, bd=3, height=20, width=60)
conversation_box.pack()

# Create input box for user to type into
input_box = tk.Text(root, bd=3, height=2, width=60)
input_box.pack()

conversation_box.insert(tk.END, "Hi, I'm Buddee! Your personal AI friend.\nPlease type or say something using the buttons below...")

# Define function to handle user input
def handle_input():
    global conversation
    user_input = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)

    prompt = user_name + ": " + user_input + "\n" + "Buddee: "
    conversation += prompt

    #Defines engine, prompt and tokens used for response
    response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)

    # Error handling
    if len(response.choices) > 0:
        response_str = response.choices[0].text.replace("\n", "")
        response_str = response_str.split(user_name + ": ", 1)[0].split("Buddee: ", 1)[0]
        conversation += response_str + "\n"
        print(response_str)

        engine.say(response_str)
        engine.runAndWait()

        # Display conversation in text box
        conversation_box.insert(tk.END, prompt)
        conversation_box.insert(tk.END, response_str + "\n")

# Define function to handle voice input
def handle_voice_input():
    with mic as source:
        audio = r.listen(source)
        try:
            user_input = r.recognize_google(audio)
            input_box.insert(tk.END, user_input)
            handle_input()
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")

# Create button to submit user text input
submit_button = tk.Button(root, text="Send", bg='grey', activebackground='lightblue', width=12, height=5, font=('Arial', 20), command=handle_input)
submit_button.place(x=100, y=400, height=88, width=120)

# Create button to activate voice input
voice_button = tk.Button(root, text="Speak", bg='grey', activebackground='red', width=12, height=5, font=('Arial', 20), command=handle_voice_input)
voice_button.place(x=270, y=400, height=88, width=120)


# Start tkinter event loop
root.mainloop()
