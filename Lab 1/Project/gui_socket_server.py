from tkinter import *
from datetime import datetime
import threading
import socket
import time
from queue import Queue
import random

# declarations 
root = Tk()
root.title('Server')
server_status = Label(root, text="Server: offline")
server_status.pack()
information_panel = Text()
information_panel.pack()
information_panel['state'] = DISABLED

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
all_clients = []

# methods
def append_info_panel(info):
    information_panel['state'] = NORMAL
    information_panel.insert(END, str(datetime.now())+ ": " + str(info)+"\n")
    information_panel.see(END)
    information_panel['state'] = DISABLED

# Create a Socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Bind socket and listen for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling connection from multiple clients and saving to a list
def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            # print("Connection has been established :" + address[0] + ":"+ str(address[1]))
            # append_info_panel("Connection has been established :" + address[0] + ":"+ str(address[1]))
            client_name = str(conn.recv(1024), "utf-8")
            
            append_info_panel("Client connection request " + client_name)
            if client_name in all_clients:
                conn.send(str.encode("Username already in use.."))
                conn.close()
                append_info_panel("username, '{}' already in use".format(client_name))
            else:
                all_clients.append(client_name)
                conn.send(str.encode("Connected.."))
                append_info_panel("'{}' is now connected..".format(client_name))
            # append_info_panel(str(all_address))
        except:
            print("Error accepting connections")


# send pause command to client
def send_timeout():
    if len(all_connections) == 0:
        append_info_panel("No clients connected!")
        return
    i = random.randrange(0,len(all_connections))
    conn = all_connections[i]
    client_name = all_clients[i]
    while True:
        try:
            cmd = str(random.randrange(3,9))
            if len(str.encode(cmd)) > 0:
                append_info_panel("Sending Data to: "+client_name+ "  :  " + cmd)
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                append_info_panel(client_response)
                return
        except ConnectionResetError as e:
            append_info_panel("closing connection to {}".format(client_name))
            conn.close()
            del all_address[i]
            del all_clients[i]
            del all_connections[i]
            continue
        except Exception as e:
            # append_info_panel("Error sending random number.\n" + str(e))
            break

# Check active client connections
def check_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            del all_clients[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)

def start_server():
    create_socket()
    bind_socket()
    accepting_connections()

def quit():
    global root
    root.destroy()

def pause_random_every_10_seconds():
    while True:
        append_info_panel("sending timeout..")
        send_timeout()
        time.sleep(10)
# code
append_info_panel("Server is currently offline")


server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

append_info_panel("Server started at port 9999")
server_status.config(text="Server: Online")

# GUI add send button
send_button = Button(root, command=send_timeout, text="send timeout")
send_button.pack()
quit_button = Button(root, command=quit, text="Quit")
quit_button.pack()

pause_thread = threading.Thread(target=pause_random_every_10_seconds)
pause_thread.daemon = True
pause_thread.start()


# GUI loop
root.mainloop()