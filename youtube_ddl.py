#!/usr/bin/env python3

from pytube import YouTube
from pytube.cli import on_progress
import argparse
import sys
from tqdm import tqdm

def ddl_video(address : str, path_out : str = "."):
    """Download a youtube video

    Args:
        address (str): http adress of the video
        path_out (str, optional): folder where video is saved. Defaults to ".".
    """

    tqdm.write(f" ---> Downloading video at {address}")

    # Stream object creation
    try: 
        # yt = YouTube(address, on_progress_callback=on_progress)
        yt = YouTube(address)
    except Exception as e: 
        print("Connection Error") #to handle exception 
        print(e)
        return 
    tqdm.write(f"Connected to {address}")

    # filter and get streams
    filtered_streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
    # tqdm.write(filtered_streams)
    video = filtered_streams.first()

    # downloading the video 
    tqdm.write(f" > Downloading {video.title}")
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

    return parser.parse_args(sys_args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    # default
    links = []
    path_out="."

    # output
    if args.output:
        path_out = args.output

    # file
    if args.file:
        print(f"Downloading from {args.file}")
        links = links + list(open(args.file,'r')) 

        # Remove \n        
        for i in range(len(links)):
            if links[i][-1] == "\n":
                links[i] = links[i][:-1]

    # address
    if args.address:
        links = links + [args.address] 

    # process
    for i in tqdm(range(len(links))): 
        ddl_video(links[i], path_out)
