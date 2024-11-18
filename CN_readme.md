## Overview

This project is a Python-based networking application that enables real-time messaging and file transfer between two users on the same network. It uses socket programming and multi-threading to handle simultaneous data sending and receivinig.

## Features

- **Messaging**: Send and receive real-time messages over a network.
- **File Transfer**: Transfer files in chunks between users securely and efficiently.
- **Connection Handling**: Robust handling of network connections and disconnections.
- **Exit Mechanism**: Cleanly exit the application from either user side using a special command.

## How to Run the Application

- **Terminal 1**: Run the script to start the first user instance. You'll be prompted to enter a listening port number. After entering the port, this instance will listen for incoming connections.
- **Terminal 2**: Start the script for the second user and follow the same steps. Enter a different listening port number for this instance, then enter the first user's port number when prompted to connect.

## Usage Instructions

- **To Send Messages**: Type your message into the console and press Enter. The message will be sent to the connected user.
- **To Send Files**: Enter `transfer <filename>` (replace `<filename>` with the actual file name you wish to send, and ensure the file is in the same directory as the script). The file will be sent in chunks.
- The received file will be saved as `fetched_<filename>` in the same directory.
- **To Exit**: Type `terminate123` and press Enter. This command will safely close all connections and stop the program.

## Connection Flow

1. **Listening for Connections**: Each instance of the application listens on a specified port.
2. **Establishing a Connection**: Enter the target user's port number to establish a connection.
3. **Data Transmission**: Once connected, you can start sending messages or files.
4. **Receiving Data**: The application automatically handles incoming data, displaying messages and saving received files prefixed with `fetched_`.

## Error Handling

The application includes basic error handling for network errors, file transfer issues, and user exit commands.

## Clean Shutdown

Typing `terminate123` will shut down both sending and receiving functions, close all sockets, and terminate the application gracefully.

---
