import os
import time
import numpy as np
import pyaudio
import wave
import soundfile as sf
import google.generativeai as genai


genai.configure(api_key="")

# Audio Settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Sample rate
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 30  # Duration to record when triggered
THRESHOLD_MULTIPLIER = 1.5  # Multiplier for threshold

# Initialize PyAudio
audio = pyaudio.PyAudio()

def get_average_sound_level(duration=30):
    """Calculates the average sound level over a given duration."""
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Calculating background noise level...")
    
    volume_readings = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        volume = np.abs(data).mean()
        volume_readings.append(volume)
    
    stream.stop_stream()
    stream.close()
    
    avg_volume = np.mean(volume_readings)
    print(f"Background noise level: {avg_volume}")
    return avg_volume

def record_audio(filename="alert_sound.wav", duration=RECORD_SECONDS):
    """Records audio for the specified duration and saves it to a file."""
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    
    print(f"Recording triggered for {duration} seconds...")
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()

    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"Audio saved as {filename}")
    return filename

def upload_to_gemini(path, mime_type="audio/wav"):
    """Uploads the recorded audio to Gemini API."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def analyze_audio(file_path):
    """Sends the recorded audio to Gemini for analysis."""
    file = upload_to_gemini(file_path)

    system_prompt = """You are an AI trained to analyze environmental sounds for wildlife conservation.
    The audio clip may contain:
    - Animal calls (e.g., birds, tigers, elephants).
    - Distress signals (animals in pain or distress).
    - Human noises (chainsaws, gunshots, voices indicating poaching).
    Please analyze the audio and determine:
    1. What sounds are present?
    2. Any signs of distress or illegal activity?
    3. The confidence level of detection.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-01-21",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 65536,
            "response_mime_type": "text/plain",
        },
    )

    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [file, system_prompt]}]
    )

    response = chat_session.send_message("Analyze the audio and provide a detailed report.")
    print("Gemini Response:\n", response.text)

def main():
    avg_volume = 130  # get_average_sound_level()
    threshold = avg_volume * THRESHOLD_MULTIPLIER
    print(f"Monitoring sounds... Alert threshold: {threshold}")

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    while True:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        volume = np.abs(data).mean()
        
        if volume > threshold:
            print(f"ALERT! High sound detected: {volume}")
            file_path = record_audio()
            analyze_audio(file_path)
            print("Resuming monitoring...")

if _name_ == "_main_":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping...")
        audio.terminate()