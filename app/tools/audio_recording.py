import pyaudio
import wave
import threading
import subprocess
import os
from  app.tools import open_ai_transcriber
from app.tools.settings import AUDIO_OUTPUT_DIRECTORY

output_directory = AUDIO_OUTPUT_DIRECTORY
wav_recording = os.path.join(output_directory, "output.wav")
mp3_converted = os.path.join(output_directory, "output.mp3")

def record(
    chunk = 1024,
    format = pyaudio.paInt16,
    channels = 1,
    rate = 16000,
    filename = wav_recording,
    ):
    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=format,
        channels=channels,
        rate=rate,
        frames_per_buffer=chunk,
        input=True
    )
    frames = []

    def record_audio():
        while not stop.is_set():
            data = stream.read(chunk)
            frames.append(data)

    stop = threading.Event()
    t = threading.Thread(target=record_audio)
    t.start()
    input()
    stop.set()
    t.join()   

    stream.stop_stream()
    stream.close()
    pa.terminate()

    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pa.get_sample_size(format=format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def convert_to_mp3():
    subprocess.run(
        ["ffmpeg", "-i", wav_recording, mp3_converted],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    os.remove(wav_recording)

def interactive_transcribe():
    input("Press enter to start recording")
    record_again = True
    while record_again == True:
        record()
        convert_to_mp3()
        transcription = open_ai_transcriber.get_transcription(
            file_path=mp3_converted
        )
        os.remove(mp3_converted)
        print("Transcription:")
        print(transcription)

        choice = input("Press enter to approve, r to record again")
        record_again = False if choice == '' else True
    return transcription