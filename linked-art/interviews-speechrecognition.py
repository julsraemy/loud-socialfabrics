import os
import glob
import speech_recognition as sr
from pydub import AudioSegment

def convert_to_wav(mp3_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    wav_file_path = os.path.splitext(mp3_file_path)[0] + ".wav"
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def transcribe_audio_file(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
    try:
        transcribed_text = r.recognize_google(audio_data)
        return transcribed_text
    except sr.UnknownValueError:
        print(f"Transcription could not be performed for file: {audio_file_path}. Audio file may be empty or contain unintelligible speech.")
    except sr.RequestError as e:
        print(f"An error occurred for file: {audio_file_path}. Error: {e}")
    return None

def write_to_markdown(output_file_path, transcribed_text):
    with open(output_file_path, 'w') as file:
        file.write("# Interview Transcription\n\n")
        paragraphs = transcribed_text.split('\n\n')
        question_count = 1
        new_paragraph = False
        for i, paragraph in enumerate(paragraphs):
            if "First question" in paragraph:
                new_paragraph = True
                continue
            elif "Next question" in paragraph:
                new_paragraph = True
                question_count += 1
                continue

            if new_paragraph:
                file.write("\n\n")
                new_paragraph = False

            if "Question" in paragraph:
                file.write(f"**Q{question_count}:** {paragraph}\n\n")
                question_count += 1
            else:
                file.write(f"**Speaker {i+1}:** {paragraph}\n\n")

def transcribe_all_files(folder_path):
    audio_files = glob.glob(os.path.join(folder_path, "*.mp3"))
    for audio_file in audio_files:
        wav_file = convert_to_wav(audio_file)
        transcribed_text = transcribe_audio_file(wav_file)
        if transcribed_text:
            output_file = os.path.splitext(audio_file)[0] + ".md"
            write_to_markdown(output_file, transcribed_text)
            print(f"Transcription saved to Markdown file: {output_file}")
        os.remove(wav_file)  # Remove the temporary WAV file

def main():
    interviews_folder_path = "interviews"
    transcribe_all_files(interviews_folder_path)

if __name__ == "__main__":
    main()
