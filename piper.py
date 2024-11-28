import subprocess
import simpleaudio as sa
import time
import re
import os
from pathvalidate import sanitize_filename

def generate_filename_from_text(text, max_words=5):
    # Extract the first few words and sanitize for filename
    words = text.split()[:max_words]
    raw_filename = '_'.join(words)
    sanitized_filename = sanitize_filename(raw_filename)
    return f"{sanitized_filename}.wav"

def get_voice_name_from_model_path(model_path):
    # Extract the voice name from the model path
    match = re.search(r"/voices/([^/]+)/", model_path)
    return match.group(1) if match else "unknown_voice"

def synthesize_and_save_piper_audio(text, model_path, output_path):
    # Run Piper to generate a raw audio file
    with open(output_path, "wb") as audio_file:
        process = subprocess.Popen(
            ["piper", "--model", model_path, "--output_file", output_path],
            stdin=subprocess.PIPE
        )
        process.stdin.write(text.encode('utf-8'))
        process.stdin.close()
        process.wait()

def play_audio_file(file_path):
    # Play the audio file using simpleaudio
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def play_meditation_script(script, model_path):
    # Get the voice name from the model path
    voice_name = get_voice_name_from_model_path(model_path)
    
    # Ensure the output directory for the voice exists
    voice_folder_path = f"./audio_files/{voice_name}"
    os.makedirs(voice_folder_path, exist_ok=True)

    for phrase in script["phrases"]:
        text = phrase["text"]
        pause_duration = phrase["pause"] / 1000  # Convert milliseconds to seconds
        tts_duration = phrase["tts_duration"] / 1000  # Convert milliseconds to seconds

        # Generate a unique filename for each phrase
        output_filename = generate_filename_from_text(text)
        output_path = f"{voice_folder_path}/{output_filename}"

        # Synthesize and save the audio
        synthesize_and_save_piper_audio(text, model_path, output_path)

        # Play the audio
        play_audio_file(output_path)
        
        # Wait for the TTS duration and then the specified pause duration
        time.sleep(pause_duration)

# Meditation script
script = {
    "phrases": [
        {
            "text": "Welcome to this Breath Awareness Meditation.",
            "pause": 10000,
            "tts_duration": 5000
        },
        {
            "text": "Find a comfortable position, sitting or lying down.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "Close your eyes gently and take a deep breath in.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "Hold that breath for a moment.",
            "pause": 10000,
            "tts_duration": 4000
        },
        {
            "text": "Now, exhale slowly and fully.",
            "pause": 10000,
            "tts_duration": 5000
        },
        {
            "text": "With each breath, allow yourself to relax deeper.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "Focus on the sensation of your breath entering and leaving your body.",
            "pause": 10000,
            "tts_duration": 7000
        },
        {
            "text": "As thoughts arise, gently acknowledge them and return your focus to your breath.",
            "pause": 10000,
            "tts_duration": 8000
        },
        {
            "text": "Breathe in calm, and breathe out tension.",
            "pause": 10000,
            "tts_duration": 5000
        },
        {
            "text": "You are capable and competent.",
            "pause": 10000,
            "tts_duration": 4000
        },
        {
            "text": "Continue this rhythm, in and out, at your own pace.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "As you breathe, visualize a calming light surrounding you.",
            "pause": 10000,
            "tts_duration": 7000
        },
        {
            "text": "Feel this light washing over you, bringing peace and clarity.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "When you're ready, start to bring your awareness back to the room.",
            "pause": 10000,
            "tts_duration": 7000
        },
        {
            "text": "Wiggle your fingers and toes gently.",
            "pause": 10000,
            "tts_duration": 4000
        },
        {
            "text": "Open your eyes slowly, returning to the present moment.",
            "pause": 10000,
            "tts_duration": 6000
        },
        {
            "text": "Thank you for taking this time to nurture yourself.",
            "pause": 10000,
            "tts_duration": 5000
        }
    ],
    "interval": 10000,
    "engagement": 10
}

# Path to your Piper model
# model_path = "/home/shamimkhaled/piper-tts/voices/amy/en_US-amy-medium.onnx"
model_path = "./voices/kristin/en_US-kristin-medium.onnx"

# Ensure the output directory exists
os.makedirs("./audio_files", exist_ok=True)

# Play the meditation script
play_meditation_script(script, model_path)
