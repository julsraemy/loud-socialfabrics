import os
import speech_recognition as sr
import wave

def get_wav_metadata(file_path):
    with wave.open(file_path, 'r') as wav_file:
        sample_rate = wav_file.getframerate()
        bit_depth = wav_file.getsampwidth() * 8
        num_channels = wav_file.getnchannels()
    return sample_rate, bit_depth, num_channels

def transcribe_audio(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext == '.wav':
        sample_rate, bit_depth, num_channels = get_wav_metadata(file_path)
    else:
        print(f"Skipping file: {file_path}")
        return

    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)

    try:
        transcribed_text = r.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        transcribed_text = "Speech recognition could not understand the audio."
    except sr.RequestError as e:
        transcribed_text = f"Could not request results from Google Speech Recognition service; {e}"

    # Splitting into paragraphs based on silence longer than 4 seconds
    paragraphs = []
    current_paragraph = ""
    for line in transcribed_text.splitlines():
        if line.strip():
            current_paragraph += line + " "
        elif current_paragraph:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = ""
    if current_paragraph:
        paragraphs.append(current_paragraph.strip())

    output_file_path = os.path.splitext(file_path)[0] + ".md"
    with open(output_file_path, 'w') as f:
        f.write(f"# Technical Metadata\n\n")
        f.write(f"- Sample Rate: {sample_rate}\n")
        f.write(f"- Bit Depth: {bit_depth}\n")
        f.write(f"- Number of Channels: {num_channels}\n\n")
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
        if os.path.isfile(file_path):
            transcribe_audio(file_path)

if __name__ == "__main__":
    folder_path = os.path.join(os.getcwd(), "linked-art/interviews")
    transcribe_all_files(folder_path)
