import asyncio
import websockets

async def websocket_server(websocket, path):
    try:
        async for message in websocket:
            # Process WebSocket messages here
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed unexpectedly.")

async def main():
    server = await websockets.serve(websocket_server, 'localhost', 8765)
    print("WebSocket server running at ws://localhost:8765")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
