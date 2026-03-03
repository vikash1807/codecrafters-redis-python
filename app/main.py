import socket  # noqa: F401
import threading

def handle_connection(conn):
    while True:
        BUFFER_SIZE_BYTES = 1024
        data = conn.recv(BUFFER_SIZE_BYTES)

        if data:
            # send response to the client
            conn.sendall(b"+PONG\r\n")
        else:
            # data is empty means connection is closed
            break


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        # Block untill we recieve an incoming connection
        conn, address = server_socket.accept() 
        
        # add handle_connection in thread to handle multiple clients concurrently
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()


if __name__ == "__main__":
    main()
