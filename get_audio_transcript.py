from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import os

save_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\Term Project\audio_files"

gradual_inebriation = ["uo3AXTIPqpg"]
all_inebriated = ["woDiIAQBCM4", "rQ63wo4XcDs", "yJJRVleE3_Q"]



def main():
    for id in video_list:
        temp_transcript = retrieve_transcript(id)
        nested_transcript_dict, clean_indices = find_longest_segments(temp_transcript)
        clean_audio_zip = concat_clean_audio(temp_transcript, clean_indices)
        # title = download_audio(id)
        # new_title = chop_audio(id, nested_transcript_dict, clean_indices)


def chop_audio(id, transcipt_dict, index_list):

    return True

"""count consecutive integers directly in front of the given value"""
def how_many_consec_in_front(index_list, val):
    in_front = 0
    val_index = index_list.index(val)
    if val != index_list[-1]:
        for temp_num in index_list:
            if temp_num == val:
                print('found value, heres the new list')
                print(index_list[val_index+1:])
                for next in index_list[val_index+1:]:
                    print('next  ', next)
                    if val + 1 == next:
                        in_front += 1
                        val = next
                    else:
                        return in_front
    return in_front

"""if there are consecutive clean audio clips, piece them and their transcripts together"""
def concat_clean_audio(transcript, index_list):
    last_val = 0
    clean_audio_zip = []
    for i in index_list:
        infront = how_many_consec_in_front(index_list, i)
        if infront == 0:
            ag_text = transcript[i]["text"]
            offsets = [transcript[i]["start"], transcript[i]["start"] + transcript[i]["duration"]]
            clean_audio_zip.append([ag_text, offsets])
        else:
            merge = " "
            ag_text = merge.join(transcript[i:i+infront+1])
            offsets = [transcript[i]["start"], transcript[i+infront]["start"] + transcript[i+infront]["duration"]]
            clean_audio_zip.append([ag_text, offsets])
    return clean_audio_zip


"""collect indicies for all speech sequents without non-words"""
def find_longest_segments(transcript):
    # print("TRANSCRIPTS  \n", transcripts)
    final_clean = []
    clean_index_lst = []
    # print(type(transcript))
    for cur_speech in transcript:
        clean_speech = []
        line_count = 0
        cur_speech["text"] = cur_speech["text"].replace('\n', ' ').replace('\r', '') # get rid of all new line characters
        non_word = extract_nonwords(cur_speech["text"])
        if non_word == "-1":
            clean_speech.append([cur_speech["text"], line_count])
            clean_index_lst.append(line_count)
        else:
            print(non_word)
        line_count += 1
    return [clean_speech, transcript], clean_index_lst


"""pull non-words like (laughing) from the given transcript"""
def extract_nonwords(string, start='(', stop=')'):
    try:
        return string[string.index(start)+1:string.index(stop)]
    except:
        return "-1"

"""list possible download streams, pull best audio file"""
def download_audio(id):
    url = pack_request(id)
    ytd = YouTube(url)
    audio = ytd.streams.filter(only_audio=True).first()
    print(audio)
    audio.download(save_path)
    return ytd.title

"""add prefix to youtube id"""
def pack_request(id):
    prefix = "https://www.youtube.com/watch?v="
    url = prefix + id
    return url

"""get video transcript from id with timestamps"""
def retrieve_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    return transcript



final = how_many_consec_in_front([4, 5, 6, 7, 8, 12, 42], 4)
print(final)
