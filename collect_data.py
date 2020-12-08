from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
import os
import sys
import csv
import re

save_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\audio_files"
chunk_save_path =  r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\chunked_audio_files_drunk"
gradual_inebriation = ["DkhFw4B_OvQ", "aEEv5xFMdCA"]
all_inebriated = ["woDiIAQBCM4", "yJJRVleE3_Q", "FbmnrDl-dUQ", "Xn0moClwDuM"]
sober = ["Hoixgm4-P4M", "g6NsBQBjpDw"]
# sober = ["Hoixgm4-P4M"]
csvname = "AudioDataListDrunk.csv"



def main():
    video_list = all_inebriated
    all_rows = []
    fields = ['Chunk Title', 'Text', 'Start Offset', 'End Offset']
    for id in video_list:
        print('vid id \n', id)
        temp_transcript = retrieve_transcript(id)
        # print("temp_transcript \n ", temp_transcript)
        nested_transcript_dict, clean_indices = find_longest_segments(temp_transcript)
        nested_transcript_dict = nested_transcript_dict[1]
        # clean_audio_zip = concat_clean_audio(temp_transcript, clean_indices)
        clean_text_and_offsets = pull_clean_text_and_offsets(id, nested_transcript_dict, clean_indices)
        title = download_audio(id)
        rows = download_audio_chunks(clean_text_and_offsets, title)
        all_rows.extend(rows)
        print("Pulled " + str(len(nested_transcript_dict)) + " audio chunks from the video titled: " + title)

    with open(csvname, 'w') as csvfile:
        print("what's going on")
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(all_rows)

"""given indicies of 'clean' audio, get corresponding text chunks and time offsets"""
def pull_clean_text_and_offsets(id, transcipt_dict, index_list):
    nested_clean_audio_transcripts = []
    for i in index_list:
        offsets = [transcipt_dict[i]["start"], transcipt_dict[i]["start"] + transcipt_dict[i]["duration"]]
        nested_clean_audio_transcripts.append([transcipt_dict[i]["text"], offsets])
    return nested_clean_audio_transcripts

"""count consecutive integers directly in front of the given value"""
def how_many_consec_in_front(index_list, val):
    in_front = 0
    val_index = index_list.index(val)
    if val != index_list[-1]:
        for temp_num in index_list:
            if temp_num == val:
                for next in index_list[val_index+1:]:
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
    line_count = 0
    for cur_speech in transcript:
        clean_speech = []

        cur_speech["text"] = cur_speech["text"].replace('\n', ' ').replace('\r', '') # get rid of all new line characters
        non_word = extract_nonwords(cur_speech["text"])
        if non_word == "-1":
            clean_speech.append([cur_speech["text"], line_count])
            clean_index_lst.append(line_count)
        else:
            pass
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
    # print(audio.title)
    out_file = audio.download(save_path)
    title = ytd.title
    # new_name = title[:15]
    # os.rename(out_file, new_name)
    # print('title ', title)
    return title

"""Use offsets to take audio chunks from original audio file"""
def download_audio_chunks(clean_text_and_offsets, title):
    chunk_num = 0
    rows = []
    # title = title.replace('|', '').replace(',', '').replace(':', '')
    # title = re.sub(' +', ' ', title)
    # print('title ', title)
    for chunk in clean_text_and_offsets:
        temp_path = save_path
        temp_path = os.path.join(temp_path, title + ".mp4")
        # print(temp_path)
        sound = AudioSegment.from_file(temp_path, "mp4")
        start = chunk[1][0]
        # print('start \n',start)
        end = chunk[1][1]
        # print('end \n',end)
        post_fix2 = "\\" + title + " CHUNK" + str(chunk_num) + ".wav"
        temp_chunk = sound[start*1000:end * 1000]
        temp_chunk.export(chunk_save_path + post_fix2, format="wav")
        chunk_num += 1
        rows.append([title + " CHUNK" + str(chunk_num), chunk[0], start, end])
    return rows

"""add prefix to youtube id"""
def pack_request(id):
    prefix = "https://www.youtube.com/watch?v="
    url = prefix + id
    return url

"""get video transcript from id with timestamps"""
def retrieve_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    return transcript


main()
