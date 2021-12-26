#!/usr/bin/env python3

from pytube import YouTube
from pytube.cli import on_progress
import argparse
import sys
from tqdm import tqdm

def ddl_video(address, path_out):
    tqdm.write(f" ---> Downloading video at {address}")

    try: 
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(address, on_progress_callback=on_progress)
    except Exception as e: 
        print("Connection Error") #to handle exception 
        print(e)
        return 
    tqdm.write(f"Connected to {address}")

    # filter and get streams
    filtered_streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
    # tqdm.write(filtered_streams)

    video = filtered_streams.first()
    tqdm.write(f" > Downloading {video.title}")

    # downloading the video 
    try: 
        video.download(path_out)
    except Exception as e: 
        print("Download error")
        print(e) 
        return

    tqdm.write(' < Done') 


def parse_args(sys_args):

    parser = argparse.ArgumentParser(description='Download video from specified list in file')


    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", type=str, help="input file")
    group.add_argument("--address", "-a", type=str, help="input address")

    parser.add_argument("--output", "-o", type=str, help="output folder")

    args = parser.parse_args(sys_args)

    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    links = []

    path_out="."
    if args.output:
        path_out = args.output

    if args.file:
        print(f"Downloading from {args.file}")
        links = links + list(open(args.file,'r')) 

        # Remove \n        
        for i in range(len(links)):
            if links[i][-1] == "\n":
                links[i] = links[i][:-1]

    if args.address:
        links = links + [args.address] 

    for i in tqdm(range(len(links))): 
        ddl_video(links[i], path_out)
