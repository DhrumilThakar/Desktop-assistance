import asyncio
import websockets
import json
from main import say, take_input, save_reminder, save_note, tell_joke, get_wikipedia_summary
import threading
import queue

# Create a queue for communication between WebSocket and voice recognition
command_queue = queue.Queue()
response_queue = queue.Queue()

def voice_recognition_thread():
    """ Separate thread for handling voice recognition """
    while True:
        try:
            # Get command from queue
            command = command_queue.get()
            if command == "stop":
                break
                
            # Process voice input
            text = take_input()
            if text:
                response_queue.put({
                    'type': 'command',
                    'text': text
                })
                
                # Process the command and get response
                response = process_command(text)
                response_queue.put({
                    'type': 'response',
                    'text': response
                })
        except Exception as e:
            response_queue.put({
                'type': 'error',
                'text': str(e)
            })

def process_command(text):
    """ Process voice commands and return responses """
    # Open Websites
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["instagram", "https://www.instagram.com"],
        ["spotify", "https://www.spotify.com"],
        ["chatgpt", "https://chat.openai.com"]
    ]
    
    for site in sites:
        if f"open {site[0]}" in text:
            return f"Opening {site[0]}"

    # Weather Feature
    if "what's the weather" in text:
        return "Please tell me your location"

    # Wikipedia Search
    if "search for" in text:
        query = text.replace("search for", "").strip()
        return get_wikipedia_summary(query)

    # Jokes
    if "tell me a joke" in text:
        return tell_joke()

    # Default response
    return "I heard your command. How can I help you?"

async def handle_client(websocket, path):
    """ Handle WebSocket client connections """
    try:
        # Start voice recognition thread
        voice_thread = threading.Thread(target=voice_recognition_thread)
        voice_thread.daemon = True
        voice_thread.start()

        while True:
            try:
                # Check for responses from voice recognition thread
                while not response_queue.empty():
                    response = response_queue.get()
                    await websocket.send(json.dumps(response))

                # Wait for messages from client
                message = await websocket.recv()
                data = json.loads(message)
                
                if data['type'] == 'start':
                    command_queue.put("start")
                elif data['type'] == 'stop':
                    command_queue.put("stop")
                    break
                elif data['type'] == 'feature':
                    feature = data['feature']
                    response = handle_feature(feature)
                    await websocket.send(json.dumps({
                        'type': 'response',
                        'text': response
                    }))
            
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'text': str(e)
                }))
    
    finally:
        # Clean up
        command_queue.put("stop")
        if voice_thread.is_alive():
            voice_thread.join()

def handle_feature(feature):
    """ Handle feature card clicks """
    feature_responses = {
        'weather': "Please tell me your location for weather information",
        'tasks': "Would you like to add, remove, or view tasks?",
        'notes': "What would you like me to note down?",
        'reminders': "What would you like me to remind you about?",
        'music': "Which genre would you like to play?",
        'system': "Would you like to shutdown or restart the system?"
    }
    return feature_responses.get(feature, "Feature not implemented yet")

async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main()) 