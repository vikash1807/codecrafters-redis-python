import asyncio

# def parse_command(command : str):
#     cmd, msg = command.split(" ")

#     if cmd == 'ECHO':



async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:

    while True:
        data = await reader.read(1024)

        if not data:
            break

        command = data.decode()
        print(f"Recieved command : {command}")

        # parsed_msg = parse_command(command)
        cmd, msg = command.split(" ")

        addr, port = writer.get_extra_info("peername")

        print(f"message from {addr}:{port}: {msg}")

        if cmd == "ECHO":
            writer.write(msg.encode())
            await writer.drain()
        
        elif cmd == "PING":
            writer.write(b"+PONG\r\n")
            await writer.drain()
            


    writer.close()
    await writer.wait_closed()


async def main():
    HOST = '127.0.0.1'
    PORT = 6379

    server = await asyncio.start_server(
        handle_connection,
        host=HOST,
        port=PORT
    )
    print(f"server runninng on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
