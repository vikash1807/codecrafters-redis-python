import asyncio


HOST = '127.0.0.1'
PORT = 6379


async def run_client():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    writer.write(b'ECHO hey')
    await writer.drain()

    while True:

        data = await reader.read(1024)
        if not data:
            raise Exception('socker connection closed')
        
        print(f"Recieved data : {data.decode()}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_client())