import asyncio

HOST = "127.0.0.1"
PORT = 6379


def encode_command(*parts: str) -> bytes:
    """
    Convert command to RESP format
    Example:
    SET a 10  ->
    *3\r\n$3\r\nSET\r\n$1\r\na\r\n$2\r\n10\r\n
    """
    cmd = f"*{len(parts)}\r\n"
    for p in parts:
        cmd += f"${len(p)}\r\n{p}\r\n"
    return cmd.encode()


async def run_client():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    print(f"Connected to {HOST}:{PORT}")
    print("Type commands like: SET a 10")
    print("Type 'exit' to quit\n")

    while True:
        try:
            user_input = input("redis> ")

            if not user_input:
                continue

            if user_input.lower() == "exit":
                break

            parts = user_input.strip().split()

            data = encode_command(*parts)

            writer.write(data)
            await writer.drain()

            resp = await reader.read(1024)

            if not resp:
                print("Connection closed")
                break

            print(resp.decode())

        except KeyboardInterrupt:
            break

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(run_client())