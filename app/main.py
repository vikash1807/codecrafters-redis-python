import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    # Block untill we recieve an incoming connection
    while(True):
        connection, address = server_socket.accept() 

        print(f"accepted connection from {address}")

        # send response to the client
        connection.sendall(b"+PONG\r\n")


if __name__ == "__main__":
    main()
