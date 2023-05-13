import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment, silence


def extract_audio_from_video(input_file, output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)


def truncate_silence(audio_file, lower_bound=100, upper_bound=700, required_silence_lower=100,
                     required_silence_upper=400):
    # Carica l'audio
    audio = AudioSegment.from_mp3(audio_file)

    # Trova le posizioni del silenzio
    silence_spots = silence.detect_silence(audio, min_silence_len=lower_bound, silence_thresh=-16)

    # Creazione del nuovo audio segment
    new_audio_segment = AudioSegment.empty()
    for start, end in silence_spots:
        if end - start > upper_bound:
            new_audio_segment += AudioSegment.silent(duration=required_silence_upper)
        else:
            new_audio_segment += AudioSegment.silent(duration=required_silence_lower)
        new_audio_segment += audio[start:end]

    # Esporta l'audio troncato
    new_audio_segment.export(audio_file, format="mp3")


def process_videos(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp4"):
            print(f"Processing file: {filename}")  # Aggiungi questa riga
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".mp3")

            # Estrai l'audio dal video
            print("Extracting audio...")  # Aggiungi questa riga
            extract_audio_from_video(input_file, output_file)

            # Tronca il silenzio
            print("Truncating silence...")  # Aggiungi questa riga
            truncate_silence(output_file)


if __name__ == "__main__":
    process_videos(r"C:\Users\Alessio\Desktop\testinput", r"C:\Users\Alessio\Desktop\testoutput")