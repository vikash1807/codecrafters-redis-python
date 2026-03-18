import asyncio

from app.server import RedisServer

    
async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
) -> None:
    
    server = RedisServer(reader, writer)
    await server.serve()


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
