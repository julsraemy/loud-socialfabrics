import os
import speech_recognition as sr
import wave
import datetime
import torch
from tqdm import tqdm
from transformers import WhisperForCTC, WhisperTokenizer

def get_audio_metadata(file_path):
    with wave.open(file_path, 'r') as audio_file:
        sample_rate = audio_file.getframerate()
        num_channels = audio_file.getnchannels()
        num_frames = audio_file.getnframes()
        duration = num_frames / sample_rate

    return sample_rate, num_channels, duration

def transcribe_audio(file_path):
    sample_rate, num_channels, duration = get_audio_metadata(file_path)

    tokenizer = WhisperTokenizer.from_pretrained("facebook/whisper-lv60")

    model = WhisperForCTC.from_pretrained("facebook/whisper-lv60")
    model.to(torch.device("cpu"))

    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    audio_text = ""
    for chunk in tqdm(audio.chunks(), desc="Transcribing audio"):
        text = r.recognize_sphinx(chunk)
        audio_text += text + " "

    tokens = tokenizer(audio_text, return_tensors="pt", padding=True).input_values
    with torch.no_grad():
        logits = model(tokens).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcribed_text = tokenizer.batch_decode(predicted_ids)[0]

    # Splitting into paragraphs based on silence longer than 2 seconds
    paragraphs = []
    current_paragraph = ""
    silence_threshold = 2  # Pause duration in seconds
    silence_duration = 0
    for line in transcribed_text.splitlines():
        if line.strip():
            current_paragraph += line + " "
            silence_duration = 0
        else:
            silence_duration += 1
            if silence_duration >= silence_threshold and current_paragraph:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    output_file_path = os.path.splitext(file_path)[0] + ".md"
    with open(output_file_path, 'w') as f:
        f.write(f"# Audio File Information\n\n")
        f.write(f"- Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- Duration: {int(duration)} seconds\n\n")
        f.write(f"# Transcription\n\n")
        for i, paragraph in enumerate(paragraphs):
            if paragraph.startswith("First question") or paragraph.startswith("Next question"):
                f.write(f"\n\nQ{i+1} {paragraph}\n")
            else:
                f.write(paragraph + "\n")

    print(f"Transcription saved to Markdown file: {output_file_path}")

def transcribe_all_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".wav"):
            transcribe_audio(file_path)

interviews_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "interviews")
transcribe_all_files(interviews_folder_path)
