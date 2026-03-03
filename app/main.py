import socket  # noqa: F401
import asyncio

async def handle_client(connection):
    while True:
        BUFFER_SIZE_BYTES = 1024
        data = await connection.recv(BUFFER_SIZE_BYTES)

        if data:
            # send response to the client
            await connection.sendall(b"+PONG\r\n")
        else:
            # data is empty means connection is closed
            break


async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        # Block untill we recieve an incoming connection
        connection, address = server_socket.accept() 
        
        # run handle_client in asynchronus to handle multiple clients concurrently
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, handle_client, (connection))

if __name__ == "__main__":
    asyncio.run(main())
