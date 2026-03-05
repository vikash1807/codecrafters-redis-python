import asyncio

STORAGE = {}

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

    
async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
) -> None:

    while True:
        addr, port = writer.get_extra_info("peername")
        print(f"message from {addr}:{port}")

        # read data from client
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

        match cmd:
            case "PING":
                writer.write(b"+PONG\r\n")

            case "ECHO":
                if args:
                    writer.write(encode_bulk_string(args[0]))

            case "SET":
                STORAGE[args[0]] = args[1]
                writer.write(b'+OK\r\n')
            
            case "GET":
                key = args[0]
                if key not in STORAGE:
                    writer.write(b'$-1\r\n')
                else:
                    writer.write(encode_bulk_string(STORAGE[key]))
            
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def run_server():
    HOST = '127.0.0.1'
    PORT = 6379

    server = await asyncio.start_server(
        handle_client,
        host=HOST,
        port=PORT
    )
    print(f"server runninng on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()



if __name__ == "__main__":
    asyncio.run(run_server())
