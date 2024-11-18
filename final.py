import threading
import socket

class Config:
    EOF = b'EOF-DATA-TRANSMISSION-COMPLETE'
    SERVER_IP = "localhost"
    BUFFER_SIZE = 1024
    FILE_CHUNK_SIZE = 1024
    RUN = True

def send_data(con):
    try:
        print("============================================")
        print("You can now send messages or files to the target or type 'terminate123' to exit.")
        print("============================================")
        while Config.RUN:
            send_msg = input()
            # Check if the user wants to exit
            if send_msg.lower() == 'terminate123':
                print("Exiting...")
                Config.RUN = False  # This will signal other threads to stop
                break
            # Check if the user wants to send a file
            elif send_msg.startswith("transfer "):
                file_name = send_msg.split()[1]
                try:
                    # 
                    con.sendall(send_msg.encode())
                    print("Transferring data...")
                    with open(file_name, "rb") as clientFile:
                        data = clientFile.read(Config.FILE_CHUNK_SIZE)
                        while data:
                            con.sendall(data)
                            data = clientFile.read(Config.FILE_CHUNK_SIZE)
                    con.sendall(Config.EOF)
                    print("--------------------------")
                    print(f"File {file_name} Sent")
                    print("--------------------------")
                except FileNotFoundError:
                    print("File not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                con.sendall(send_msg.encode())
    finally:
        con.close()
        print("Connection closed by sender.")


def main():
    port1 = int(input("Enter your listening port number: "))
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind the listener socket to the specified port
        listener_socket.bind((Config.SERVER_IP, port1))
        listener_socket.listen(1)
        print("Listening on port:", listener_socket.getsockname()[1])
        
        port2 = int(input("Enter the port number to connect: "))
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to the target port
            sender_socket.connect((Config.SERVER_IP, port2))
            print("Connected to", port2)
            threading.Thread(target=send_data, args=(sender_socket,), daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to target port {port2}: {e}")
            listener_socket.close()
            return  # Early exit if connection fails

        conn, _ = listener_socket.accept()
        print("Connection successfully established with:", conn.getpeername())
        try:
            while Config.RUN:
                data_received = conn.recv(Config.BUFFER_SIZE)
                if not data_received:
                    print("Connection closed by the other side.")
                    break
                recv_msg = data_received.decode()
                print("Received:", recv_msg)

                if recv_msg.lower() == 'terminate123':  # Check if the other side sent an exit command
                    print("Exit command received. Shutting down...")
                    Config.RUN = False  # Set the flag to stop the send_data thread
                    break

                # Check if the received message is a file transfer request
                if recv_msg.startswith("transfer "):
                    filename = recv_msg.split()[1]
                    # Receive the file in chunks and write to a file
                    with open(f"fetched_{filename}", "wb") as file:
                        while True:
                            data_received = conn.recv(Config.BUFFER_SIZE)
                            if data_received.endswith(Config.EOF):
                                data_received = data_received[:-len(Config.EOF)]
                                file.write(data_received)
                                break
                            file.write(data_received)
                    print("--------------------------")
                    print(f"File {filename} received.")
                    print("--------------------------")
        finally:
            conn.close()
            print("Connection closed by receiver.")
    finally:
        listener_socket.close()
        print("Listener socket closed.")

# Call the main function
print("Hey there!!")
main()

