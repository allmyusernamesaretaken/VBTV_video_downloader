# VBTV video downloader

## Description

In a recent update vb.tv changed their web player. The new one doesn't allow for any keyboard controls like pause, skip, rewind, etc. To combat this issue, I wrote this script to download a replay, so you can watch it in your favorite video player.


## Requirements

To get started with this project, you'll need to ensure you have the following:

- tested with Python 3.9
- urllib.parse
- requests
- m3u8_To_MP4
- ffmpeg (for `m3u8_To_MP4` functionality)


### Important Note for `m3u8_To_MP4`
I had an error where a file couldn't be found. like stated in this issue (https://github.com/h2soong/m3u8_To_MP4/issues/22) you can tackle this by changing a method in the "v2_abstract_crawler_processor.py" file to the following.
   
```python
       def _construct_segment_path_recipe(self, key_segment_pairs):
        with open(self.segment_path_recipe, 'w', encoding='utf8') as fw:
            for _, segment in key_segment_pairs:
                file_name = path_helper.resolve_file_name_by_uri(segment)
                fw.write("file '{}'\n".format(file_name))
```    

## Installation

1. install ffmpeg by following the instructions on their website (https://ffmpeg.org/download.html)
2. install the other requirements
3. maybe change the function in the `m3u8_To_MP4` package as described above
4. run the script with `python main.py -url <url> -path <output_path>`
