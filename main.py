import urllib.parse
import argparse
from pym3u8downloader import M3U8Downloader
import m3u8_To_MP4
import requests
import subprocess
import os

def split_url(full_url, split_marker="https://tv.volleyballworld.com/player?self-link="):
    """
    Splits a URL at a specified marker and returns the part after the marker.

    Parameters:
    full_url (str): The full URL to be split.
    split_marker (str): The marker at which to split the URL. Defaults to "https://tv.volleyballworld.com/player?self-link=".

    Returns:
    split url (str): The portion of the URL after the specified marker.

    Exits:
    If the marker is not found in the full_url, the function exits with the message "Invalid URL".
    """
    if split_marker in full_url:
        split_url = full_url.split(split_marker, 1)[1]
        return split_url
    else:
        exit("Invalid URL")


def decode_url(encoded_url):
    """
        Decodes a percent-encoded URL into its original, human-readable format.

        Parameters:
        encoded_url (str): The percent-encoded URL to decode.

        Returns:
        decoded url (str): The decoded URL, where percent-encoded characters have been converted back to their original form.
        """
    return urllib.parse.unquote(encoded_url)


def fetch_json(url):
    """
    Fetches JSON data from a URL

    Parameters:
    url (str): The url of the media content to fetch.

    Returns:
    json data (dict) The parsed JSON data as a dictionary, or exits if an error occurred.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()  # Parse JSON response
        return json_data

    except requests.exceptions.RequestException as e:
        exit(f"Error fetching data: {e}")
    except ValueError as e:
        exit(f"Error parsing JSON: {e}")


def extract_video_url(json_data):
    """
    Extracts the video URL (*.m3u8) from the JSON data, which vbtv links to.

    Parameters:
    json_data (dict): The JSON data containing video information.

    Returns:
    video URL (str), or exits the script if an error occurs.
    """
    try:
        entry = json_data.get("entry", [])
        if entry:
            content = entry[0].get("content", {})
            video_url = content.get("src", "")
            return video_url
        else:
            exit("No entry found in JSON data")

    except (IndexError, KeyError, TypeError) as e:
        exit(f"Error extracting video URL: {e}")


def parse_arguments():
    """
    Parses command-line arguments for the script.

    This function sets up an argument parser using the argparse module to handle command-line arguments.
    It defines a single argument, '-url', which is a string representing the URL to download. The function
    returns the parsed arguments.


    Returns:
    argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='download a vbtv replay')
    parser.add_argument('-url', type=str, help='url to download')
    return parser.parse_args()


def fetch_m3u8_playlist(m3u8_url):
    """
    Fetches and parses an M3U8 playlist from the given URL.

    Parameters:
    m3u8_url (str): The URL of the M3U8 playlist.

    Returns:
    list or None: A list of tuples (resolution, url) extracted from the M3U8 playlist, or None if an error occurred.
    """
    try:
        response = requests.get(m3u8_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        lines = response.text.splitlines()
        playlist = []

        # Parse the playlist and extract resolutions and URLs
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('#EXT-X-STREAM-INF:'):
                attributes = line.split(',')
                for attr in attributes:
                    if attr.startswith('RESOLUTION='):
                        resolution = attr.split('=')[1]
                i += 1
                if i < len(lines):
                    url = lines[i].strip()
                    playlist.append((resolution, url))
            i += 1

        return playlist

    except requests.exceptions.RequestException as e:
        print(f"Error fetching M3U8 playlist: {e}")
        return None




def main():
    args = parse_arguments()
    print(args.url)
    json_url_encoded = split_url(args.url)
    print(json_url_encoded)
    jason_url_decoded = decode_url(json_url_encoded)
    print(jason_url_decoded)
    json_data = fetch_json(jason_url_decoded)
    print(json_data)
    video_url = extract_video_url(json_data)
    print(video_url)
    playlist = fetch_m3u8_playlist(video_url)
    print("playlist::" , playlist)
    print(playlist[1][1])
    url_m3u8 = playlist[1][1]
    ts_list = requests.get(url_m3u8)
    print("Downloading video...")
    print(ts_list.content)
    downloader = M3U8Downloader(
        input_file_path=video_url,
        output_file_path="output_video"
    )

    print("---------", downloader.input_file_path)
    downloader.download_playlist()

    #m3u8_To_MP4.multithread_download(video_url, mp4_file_dir="./", mp4_file_name="video.mp4", tmpdir="./tmp")
    # m3u8_To_MP4.async_download(video_url, mp4_file_dir="", mp4_file_name="video1.mp4", tmpdir="./tmp")
    print("Download complete")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
