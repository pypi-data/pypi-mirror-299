from websockets.sync.client import connect as cn
import threading

ws = None
_api_key = None
_symbol = 'GBPUSD'
message_callback = None  # Added callback variable


def set_ws_key(api_key):
    """Set the WebSocket API key."""
    global _api_key
    _api_key = api_key

def set_symbols(symbol):
    """Set the symbol to subscribe to."""
    global _symbol
    _symbol = symbol

def stream_data(callback):
    """Set the callback function to process incoming messages."""
    global message_callback
    message_callback = callback

def get_symbols():
    """Return the currently set symbol."""
    return _symbol

def api_key():
    """Return the currently set API key."""
    return _api_key

def on_message(message):
    """Handle incoming messages by calling the callback."""
    if message_callback:
        message_callback(message)

def on_error(error):
    """Handle WebSocket errors."""
    print(f"Error: {error}")

def on_close():
    """Handle WebSocket closure."""
    print("### WebSocket connection closed ###")

def on_open(websocket):
    """Handle WebSocket opening and send credentials to TraderMade."""
    cred = f'{{"userKey":"{_api_key}", "symbol":"{_symbol}"}}'
    websocket.send(cred)
    print(f"Sent credentials: {cred}")

def connect_tradermade():
    """Connect to the TraderMade WebSocket server."""
    global ws

    url = "wss://marketdata.tradermade.com/feedadv"
    try:
        with cn(url) as websocket:
            # Open WebSocket and send authentication
            on_open(websocket)

            # Continuously receive and process messages
            while True:
                try:
                    message = websocket.recv()
                    print(f"Received: {message}")
                    on_message(message)  # Call the message handler
                except Exception as e:
                    on_error(e)
                    break

    except Exception as e:
        on_error(e)

    finally:
        on_close()

# Start the streaming connection in a thread
def connect():
    thread = threading.Thread(target=connect_tradermade)
    thread.start()

