from openai import OpenAI
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, CompositeAudioClip
import json
import matplotlib.font_manager as fm
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

font_path = 'komika.ttf'
prop = fm.FontProperties(fname=font_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  #replace with your own openai api key
groqC = Groq(api_key=os.getenv("GROQ_API_KEY"))  #replace with your own groq api key

def gen_tts():
    with open("essay.txt", 'rb') as f:
        essay = f.read()

    response = groqC.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "system", "content": """You are a helpful content creator assistant.
                                      Your only role is to come up with human-sounding transcripts for a video given a large chunk of text, use uncomplicated language and don't paraphrase.
                                      Always start your response with Hello, then get into the transcript
                                      Based on the essay provided to you, pick a random chunk of the essay without changing the original text.
                                      Come up with a transcript that reiterates that chunk of the essay.
                                      Integrate who wrote this essay into the transcript, smoothly.
                                      Don't blabber; just straight up get into the textual part of the essay.
                                      Don't leave out much detail; add more text and as few cliffhangers as possible.
                                      Only use the text provided to you.
                                      Don't return any text that tells the user that this is a transcript.
                                      Limit your response to 4096 characters.
        """},
        {"role": "user", "content": f"here's the essay: {essay}"},
    ]
    )
    # print(response.choices[0].message.content)
    speechResponse = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=f"{response.choices[0].message.content}",
    )

    speechResponse.stream_to_file("transcript.mp3")


def gen_transcriptions():
    audio_file = open("transcript.mp3", "rb")

    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"],
    )

    print("transcription complete")

    json_file = "data.json"
    with open(json_file, 'w') as f:
        json.dump(transcript.words, f, indent=4)


def align_video_audio():
    video = VideoFileClip("footage.mp4")
    audio = AudioFileClip("transcript.mp3")
    bg_music = AudioFileClip("minecraft_bg.mp3")

    audio_length_sec = audio.duration
    bg_music = bg_music.subclip(0, audio_length_sec).volumex(0.1) 

    # Combine main audio with background music
    combined_audio = CompositeAudioClip([audio, bg_music])

    trimmed_video = video.subclip(0, audio_length_sec)
    trimmed_video = trimmed_video.set_audio(combined_audio)

    return trimmed_video


def group_words(segments, max_length):
    grouped = []
    current_group = []
    current_length = 0

    for segment in segments:
        word = segment['word']
        #conditionally determines if the word is too long or if the current group is too long
        if len(word) > max_length or current_length + len(word) > max_length: 
            #if it is then we append straight to parent list grouped
            if current_group:
                grouped.append(current_group)
            current_group = [segment]
            current_length = len(word)

        #if not, we append the word to the current group
        else:
            current_group.append(segment)
            current_length += len(word)

        if len(current_group) == 2:
            grouped.append(current_group)
            current_group = []
            current_length = 0

    if current_group:
        grouped.append(current_group)

    return grouped
    
    # the reason we store entire json objects here in grouped is 
    # because we need the start and end times for the captions below


def generate_captions():
    caption_clips = []
    with open ("data.json", "r") as f:
        segment_data = json.load(f)

    grouped_segments = group_words(segment_data, 10)

    for group in grouped_segments:
        text = ' '.join(segment['word'] for segment in group)
        start_time = group[0]['start']
        end_time = group[-1]['end']
        
        caption = TextClip(text, fontsize=50, color='white', font=font_path, stroke_color='black', stroke_width=1.5)
        caption = caption.set_position(('center')).set_start(start_time).set_end(end_time)
        caption_clips.append(caption)
        
    return caption_clips

def crop_render():
    #mobile resolution figured out through resizing rectangles in figma
    x1 = 600    # x-coordinate of the top-left corner
    y1 = 0      # y-coordinate of the top-left corner
    x2 = 1120   # x-coordinate of the bottom-right corner
    y2 = 1080   # y-coordinate of the bottom-right corner

    trimmed = align_video_audio()
    cropped = trimmed.crop(x1=x1, y1=y1, x2=x2, y2=y2)
    caption_clips = generate_captions()
    final_video = CompositeVideoClip([cropped] + caption_clips)

    final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac", threads=8)


def main():
    #gen_tts() #generates text + tts for text
    #gen_transcriptions() #timestamp transcription
    crop_render() #crops vid and renders with captions

if __name__ == "__main__":
    main()
