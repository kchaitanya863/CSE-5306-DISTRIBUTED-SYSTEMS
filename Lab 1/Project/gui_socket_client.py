import socket
import time
from tkinter import *
import threading

# methods
# Quit functionality for GUI
def quit():
    global root
    root.destroy()

# start the socket listener thread
def start_thread():
    print("start thread")
    global username
    global username_box
    global status_label
    global skip_button
    global t
    username = username_box.get()
    t  = threading.Thread(target=listen)
    t.daemon = True
    t.start()
    username_label.pack_forget()
    username_box.pack_forget()
    login_button.pack_forget()
    status_label = Label(root, text = "connecting as {}".format(username))
    status_label.pack()
    skip_button = Button(root, text="skip", command=skip_wait)
    skip_button.pack()
    skip_button['state'] = DISABLED

# skips the pause signal received from the server
def skip_wait():
    global wait_time
    wait_time = 0

# utility to set UI message
def set_label(data):
    global status_label
    status_label.config(text=str(data))

# listen to the server over the socket
def listen():
    try:
        try:
            global wait_time
            global skip_button
            s = socket.socket()
            s.connect((host, port))
            # request with the username
            s.send(str.encode(username))
            data = s.recv(1024).decode('utf-8')
            set_label(data)
            print(data + " as " + username)
            if data == "Username already in use..":
                set_label(data)
                username_label.pack()
                username_box.pack()
                login_button.pack()
                skip_button.pack_forget()
                s.close()
                time.sleep(2)
                status_label.pack_forget()
                return
        except Exception as e:
            set_label("Connection could not be established.." + str(e))
        # username available and connected to server
        root.title(username) # set the window title to username once connected
        # keep listening to the server and send responses 
        while True:
            print("data receiving...")
            data = s.recv(1024).decode('utf-8')
            wait_time = int(data)
            if data == "check":
                s.send(str.encode("check_received"))
                continue
            set_label(data)
            count = 0
            while wait_time > 0:
                count+=1
                skip_button['state'] = NORMAL
                time.sleep(1)
                wait_time-=1
                set_label(wait_time)
            skip_button['state'] = DISABLED
            set_label("Listening for server..")
            s.send(str.encode("Client {} waited {} seconds for server.".format(username, str(count))))
    except Exception as e:
        set_label("connection Lost...")

# code
# socket initialization 
s = socket.socket()
host = 'localhost'
port = 9999
username = "user1"
# GUI widgets 
root = Tk()
root.title('Client')
root.geometry("370x120")
username_label = Label(root, text="Enter username")
username_label.pack()
username_box = Entry(root)
username_box.pack()
login_button = Button(root, text="logon", command=start_thread)
login_button.pack()
quit_button = Button(root, command=quit, text="Quit")
quit_button.pack()

# GUI loop
root.mainloop()


