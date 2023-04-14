import os
import glob
import speech_recognition as sr

# Function to transcribe an audio file given its file path
def transcribe_audio_file(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
    try:
        transcribed_text = r.recognize_google(audio_data)  # Perform transcription using Google Speech Recognition
        return transcribed_text
    except sr.UnknownValueError:
        print(f"Transcription could not be performed for file: {audio_file_path}. Audio file may be empty or contain unintelligible speech.")
    except sr.RequestError as e:
        print(f"An error occurred for file: {audio_file_path}. Error: {e}")
    return None

# Function to write the transcribed text to a Markdown file
def write_to_markdown(output_file_path, transcribed_text):
    with open(output_file_path, 'w') as file:
        file.write("# Interview Transcription\n\n")
        paragraphs = transcribed_text.split('\n\n')  # Split the transcribed text into paragraphs
        question_count = 1  # Counter for question number
        for i, paragraph in enumerate(paragraphs):
            if "Question" in paragraph:
                file.write(f"**Q{question_count}:** {paragraph}\n\n")  # Write questions with Q and question number
                question_count += 1
            else:
                file.write(f"**Speaker {i+1}:** {paragraph}\n\n")  # Write speaker paragraphs with Speaker and speaker number

# Function to transcribe all files in a folder
def transcribe_all_files(folder_path):
    audio_files = glob.glob(os.path.join(folder_path, "*.mp3"))  # Get a list of all MP3 files in the folder
    for audio_file in audio_files:
        transcribed_text = transcribe_audio_file(audio_file)  # Transcribe the audio file
        if transcribed_text:
            output_file = os.path.splitext(audio_file)[0] + ".md"  # Generate the output file name with .md extension
            write_to_markdown(output_file, transcribed_text)  # Write transcribed text to Markdown file
            print(f"Transcription saved to Markdown file: {output_file}")

# Main function
def main():
    interviews_folder_path = "interviews"  # Folder path where the MP3 files are stored
    transcribe_all_files(interviews_folder_path)  # Transcribe all MP3 files in the folder

if __name__ == "__main__":
    main()