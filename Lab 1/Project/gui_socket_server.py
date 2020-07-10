from tkinter import *
from datetime import datetime
import threading
import socket
import time
import random

# declarations 
root = Tk()
root.title('Server')
server_status = Label(root, text="Server: offline")
server_status.pack()
information_panel = Text()
information_panel.pack()
information_panel['state'] = DISABLED

all_connections = []
all_address = []
all_clients = []

# methods

# append information to panel on the UI
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

# Accepting connection from multiple clients
def accept_connections():
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
            client_name = str(conn.recv(1024), "utf-8")
            
            # client trying to connect
            append_info_panel("Client connection request " + client_name)
            if client_name in all_clients:
                conn.send(str.encode("Username already in use.."))
                conn.close()
                all_connections.remove(conn)
                all_address.remove(address)
                append_info_panel("username, '{}' already in use".format(client_name))
            else:
                all_clients.append(client_name)
                conn.send(str.encode("Connected.."))
                append_info_panel("'{}' is now connected..".format(client_name))
                update_active_connections_label()
        except:
            print("Error accepting connections")


# send pause command to a random client
def send_timeout():
    if len(all_connections) == 0:
        append_info_panel("No clients connected!")
        return
    i = random.randrange(0,len(all_connections))
    conn = all_connections[i]
    client_name = all_clients[i]
    try:
        cmd = str(random.randrange(3,9))
        if len(str.encode(cmd)) > 0:
            append_info_panel("Sending pause command to: "+client_name+ "  :  " + cmd)
            conn.send(str.encode(cmd)) # sending the random number to client
            client_response = str(conn.recv(1024), "utf-8")
            append_info_panel(client_response)
            return
    except ConnectionResetError as e:
        append_info_panel("{} disconnected".format(client_name)) # client disconnected or no longer availavle
        conn.close()
        del all_address[i]
        del all_clients[i]
        del all_connections[i]
        update_active_connections_label()
        send_timeout()
    except Exception as e:
        return

# Start socket server 
def start_server():
    create_socket()
    bind_socket()
    accept_connections()

# Quit functionality for GUI
def quit():
    global root
    root.destroy()

# uses new thread to send a pause signal to clinet and receive response from the client
def pause_random_every_10_seconds():
    while True:
        # append_info_panel("sending timeout..")
        t1 = threading.Thread(target=send_timeout)
        t1.daemon = True
        t1.start()
        time.sleep(10)

# set active connections label on GUI
def update_active_connections_label():
    data = "No Clients conencted!"
    if len(all_clients) > 0:
        data = "Connected to: " + ",".join(all_clients)
    global active_connections_label
    active_connections_label.config(text=str(data))


# code
append_info_panel("Server is currently offline")

# start the socket server thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

append_info_panel("Server started at port 9999")
server_status.config(text="Server: Online")

# GUI add send button Uncomment to have that functionality
# send_button = Button(root, command=send_timeout, text="send timeout")
# send_button.pack()
active_connections_label = Label(root, text="No Active Connections!")
active_connections_label.pack()
quit_button = Button(root, command=quit, text="Quit")
quit_button.pack()

# send pause signals over a new thread
pause_thread = threading.Thread(target=pause_random_every_10_seconds)
pause_thread.daemon = True
pause_thread.start()


# GUI loop
root.mainloop()