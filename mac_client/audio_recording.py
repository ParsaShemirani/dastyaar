import pyaudio
import wave
import threading
import subprocess
import os


output_directory = '/Users/parsashemirani/Main/dastyaar'
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

