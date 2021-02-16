import socket
import select
import errno
import sys
from tkinter import *
import keyboard
from playsound import playsound

# Specifies the directory where notification sounds can be sent.
# This can allow directories to be changed for custom notification sounds
innotifdir = "assets/audio/innoti.wav"
outnotifdir = "assets/audio/outnoti.mp3"

chathistory = "This is the beginning of the chat.\n"
#Initialize GUI------------
root = Tk()
my_username = input("//VXNY.NET USERNAME// >>")
root.geometry("600x600")
root.title("Voxany Chat")
voxico = PhotoImage(file="assets/images/cornerlogo.gif")
errorphoto = PhotoImage(file="assets/images/redattempting.png")
Label(root, image=voxico, bg = "black").grid(row=0, column=0)
prompt = Entry(root, fg="Purple", bg="Black", bd=5, width = 50)
root.configure(background="black")
message = ""
messageid = 0



iconicon = PhotoImage(file =  "assets/images/ico.png")


root.iconphoto(False, iconicon)


HEADER_LENGTH = 10

IP = "47.40.132.255"
PORT = 5555



prompt.place(x=20, y=400)
chatBox = Text(root, height=10, width =60, bg = "#101010", fg = "Purple", wrap=WORD)
chatBox.place(x = 32, y = 164)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)
        break
    except:
        Label(root, image=errorphoto, bg="black").grid(row=0, column=0)
        root.update()

root.iconphoto(False, iconicon)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
usernamelabel = Label(root, text="You are signed in as: " + str(my_username), fg = "Purple", bg="Black").place(x=32, y=128)
while True:
    root.update()
    if keyboard.is_pressed("enter") and len(prompt.get()) > 0:
        print(my_username +" > " +str(prompt.get()))
        message = prompt.get()
        if message == "ilovekruz":
            innotifdir = "assets/audio/kruzinnoti.wav"
            outnotifdir = "assets/audio/kruzoutnoti.wav"
        chatBox.insert(INSERT, "You >  " + str(message) + "\n")
        chatBox.see("end")
        prompt.delete(0, 1000)
        playsound(outnotifdir)


    if isinstance(message, str):
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

    try:

        #receive things
        username_header = client_socket.recv(HEADER_LENGTH)
        if not len(username_header):
            print("Vxny.net has Banished you.")
            sys.exit()

        username_length = int(username_header.decode('utf-8').strip())
        username = client_socket.recv(username_length).decode('utf-8')

        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')

        print(f"{username} > {message}")
        chatBox.insert(INSERT,f"{username} > {message}\n" )
        chatBox.see("end")
        message = ""
        playsound(innotifdir)


    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('VXNY.NET HAS ENCOUNTERED A MASSIVE ERROR AT ', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General Error', str(e))
        sys.exit()

