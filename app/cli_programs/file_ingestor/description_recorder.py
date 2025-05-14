import os
import sys
import pyaudio
import wave
import subprocess
import threading
from app.tools.openai.functions import get_transcription, tag_generator_from_description

class AudioRecorder:
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.frames = []
        self.recording = False
        self.stop_recording = False
        self.audio = None
        
        # Setup paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_audio_dir = os.path.join(self.script_dir, "tempaudio")
        self.wav_output_path = os.path.join(self.temp_audio_dir, "output.wav")
        self.mp3_output_path = os.path.join(self.temp_audio_dir, "output.mp3")
        
        # Ensure temp directory exists
        if not os.path.exists(self.temp_audio_dir):
            os.makedirs(self.temp_audio_dir)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensure cleanup"""
        self.cleanup_files()
        if self.audio:
            self.audio.terminate()

    def record_audio(self):
        """Record audio in a separate thread"""
        try:
            self.audio = pyaudio.PyAudio()
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.recording = True
            print("Recording... Press Enter to stop.")
            
            while not self.stop_recording:
                data = stream.read(self.chunk, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            print(f"Error during recording: {e}")
            self.stop_recording = True
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()

    def start_recording(self):
        """Start the recording process"""
        try:
            print("Press Enter to start recording...")
            input()
            
            recording_thread = threading.Thread(target=self.record_audio)
            recording_thread.start()
            
            input()  # Wait for Enter to stop recording
            self.stop_recording = True
            recording_thread.join()
            
            print("Recording stopped.")
        except KeyboardInterrupt:
            print("\nRecording interrupted.")
            self.stop_recording = True
            return False
        return True

    def save_audio(self):
        """Save the recorded audio as WAV and convert to MP3"""
        if not self.frames:
            print("No audio recorded")
            return False

        try:
            # Save WAV
            with wave.open(self.wav_output_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            # Convert to MP3
            print("Converting to MP3...")
            subprocess.run([
                'ffmpeg', '-y', '-i', self.wav_output_path,
                '-b:a', '64k', self.mp3_output_path
            ], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error converting to MP3: {e}")
            print("Make sure FFmpeg is installed and available in your PATH.")
            return False
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False

    def cleanup_files(self):
        """Clean up temporary audio files"""
        try:
            if os.path.exists(self.wav_output_path):
                os.remove(self.wav_output_path)
            if os.path.exists(self.mp3_output_path):
                os.remove(self.mp3_output_path)
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def verify_files(self):
        """Verify that both WAV and MP3 files exist"""
        return os.path.exists(self.wav_output_path) and os.path.exists(self.mp3_output_path)

def main():
    """Main function to handle the recording process"""
    while True:
        try:
            with AudioRecorder() as recorder:
                if not recorder.start_recording():
                    return None
                
                if not recorder.save_audio():
                    return None
                    
                if recorder.verify_files():
                    print(f"MP3 file saved: {recorder.mp3_output_path}")
                    
                    print("Transcription:")
                    transcription = get_transcription(recorder.mp3_output_path)
                    print(transcription)
                    
                    redo = input("Redo recording? (y/n): ").strip().lower()
                    if redo == 'y':
                        print("Restarting recording process...")
                        continue
                    else:
                        print("Recording complete.")
                        return transcription
                else:
                    print("Error: Output files not found.")
                    return None
        except KeyboardInterrupt:
            print("\nRecording process interrupted.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

if __name__ == "__main__":
    main()
