import asyncio

cmd_dict = {}

def parse_resp(cmd : str):
    lines : list = cmd.split("\r\n")
    idx = 0


    if lines[idx].startswith('*'):

        count = int(lines[idx][1:])
        idx += 1

        elements = []
        for _ in range(count):
            # parse bulk string
            if lines[idx].startswith('$'):
                length = int(lines[idx][1:])
                idx += 1

                if length:
                    value = lines[idx]
                    idx += 1
                    elements.append(value)
                else:
                    elements.append(None)
            
            else:
                idx += 1
        
        return elements
    return []


def encode_bulk_string(value: str) -> bytes:
    return f"${len(value)}\r\n{value}\r\n".encode()

    
async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:

    while True:
        addr, port = writer.get_extra_info("peername")
        print(f"message from {addr}:{port}")

        data = await reader.read(1024)

        if not data:
            break

        # parse command
        cmd = data.decode()
        elements = parse_resp(cmd)

        if not elements:
            continue

        cmd = elements[0].upper()
        args = elements[1:]

        if cmd == "ECHO":
            if args:
                writer.write(encode_bulk_string(args[0]))
                await writer.drain()
        
        elif cmd == "PING":
            writer.write(b"+PONG\r\n")
            await writer.drain()

        elif cmd == "SET":
            cmd_dict[args[0]] = args[1]
            writer.write(b'+OK\r\n')
            await writer.drain()
        
        elif cmd == "GET":
            writer.write(cmd_dict[args[0]].encode())
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
