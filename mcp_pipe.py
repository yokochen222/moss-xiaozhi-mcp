"""
This script is used to connect to the MCP server and pipe the input and output to the websocket endpoint.
Version: 0.1.0

Usage:

export MCP_ENDPOINT=<mcp_endpoint>
python mcp_pipe.py <mcp_script>

"""

import asyncio
import websockets
import subprocess
import logging
import os
import signal
import sys
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MCP_PIPE')

# Reconnection settings
INITIAL_BACKOFF = 1  # Initial wait time in seconds
MAX_BACKOFF = 60  # Maximum wait time in seconds
reconnect_attempt = 0
backoff = INITIAL_BACKOFF

async def connect_with_retry(uri):
    """Connect to WebSocket server with retry mechanism"""
    global reconnect_attempt, backoff
    while True:  # Infinite reconnection
        try:
            if reconnect_attempt > 0:
                wait_time = backoff * (1 + random.random() * 0.1)  # Add some random jitter
                logger.info(f"Waiting {wait_time:.2f} seconds before reconnection attempt {reconnect_attempt}...")
                await asyncio.sleep(wait_time)
                
            # Attempt to connect
            await connect_to_server(uri)
        
        except Exception as e:
            reconnect_attempt += 1
            logger.warning(f"Connection closed (attempt: {reconnect_attempt}): {e}")            
            # Calculate wait time for next reconnection (exponential backoff)
            backoff = min(backoff * 2, MAX_BACKOFF)

async def connect_to_server(uri):
    """Connect to WebSocket server and establish bidirectional communication with `mcp_script`"""
    global reconnect_attempt, backoff
    try:
        logger.info(f"Connecting to WebSocket server...")
        async with websockets.connect(uri) as websocket:
            logger.info(f"Successfully connected to WebSocket server")
            # Reset reconnection counter if connection closes normally
            reconnect_attempt = 0
            backoff = INITIAL_BACKOFF
            
            # Start mcp_script process
            process = subprocess.Popen(
                ['python', mcp_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Use text mode
            )
            logger.info(f"Started {mcp_script} process")
            
            # Create two tasks: read from WebSocket and write to process, read from process and write to WebSocket
            await asyncio.gather(
                pipe_websocket_to_process(websocket, process),
                pipe_process_to_websocket(process, websocket),
                pipe_process_stderr_to_terminal(process)
            )
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"WebSocket connection closed: {e}")
        raise  # Re-throw exception to trigger reconnection
    except Exception as e:
        logger.error(f"Connection error: {e}")
        raise  # Re-throw exception
    finally:
        # Ensure the child process is properly terminated
        if 'process' in locals():
            logger.info(f"Terminating {mcp_script} process")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            logger.info(f"{mcp_script} process terminated")

async def pipe_websocket_to_process(websocket, process):
    """Read data from WebSocket and write to process stdin"""
    try:
        while True:
            # Read message from WebSocket
            message = await websocket.recv()
            logger.debug(f"<< {message[:120]}...")
            print('message', message)
            # Write to process stdin (in text mode)
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            process.stdin.write(message + '\n')
            process.stdin.flush()
    except Exception as e:
        logger.error(f"Error in WebSocket to process pipe: {e}")
        raise  # Re-throw exception to trigger reconnection
    finally:
        # Close process stdin
        if not process.stdin.closed:
            process.stdin.close()

async def pipe_process_to_websocket(process, websocket):
    """Read data from process stdout and send to WebSocket"""
    try:
        while True:
            # Read data from process stdout
            data = await asyncio.get_event_loop().run_in_executor(
                None, process.stdout.readline
            )
            
            if not data:  # If no data, the process may have ended
                logger.info("Process has ended output")
                break
                
            # Send data to WebSocket
            logger.debug(f">> {data[:120]}...")
            # In text mode, data is already a string, no need to decode
            await websocket.send(data)
    except Exception as e:
        logger.error(f"Error in process to WebSocket pipe: {e}")
        raise  # Re-throw exception to trigger reconnection

async def pipe_process_stderr_to_terminal(process):
    """Read data from process stderr and print to terminal"""
    try:
        while True:
            # Read data from process stderr
            data = await asyncio.get_event_loop().run_in_executor(
                None, process.stderr.readline
            )
            
            if not data:  # If no data, the process may have ended
                logger.info("Process has ended stderr output")
                break
                
            # Print stderr data to terminal (in text mode, data is already a string)
            sys.stderr.write(data)
            sys.stderr.flush()
    except Exception as e:
        logger.error(f"Error in process stderr pipe: {e}")
        raise  # Re-throw exception to trigger reconnection

def signal_handler(sig, frame):
    """Handle interrupt signals"""
    logger.info("Received interrupt signal, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # mcp_script
    if len(sys.argv) < 2:
        logger.error("Usage: mcp_pipe.py <mcp_script>")
        sys.exit(1)
    
    mcp_script = sys.argv[1]
    
    # Get token from environment variable or command line arguments
    endpoint_url = os.environ.get('MCP_ENDPOINT')
    if not endpoint_url:
        logger.error("Please set the `MCP_ENDPOINT` environment variable")
        sys.exit(1)
    
    # Start main loop
    try:
        asyncio.run(connect_with_retry(endpoint_url))
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Program execution error: {e}")