#!/usr/bin/env python3
import os
import sys
import pyaudio
import wave
import subprocess
import time
import threading
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def main():
    # Determine script directory and setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_audio_dir = os.path.join(script_dir, "tempaudio")
    
    # Create tempaudio directory if it doesn't exist
    if not os.path.exists(temp_audio_dir):
        os.makedirs(temp_audio_dir)
    
    # Define output paths
    wav_output_path = os.path.join(temp_audio_dir, "output.wav")
    mp3_output_path = os.path.join(temp_audio_dir, "output.mp3")
    
    # Audio parameters
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    
    while True:
        frames = []
        recording = False
        stop_recording = False
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        print("Press Enter to start recording...")
        input()  # Wait for Enter key
        
        # Function to capture audio
        def record_audio():
            nonlocal frames, recording, stop_recording
            # Open audio stream
            stream = audio.open(format=format, channels=channels,
                                rate=rate, input=True,
                                frames_per_buffer=chunk)
            
            recording = True
            print("Recording... Press Enter to stop.")
            
            # Record audio frames until stop flag is set
            while not stop_recording:
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
        
        # Start recording in a thread
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()
        
        # Wait for user to press Enter to stop recording
        input()
        stop_recording = True
        recording_thread.join()
        
        print("Recording stopped.")
        audio.terminate()
        
        # Save as WAV file
        with wave.open(wav_output_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
        
        # Convert to MP3 using FFmpeg
        print("Converting to MP3...")
        try:
            subprocess.run([
                'ffmpeg', '-y', '-i', wav_output_path, 
                '-b:a', '64k', mp3_output_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Error: FFmpeg conversion failed. Make sure FFmpeg is installed and in your PATH.")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: FFmpeg not found. Please install FFmpeg and ensure it's available in your PATH.")
            sys.exit(1)
        
        # Verify files exist
        if os.path.exists(wav_output_path) and os.path.exists(mp3_output_path):
            print(f"MP3 file saved: {mp3_output_path}")
            
            #PRINT TRANSCRIPTION
            print("Transcription:")
            transcription = transcriber()
            print(transcription)
            # Prompt for redo
            redo = input("Redo recording? (y/n): ").strip().lower()
            if redo == 'y':
                # Delete files and restart
                if os.path.exists(wav_output_path):
                    os.remove(wav_output_path)
                    print("Deleted WAV file.")
                
                if os.path.exists(mp3_output_path):
                    os.remove(mp3_output_path)
                    print("Deleted MP3 file.")
                
                print("Restarting recording process...")
            else:
                print("Recording complete.")
                return transcription
        else:
            print("Error: Output files not found.")
            break





def transcriber():
    client = OpenAI()
    #GETTING NAME
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_audio_dir = os.path.join(script_dir, "tempaudio")
    mp3_output_path = os.path.join(temp_audio_dir, "output.mp3")
    audio_file= open(mp3_output_path, "rb")
    #CREATING TRANSCRIPTION
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text



def tag_generator(description):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o-mini",

        instructions="""
        Observe the description provided through the input. Come up
        with up to 8 key word tags that you can attribute to the description based on its content.
        These tags are used to describe a file, and will be used later to find files based on
        things like key people mentioned in the description, places, events, people, activites, etc.
        Exclude any words that dont contribute much meaning to the description.

        Repond with a comma seperated list of these values, no spaces between commas, all lowercase.

        Example description: My family and I are visiting Daii Joons house and
        we went to the nearby resturant and ate together. We also saw Richard on the way there
        while we were on the bus

        Repsonse: "family,resturant,daii joon,richard,bus,

        """,

        input = description
    )

    return response.output_text

#tester = tag_generator("My friend Richard and I were on the bus going to target to pick up my Sony camera. This is a selfie as we are on the bus.")

#print(tester)


if __name__ == "__main__":
    main()

    