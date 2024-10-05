# Import socket module
from socket import *
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Listen for incoming connections
    
    print("Server is ready to serve on port", port)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept a connection
        
        try:
            message = connectionSocket.recv(1024).decode()  # A client is sending you a message
            filename = message.split()[1]  # Extract the filename from the request
            
            # Opens the client requested file
            with open(filename[1:], 'rb') as f:  # Open the file in binary mode
                outputdata = f.read()  # Read the file content

            # Send HTTP response headers
            header = b"HTTP/1.1 200 OK\r\n"
            header += b"Content-Type: text/html; charset=UTF-8\r\n"
            header += b"\r\n"  # End of headers
            
            # Send the response headers and file content to the client
            connectionSocket.send(header + outputdata)

        except IOError:
            # Send response message for invalid request due to the file not being found (404)
            error_header = b"HTTP/1.1 404 Not Found\r\n"
            error_header += b"Content-Type: text/html; charset=UTF-8\r\n"
            error_header += b"\r\n"
            error_message = b"<html><body><h1>404 Not Found</h1></body></html>"
            
            connectionSocket.send(error_header + error_message)

        finally:
            # Close client socket
            connectionSocket.close()  # Closing the connection socket

    # Uncomment the below lines if you want to close the server socket on exit
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
