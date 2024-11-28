

import subprocess
import simpleaudio as sa
import time
import re

def generate_filename_from_text(text, max_words=5):
    # Extract the first few words and sanitize for filename
    sanitized_text = re.sub(r'[^a-zA-Z0-9]+', '_', ' '.join(text.split()[:max_words]))
    return f"{sanitized_text}.wav"

def synthesize_and_play_piper_simpleaudio(text, model_path):
    # Run Piper to generate a temporary raw audio file
    raw_audio_file = "piper_tts_output.raw"
    with open(raw_audio_file, "wb") as audio_file:
        process = subprocess.Popen(
            ["piper", "--model", model_path, "--output-raw"],
            stdin=subprocess.PIPE,
            stdout=audio_file
        )
        process.stdin.write(text.encode('utf-8'))
        process.stdin.close()
        process.wait()

    # Read the raw audio data and play it with simpleaudio
    with open(raw_audio_file, "rb") as audio_file:
        raw_audio = audio_file.read()
        wave_obj = sa.WaveObject(raw_audio, num_channels=1, bytes_per_sample=2, sample_rate=22050)
        play_obj = wave_obj.play()
        play_obj.wait_done()

def play_meditation_script(script, model_path):
    for phrase in script["phrases"]:
        text = phrase["text"]
        pause_duration = phrase["pause"] / 1000  # Convert milliseconds to seconds
        generate_filename_from_text(text)
        # Synthesize and play the text
        synthesize_and_play_piper_simpleaudio(text, model_path)
        
        # Pause for the specified duration
        time.sleep(pause_duration)

# Path to your Piper model
model_path = "./voices/amy/en_US-amy-medium.onnx"
# model_path = "/home/shamimkhaled/piper-tts/voices/kristin/en_US-kristin-medium.onnx"

# Meditation script
script = {
    "phrases": [
        {"text": "Begin by finding a comfortable position, either sitting or lying down.", "pause": 2000},
        {"text": "Close your eyes gently, and take a deep breath in through your nose.", "pause": 2000},
        {"text": "Feel your chest and abdomen expand as you inhale.", "pause": 2000},
        {"text": "Now, slowly exhale through your mouth, releasing any tension.", "pause": 2000},
        {"text": "As you continue to breathe, notice the sensation of the air entering and leaving your body.", "pause": 2000},
        {"text": "Let your breath flow naturally, without forcing it.", "pause": 2000},
        {"text": "If your mind begins to wander, gently bring your focus back to your breath.", "pause": 2000},
        {"text": "Inhale deeply, filling your lungs with air, and then exhale fully.", "pause": 2000},
        {"text": "Allow yourself to be present in this moment of tranquility.", "pause": 2000},
        {"text": "Continue to breathe slowly and deeply, embracing each breath.", "pause": 2000}
    ]
}

# Play the meditation script
play_meditation_script(script, model_path)
print("Meditation script has been played.")
# 3.10