#Test GUI for AI chatbot

#Library
from tkinter import *

#Create tinker object (parent window)
root = Tk()

#Window title
root.title('Buddee AI Chatbot')

#Window dimensions
root.geometry('400x500')

#Sub menu for file
file_menu = Menu(root)
file_menu.add_command(label='New...')
file_menu.add_command(label='Save As...')
file_menu.add_command(label='Exit')

#Main menu bar
main_menu = Menu(root)
main_menu.add_cascade(label='File', menu=file_menu)
main_menu.add_command(label='Edit')
main_menu.add_command(label='Quit')
root.config(menu=main_menu)

#Chat window area
chatWindow = Text(root, bd=3, bg='white', width=50, height=8)
chatWindow.place(x=6, y=6, height=385, width=370)

#Text message area
messageWindow = Text(root, bd=3, bg='white', width=30, height=4)
messageWindow.place(x=6, y=400, height=88, width=260)

#Button to send message
Button = Button(root, text='Send', bg='blue', activebackground='light blue', width=12, height=5, font=('Arial', 20))
Button.place(x=270, y=400, height=88, width=120)



#Event loop which waits for user input, keeps window open until user closes out window
root.mainloop()