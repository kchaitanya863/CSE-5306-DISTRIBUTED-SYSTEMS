# Krishna Chaitanya Naragam
# 1001836274

from tkinter import *
from datetime import datetime
import threading
import random
import string
import requests


# methods
# generate a random string of length specified
# https://pynative.com/python-generate-random-string/
def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# load the upload messages UI
def upload_messages_ui():
    # UI for uploading messages
    global upload_status_label
    upload = Tk()
    # upload.geometry("370x150")
    upload.title("Upload Message")

    upload_status_label = Label(upload, text="")
    upload_status_label.pack()
    q = StringVar(upload)
    q.set("A") # default value
    w = OptionMenu(upload, q, "A", "B", "C") # dropdown 
    w.pack()
    number_enter_label = Label(upload, text="Enter a number to send:")
    number_enter_label.pack()
    number_enter_box = Entry(upload)
    number_enter_box.pack()
    send_number_button = Button(upload, text="Send to Queue", command=lambda: send_metric_to_server(q.get(),number_enter_box.get()))
    send_number_button.pack()
    quit_button = Button(upload, command=lambda: upload.destroy(), text="Close")
    quit_button.pack()
    upload.mainloop()

# load the receive messages UI
def check_messages_ui():
    global check_messages_status_label
    check = Tk()
    # check.geometry("370x130")
    check.title("Check for messages")

    check_messages_status_label = Label(check, text="")
    check_messages_status_label.pack()

    q = StringVar(check)
    q.set("A") # default value
    w = OptionMenu(check, q, "A", "B", "C") # dropdown 
    w.pack()

    number_enter_label = Label(check, text="Select queue and click Check for messages")
    number_enter_label.pack()
    send_number_button = Button(check, text="Check for messages", command=lambda: poll_queue(q.get()))
    send_number_button.pack()
    quit_button = Button(check, command=lambda: check.destroy(), text="Close")
    quit_button.pack()
    check.mainloop()

# set upload label
def set_upload_ui_label(data):
    global upload_status_label
    upload_status_label.config(text=str(data))

# set check messages label
def set_check_messages_ui_label(data):
    global check_messages_status_label
    check_messages_status_label.config(text=str(data))

# Send a number to server
def send_metric_to_server(q, metric):
    try:
        response = requests.get('http://{}:{}/putInQueue/{}/{}/{}'.format(host, port, user, q, metric))
        print('http://{}:{}/putInQueue/{}/{}/{}'.format(host, port, user, q, metric))
        print(response.text)
        set_upload_ui_label(response.text)
    except Exception as e:
        set_upload_ui_label("Server not found!!")

# receive from queue
def poll_queue(q):
    try:
        response = requests.get('http://{}:{}/getQueue/{}/{}'.format(host, port, user, q))
        print('http://{}:{}/getQueue/{}/{}'.format(host, port, user, q))
        print(response.text)
        set_check_messages_ui_label(response.text)
    except Exception as e:
        set_check_messages_ui_label("Server not found!!")

# utility method to start popup UI in a new window
def start_new_ui(i):
    if i == 1:
        t = threading.Thread(target=check_messages_ui)
        t.daemon = True
        t.start()
    elif i == 0:
        t = threading.Thread(target=upload_messages_ui)
        t.daemon = True
        t.start()

# Quit functionality for GUI
def quit():
    global root
    root.destroy()

# Initial GUI
host = "localhost"
port = 5000
user = get_random_string(5)


# GUI widgets
root = Tk()
root.title(user)
send_number_button = Button(root, text="Upload Message", command=lambda: start_new_ui(0))
send_number_button.pack()

poll_queue_button = Button(root, text="Check for messages", command=lambda: start_new_ui(1))
poll_queue_button.pack()
quit_button = Button(root, command=quit, text="Quit")
quit_button.pack()

# GUI loop
root.mainloop()

