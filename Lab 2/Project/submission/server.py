# Krishna Chaitanya Naragam
# 1001836274

from tkinter import *
from datetime import datetime
import threading
from flask import Flask
import os, signal
from flask import request
import time

# declarations 
root = None
information_panel = None

# serve Queue A
def serve_A(i):
    i = float(i)
    output = "\n=========================\n"
    output += "Meter: {}\n".format(i)
    output += "Millimeter: {}\n".format(i*1000)
    output += "Centimeter: {}\n".format(i*100)
    output += "Kilometer: {}\n".format(i*0.001)
    output += "Astronomical Unit: {}\n".format(i*(6.68459e-12))
    output += "=========================\n"  
    return output

# serve Queue B
def serve_B(i):
    i = float(i)
    output = "\n=========================\n"
    output += "Meter: {}\n".format(i)
    output += "Parsec: {}\n".format(i*(3.24078e-17))
    output += "Light Year: {}\n".format(i*(1.057e-16))
    output += "Inch: {}\n".format(i*39.3701)
    output += "Foot: {}\n".format(i*3.28084)
    output += "Yard: {}\n".format(i*(1.0936133333333))
    output += "=========================\n"  
    return output

# serve Queue A
def serve_C(i):
    i = float(i)
    output = "=========================\n"
    output += "Meter: {}\n".format(i)
    output += "Mile: {}\n".format(i*0.000621371)
    output += "Nautical Mile: {}\n".format(i*0.000539957)
    output += "American football field: {}\n".format(i/109.7)
    output += "Hand: {}\n".format(i*9.84252)
    output += "Horse: {}\n".format(i/2.4)
    output += "=========================\n"  
    return output

# Quit functionality for GUI
def quit():
    global app
    global root
    app.do_teardown_appcontext()
    root.destroy()
    os.kill(os.getpid(), signal.SIGINT)

# append information to panel on the UI
def append_info_panel(info):
    global information_panel
    information_panel['state'] = NORMAL
    information_panel.insert(END, str(datetime.now())+ ": " + str(info)+"\n")
    information_panel.see(END)
    information_panel['state'] = DISABLED

# run GUI
def run_GUI():
    # GUI loop
    global information_panel
    global root
    root = Tk()
    root.title('Server')
    server_status = Label(root, text="Server: Online")
    server_status.pack()
    information_panel = Text()
    information_panel.pack()
    information_panel['state'] = DISABLED
    quit_button = Button(root, command=quit, text="Quit")
    quit_button.pack()
    root.mainloop()

app = Flask(__name__)


# home page
@app.route('/')
def home():
    return 'Server up!'

# get entire queue and delete the file
@app.route('/getQueue/<user>/<q>')
def getQueue(user,q):
    append_info_panel("User connected {}".format(user))
    if q in ['A', 'B', 'C']:
        
        out = ''
        try:
            f= open('{}.queue'.format(q))
            out = f.read()
            f.close()
            os.remove('{}.queue'.format(q))
        except Exception as e:
            out = "Queue {} is empty!".format(q)
        append_info_panel("Getting Queue {}\n{}".format(q, out))
        return out
    append_info_panel("User {} Disconnected!".format(user))
    return "Queue Not Found"

# put item into the queue
@app.route('/putInQueue/<user>/<q>/<metric>')
def putInQueue(user,q,metric):
    append_info_panel("User connected {}".format(user))
    append_info_panel("user {} inserterd to queue: {}, metric: {}".format(user, q, metric))
    f = open('{}.queue'.format(q),'a+')
    if q == 'A':
        metric = serve_A(metric)
    if q == 'B':
        metric = serve_B(metric)
    if q == 'C':
        metric = serve_C(metric)
    f.write(metric)
    f.close()
    append_info_panel("Converted values are,\n{}".format(metric))
    append_info_panel("User {} Disconnected!".format(user))
    return "inserted to queue: {}".format(q)

if __name__ == '__main__':
    port = 5000
    t = threading.Thread(target=run_GUI)
    t.daemon = True
    t.start()
    time.sleep(2)
    append_info_panel("Server running on port {}".format(port))
    app.run(port=port)