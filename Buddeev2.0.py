# Libraries
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import openai
import pyttsx3
import sys
sys.path.append("C:\\Users\\Mahir\\PycharmProjects\\Buddee\\venv\\Lib\\site-packages")
import speech_recognition as sr
from api_secrets import API_KEY
import time


# Imports api key
openai.api_key = API_KEY

# Engine specified
engine = pyttsx3.init()

# Speech recognition initialized
r = sr.Recognizer()
# Microphone initialized
mic = sr.Microphone(device_index=1)

# Asks the user whether they are visually impaired or not by speaking
print("Hi, I'm Buddee, your personal AI companion, before we get started I need to know whether you are visually impaired or not, please say yes if you are or no if you aren't")
engine.say("Hi, I'm Buddee, your personal AI companion, before we get started I need to know whether you are visually impaired or not, please say yes if you are or no if you aren't")
engine.runAndWait()
with mic as source:
    print("Listening...")
    r.adjust_for_ambient_noise(source, duration=0.2)
    audio = r.listen(source)
print("No longer listening.")
try:
    va = r.recognize_google(audio)
    print("User response:", va)
except:
    print("Could not recognize user response.")
    va = ""

#activate visually impaired mode if user response is yes.
if va.lower() == "yes":
    with mic as source:
        print("Visually impaired mode activated")
        engine.say("Visually impaired mode activated")
        print("What is your name?")
        engine.say("What is your name?")
        engine.runAndWait()
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    try:
        user_name = r.recognize_google(audio)
        print("User response:", user_name)
    except:
        print("Could not recognize user response.")
        user_name = ""
    # Initializes conversation variable
    conversation = ""
    print(f"Hi {user_name} how are you doing?")
    engine.say(f"Hi {user_name} how are you doing?")
    engine.runAndWait()

    # While true loop to listen to mic source and transcribe the audio to text.
    while True:
        with mic as source:
            print("Listening...")
            engine.say("Listening")
            engine.runAndWait()
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
        print("No longer listening.")

        try:
            user_input = r.recognize_google(audio)
        except:
            continue
        if "exit program" in user_input.lower():
            break

        # Creates the prompt for the AI using user name and input variables.
        prompt = user_name + ": " + user_input + "\n" + "Buddee :"

        # Adds prompt to conversation variable to build history of chat.
        conversation += prompt

        # Uses openai method to set engine to 'davinci-003', prompt to conversation and max tokens.
        response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)

        # Formats response as string.
        response_str = response["choices"][0]["text"].replace("\n", "")

        # Removes username and bot name from response string.
        response_str = response_str.split(user_name + ": ", 1)[0].split("Buddee" + ": ", 1)[0]

        # Adds reponse string to conversation to build history of chat.
        conversation +=  response_str + "\n"
        print(response_str)

        engine.say(response_str)
        engine.runAndWait()

else:
    # Initializes conversation variable
    conversation = ""

    # Set up tkinter GUI
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Buddee: Personal AI Companion")
    # Hides main window
    root.withdraw()


    def open_help_window():
        # Create a new Toplevel window
        help_window = Toplevel(root)
        help_window.title('Help')
        help_window.geometry('500x100')

        # Create a label and text box in the new window
        label = Label(help_window,
                      text="This is Buddee, your personal AI companion.\nType something in the text box and press submit,\n or press the speak button and speak into your microphone.\nBuddee will try its best to answer any questions or requests you may have.\nDisclaimer: Buddee is just an artificial intelligence chatbot created by humans.\n Please do not replace human relationships with aritifical intelligence. :)")
        label.pack()


    def clear_conversation():
        global conversation
        conversation = ""
        conversation_box.config(state=NORMAL)
        conversation_box.delete('1.0', END)
        conversation_box.insert(tk.END, "Conversation cleared\nPlease type or say something...")
        conversation_box.config(state=DISABLED)


    # Defines function to handle text input
    def handle_input():
        # Enables conversation box so that is read and write.
        conversation_box.config(state=NORMAL)
        global conversation
        user_input = input_box.get("1.0", tk.END).strip()
        input_box.delete("1.0", tk.END)

        # Bold the username and Buddee prompts
        bold_username = user_name
        conversation_box.tag_config("bold_username", font=("Arial", 12, "bold"))

        prompt = bold_username + ": " + user_input + "\n" + "Buddee:"
        conversation += prompt

        start_time = time.time()
        # Defines engine, prompt and tokens used for response
        response = openai.Completion.create(engine='text-davinci-003', prompt=conversation, max_tokens=50)

        # Formats response string and speaks it
        if len(response.choices) > 0:
            response_str = response.choices[0].text.replace("\n", "")
            response_str = response_str.split(user_name + ": ", 1)[0].split("Buddee: ", 1)[0]
            conversation += response_str + "\n"
            print(response_str)

            engine.say(response_str)
            engine.runAndWait()

            # Display conversation in text box
            conversation_box.insert(tk.END, prompt, "bold_username")
            conversation_box.insert(tk.END, response_str + "\n")

            end_time = time.time()
            duration = end_time - start_time
            print(f"Response time: {duration} seconds ")
            # Disables conversation box so that it is read only
            conversation_box.config(state=DISABLED)


    # Defines function to handle voice input
    def handle_voice_input():
        # Changes conversation box config state to normal, (allows read and write)
        conversation_box.config(state=NORMAL)
        with mic as source:
            audio = r.listen(source)
            try:
                user_input = r.recognize_google(audio)
                input_box.insert(tk.END, user_input)
                handle_input()
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said.")
        # Changes conversation box config state to disabled, (read only)
        conversation_box.config(state=DISABLED)


    # Main menu bar
    main_menu = Menu(root)
    main_menu.add_command(label='Clear', command=clear_conversation)
    main_menu.add_command(label='Help', command=open_help_window)
    root.config(menu=main_menu)

    # Prompts user for name
    user_name = simpledialog.askstring(title="Buddee: Personal AI Companion", prompt="What's your name?\t\t\t\t")
    # Displays main window after dialogue box is closed
    root.deiconify()
    engine.say(f"Hi {user_name}")
    engine.runAndWait()

    # Create text box to display conversation
    conversation_box = tk.Text(root, bd=3, height=20, width=60)
    conversation_box.pack()
    # Changes font to arial size 12
    conversation_box.config(font=("Arial", 12))

    # Create input box for user to type into
    input_box = tk.Text(root, bd=3, height=2, width=60)
    input_box.pack()
    input_box.config(font=("Arial", 12))

    # Welcome message
    conversation_box.insert(tk.END, f"Hi {user_name} I'm Buddee, your personal AI companion.\nPlease type or say something...\n\n")
    # Disables conversation box so that it1ly
    conversation_box.config(state=DISABLED)

    # Creates Button for submitting text
    submit_button = tk.Button(root, text="Submit", bg='lightgrey', activebackground='lightblue', width=12, height=5, font=('Arial', 20), command=handle_input)
    submit_button.place(x=100, y=430, height=50, width=120)

    # Creates button to activate voice input
    voice_button = tk.Button(root, text="Speak", bg='lightgrey', activebackground='red', width=12, height=5,font=('Arial', 20),command=handle_voice_input)
    voice_button.place(x=270, y=430, height=50, width=120)

    # Start tkinter event loop
    root.mainloop()

