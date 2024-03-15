import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
import requests
import ftplib
import socket
import threading

# to clear the output box, we need to enable it first to clear it.
def clear_output(output_box):
    output_box.config(state='normal')
    output_box.delete('1.0', 'end')
    output_box.config(state='disabled')

# to insert a text into the output box, we need to enable it first, then insert the text, and finally disable it again.
def display_output(output_box, output_text):
    output_box.config(state='normal')
    output_box.delete('1.0', 'end')
    output_box.insert('1.0', output_text)
    output_box.config(state='disabled')

# this function is used to add text to the output box.
def add_output(output_box, output_text):
    output_box.config(state='normal')
    output_box.insert('end', output_text + '\n')
    output_box.see('end')
    output_box.config(state='disabled')

# creating the main window
root = tk.Tk()

# to have multiple tabs, we need to create a notebook widget
nb = ttk.Notebook(root)
root.title("Network Utility")

# creating the frames for the tabs
frame1 = ttk.Frame(nb)
frame2 = ttk.Frame(nb)
frame3 = ttk.Frame(nb)

# DNS TOOL WINDOW
# defining functions for the DNS commands first
# using subprocess to run the traceroute and tracepath commands
def run_command():
    command_name = command_combo.get()
    domain = command_input.get()
    output_text = subprocess.run([command_name, domain], capture_output=True, text=True).stdout
    display_output(command_output, output_text)

# for the HTTP and FTP requests we use the requests and ftplib libraries
def send_request():
    request_type = request_combo.get()
    request_url = url_input.get()
    request_port = port_input.get()

    if request_type == "HTTP":
        if request_port == "":
            request_port = "80"
        try:
            response = requests.get(f"http://{request_url}:{request_port}")
            display_output(command_output, response.text)
        except requests.exceptions.RequestException as e:
            display_output(command_output, e)
    elif request_type == "FTP":
        if request_port == "":
            request_port = "21"
        try:
            ftp = ftplib.FTP()
            ftp.connect(request_url, int(request_port))
            ftp.login(username_input.get(), password_input.get())
            display_output(command_output, ftp.getwelcome())
            ftp.quit()
        except ftplib.error_perm as e:
            display_output(command_output, e)

# we will have two columns in the main frame, one for the commands and one for the requests
command_frame = ttk.Frame(frame1)
command_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")
request_frame = ttk.Frame(frame1)
request_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")
output_frame = ttk.Frame(frame1)
output_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")

# getting the command name and the domain from the user
input_label = ttk.Label(command_frame, text="Enter the domain")
input_label.pack(padx=5)
command_input = ttk.Entry(command_frame, width=25)
command_input.pack(padx=5, pady=5)

# allowing the user to choose the command from the dropdown list
commands = ["nslookup", "host", "dig"]
command_combo = ttk.Combobox(command_frame, values=commands)
command_combo.set("Choose the command")
command_combo.pack(padx=5, pady=5)

# button to execute the command
exec_button = ttk.Button(command_frame, text="Execute", command=run_command)
exec_button.pack(padx=5, pady=5)

# output box that will display the command's results
output_label = ttk.Label(output_frame, text="Output")
output_label.pack(padx=5, pady=5)
command_output = scrolledtext.ScrolledText(output_frame, state='disabled')
command_output.pack(padx=5, pady=5)

frame1.pack(fill= tk.BOTH, expand=True)
nb.add(frame1, text = "DNS Commands")

# combobox that allows users to choose the protocol type for making a request
protocols = ["HTTP", "FTP"]
request_combo = ttk.Combobox(request_frame, values=protocols)
request_combo.set("Choose the protocol")
request_combo.pack(padx=5, pady=5)

# to make a request, we need to retrieve the URL and the port
input_label = ttk.Label(request_frame, text="Enter the URL")
input_label.pack(padx=5)
url_input = ttk.Entry(request_frame, width=25)
url_input.pack(padx=5, pady=5)

# input box for the server port
input_label = ttk.Label(request_frame, text="Enter the port")
input_label.pack(padx=5)
port_input = ttk.Entry(request_frame, width=25)
port_input.pack(padx=5, pady=5)

# since FTP requires a username and a password, we need to retrieve them from the user
input_label = ttk.Label(request_frame, text="Enter the username (FTP only)")
input_label.pack(padx=5)
username_input = ttk.Entry(request_frame, width=25)
username_input.pack(padx=5, pady=5)
input_label = ttk.Label(request_frame, text="Enter the password (FTP only)")
input_label.pack(padx=5)
password_input = ttk.Entry(request_frame, width=25)
password_input.pack(padx=5, pady=5)

# Button to send the request
send_button = ttk.Button(request_frame, text="Send", command=send_request)
send_button.pack(padx=5, pady=5)


# NETWORK TRACING WINDOW
# defining functions for the DNS commands first
# using subprocess to run the traceroute and tracepath commands
def run_trace_command():
    display_output(trace_output, "Processing your request... It might take a while.")
    trace_command_input.config(state='disabled')
    tracing_combo.config(state='disabled')
    trace_exec_button.config(state='disabled')
    if tracing_combo.get() == "traceroute":
        threading.Thread(target=run_traceroute).start()
    elif tracing_combo.get() == "tracepath":
        threading.Thread(target=run_tracepath).start()

def run_traceroute():
    domain = trace_command_input.get()
    output_text = subprocess.run(["traceroute", domain], capture_output=True, text=True).stdout
    display_output(trace_output, output_text)
    trace_command_input.config(state='normal')
    tracing_combo.config(state='normal')
    trace_exec_button.config(state='normal')

def run_tracepath():
    domain = trace_command_input.get()
    output_text = subprocess.run(["tracepath", domain], capture_output=True, text=True).stdout
    display_output(trace_output, output_text)
    trace_command_input.config(state='normal')
    tracing_combo.config(state='normal')
    trace_exec_button.config(state='normal')

# creating the frames for the tabs
trace_command_frame = ttk.Frame(frame2)
trace_command_frame.pack(padx=10, pady=10)
trace_output_frame = ttk.Frame(frame2)
trace_output_frame.pack(padx=10, pady=10)

# getting the domain from the user
input_label = ttk.Label(trace_command_frame, text="Enter the domain")
input_label.pack(padx=5)
trace_command_input = ttk.Entry(trace_command_frame, width=25)
trace_command_input.pack(padx=5, pady=5)

# allowing the user to choose the command from the dropdown list
tracing_commands = ["traceroute", "tracepath"]
tracing_combo = ttk.Combobox(trace_command_frame, values=tracing_commands)
tracing_combo.set("Choose the command")
tracing_combo.pack(padx=5, pady=5)

# button to execute the tracing commands
trace_exec_button = ttk.Button(trace_command_frame, text="Trace", command=run_trace_command)
trace_exec_button.pack(padx=5, pady=5)

# displaying the output of the tracing commands
trace_output_label = ttk.Label(trace_output_frame, text="Output")
trace_output_label.pack(padx=5, pady=5)
trace_output = scrolledtext.ScrolledText(trace_output_frame, state='disabled')
trace_output.pack(padx=5, pady=5)

frame2.pack(fill= tk.BOTH, expand=True)
nb.add(frame2, text = "Network Tracing")


# SOCKET PROGRAMMING WINDOW
# defining the server_socket as a global variable so that we can close it when the user wants to stop the server
server_socket = None

# starting the server that listens for incoming connections
def start_server():
    def run_server():
        global server_socket

        ip = socket_ip_input.get()
        port = int(socket_port_input.get())

        # depending on the protocol, we need to create a TCP or UDP socket
        if socket_combo.get() == "TCP":
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif socket_combo.get() == "UDP":
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # to avoid the "Address already in use" error, we need to catch the exception
        try:
            server_socket.bind((ip, port))
            clear_output(server_output)
        except OSError as e:
            add_output(server_output, f"Error: {e}")
            return

        if socket_combo.get() == "TCP":
            add_output(server_output, f"TCP server has started.\nListening on {ip}, {port}.")
        elif socket_combo.get() == "UDP":
            add_output(server_output, f"UDP server has started.\nListening on {ip}, {port}.")

        # making some ui elements disabled to prevent the user from changing the settings while the server is running
        socket_ip_input.config(state='disabled')
        socket_port_input.config(state='disabled')
        socket_combo.config(state='disabled')
        start_button.config(text="Stop server", command=stop_server, state="disabled")
        message_input.config(state='normal')
        send_button.config(state='normal')
        
        if socket_combo.get() == "TCP":
            server_socket.listen(1)
            client_socket, client_address = server_socket.accept()
            add_output(server_output, f"Server accepted connection from {client_address}.")
            message = client_socket.recv(1024)
            # displaying the message that the server has received
            add_output(server_output, f"Server has received a message: {message.decode()}")
            # sending a response to the client
            client_socket.send(b"Good to know.")
            client_socket.close()
            return
        elif socket_combo.get() == "UDP":
            message, client_address = server_socket.recvfrom(1024)
            add_output(server_output, f"Server accepted connection from {client_address}.")
            add_output(server_output, f"Server has received a message: {message.decode()}")
            server_socket.sendto(b"Good to know.", client_address)
            return

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

# initiating the client that connects to the server and then sending a message
def send_message():
    def run_send_message():
        ip = socket_ip_input.get()
        port = int(socket_port_input.get())

        if socket_combo.get() == "TCP":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif socket_combo.get() == "UDP":
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        client_socket.connect((ip, port))
        add_output(client_output, f"Client connected to {ip}, {port}.")

        # taking input from the user and sending it to the server
        message = message_input.get()
        client_socket.send(message.encode())
        add_output(client_output, f"Client sent a message: {message}")

        message_input.config(state='disabled')
        send_button.config(state='disabled')

        response = client_socket.recv(1024)
        add_output(client_output, f"Server responded with: {response.decode()}")

        # after getting the successful response, we close the client socket
        client_socket.close()
        add_output(client_output, "Client disconnected.")

        start_button.config(state="normal")

    client_thread = threading.Thread(target=run_send_message)
    client_thread.start()

# function to stop the server so user can create a new one
def stop_server():
    global server_socket
    if server_socket is not None:
        server_socket.close()
        server_socket = None
    add_output(server_output, "Server stopped.")
    socket_ip_input.config(state='normal')
    socket_port_input.config(state='normal')
    socket_combo.config(state='normal')
    start_button.config(text="Start server", command=start_server)
    message_input.config(state='disabled')
    send_button.config(state='disabled')

# creating the frames for the tabs
server_frame = ttk.Frame(frame3)
server_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")
client_frame = ttk.Frame(frame3)
client_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

# allowing the user to choose the protocol from the dropdown list
socket_types = ["TCP", "UDP"]
socket_combo = ttk.Combobox(server_frame, values=socket_types)
socket_combo.set("Choose the protocol")
socket_combo.pack(padx=5, pady=5)

# getting the server IP and port from the user
input_label = ttk.Label(server_frame, text="Enter IP address")
input_label.pack(padx=5)
socket_ip_input = ttk.Entry(server_frame, width=25)
socket_ip_input.pack(padx=5, pady=5)
input_label = ttk.Label(server_frame, text="Enter port")
input_label.pack(padx=5)
socket_port_input = ttk.Entry(server_frame, width=25)
socket_port_input.pack(padx=5, pady=5)

# button to start the server
start_button = ttk.Button(server_frame, text="Start server", command=start_server)
start_button.pack(padx=5, pady=5)

# displaying the output of the server
server_output_label = ttk.Label(server_frame, text="Server output")
server_output_label.pack(padx=5, pady=5)
server_output = scrolledtext.ScrolledText(server_frame, state='disabled', width=40)
server_output.pack(padx=5, pady=5)

# initiating the client that connects to the server and then sending a message from input box
message_label = ttk.Label(client_frame, text="Message (optional)")
message_label.pack(padx=5)
message_input = ttk.Entry(client_frame, width=25, state="disabled")
message_input.pack(padx=5, pady=5)
send_button = ttk.Button(client_frame, text="Start client", command=send_message, state="disabled")
send_button.pack(padx=5, pady=5)

# displaying the output of the client
client_output_label = ttk.Label(client_frame, text="Client output")
client_output_label.pack(padx=5, pady=5)
client_output = scrolledtext.ScrolledText(client_frame, state='disabled', width=40)
client_output.pack(padx=5, pady=5)

frame3.pack(fill= tk.BOTH, expand=True)
nb.insert("end", frame3, text = "Socket Programming")

nb.pack(padx = 5, pady = 5, expand = True)
root.mainloop()