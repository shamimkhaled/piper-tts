import subprocess
import simpleaudio as sa
import time
import re
from pathvalidate import sanitize_filename

def generate_filename_from_text(text, max_words=5):
    # Extract the first few words and sanitize for filename
    words = text.split()[:max_words]
    raw_filename = '_'.join(words)
    sanitized_filename = sanitize_filename(raw_filename)
    return f"{sanitized_filename}.wav"



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
    for phrase in script["phrases"]:
        text = phrase["text"]
        pause_duration = phrase["pause"] / 1000  # Convert milliseconds to seconds

        # Generate a unique filename for each phrase
        output_filename = generate_filename_from_text(text)
        output_path = f"./audio_files/{output_filename}"

        # Synthesize and save the audio
        synthesize_and_save_piper_audio(text, model_path, output_path)

        # Play the audio
        play_audio_file(output_path)
        
        # Pause for the specified duration
        time.sleep(pause_duration)

model_path = "/home/shamimkhaled/piper-tts/voices/amy/en_US-amy-medium.onnx"

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

# Ensure the output directory exists
import os
os.makedirs("./audio_files", exist_ok=True)

# Play the meditation script
play_meditation_script(script, model_path)
