import speech_recognition as sr
import wave
import os

# Function to extract technical metadata from WAV files
def get_wav_metadata(file_path):
    with wave.open(file_path, 'r') as wav_file:
        sample_rate = wav_file.getframerate()
        bit_depth = wav_file.getsampwidth() * 8
        num_channels = wav_file.getnchannels()
    return sample_rate, bit_depth, num_channels

# Function to transcribe audio file and save to Markdown file
def transcribe_audio(file_path):
    # Extract file extension and check if WAV
    ext = os.path.splitext(file_path)[1]
    if ext == '.wav':
        sample_rate, bit_depth, num_channels = get_wav_metadata(file_path)
    else:
        print(f"Skipping file: {file_path}")
        return
    
    # Load audio file
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    
    # Transcribe audio
    try:
        transcribed_text = r.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        transcribed_text = "Speech recognition could not understand the audio."
    except sr.RequestError as e:
        transcribed_text = f"Could not request results from Google Speech Recognition service; {e}"
    
    # Write metadata and transcribed text to Markdown file
    output_file_path = os.path.splitext(file_path)[0] + ".md"
    with open(output_file_path, 'w') as f:
        f.write(f"# Technical Metadata\n\n")
        f.write(f"- Sample Rate: {sample_rate}\n")
        f.write(f"- Bit Depth: {bit_depth}\n")
        f.write(f"- Number of Channels: {num_channels}\n\n")
        f.write(f"# Transcription\n\n")
        f.write(transcribed_text)
    
    print(f"Transcription saved to Markdown file: {output_file_path}")

def transcribe_all_files(folder_path):
    audio_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for audio_file in audio_files:
        file_extension = os.path.splitext(audio_file)[1].lower()
        if file_extension == '.wav':
            audio_file_path = os.path.join(folder_path, audio_file)
            transcribe_audio(audio_file_path)
        else:
            print(f"Skipping file: {audio_file_path}")

if __name__ == "__main__":
    folder_path = 'interviews'
    transcribe_all_files(folder_path)
