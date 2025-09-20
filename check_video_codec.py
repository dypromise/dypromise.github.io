import cv2
import os
import subprocess
import shutil

def get_video_info(file_path):
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return None, None
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        bitrate = int(cap.get(cv2.CAP_PROP_BITRATE))
        cap.release()
        return codec, bitrate
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None

def process_videos(source_directory, dest_directory):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    h264_codecs = ['avc1', 'h264', 'x264']
    
    for filename in os.listdir(source_directory):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            source_path = os.path.join(source_directory, filename)
            dest_path = os.path.join(dest_directory, filename)
            
            codec, bitrate = get_video_info(source_path)
            
            if codec and codec.lower() not in h264_codecs:
                print(f"Converting {filename} (Codec: {codec}) to H.264...")
                bitrate_str = f"{bitrate}k" if bitrate > 0 else '2000k'
                command = [
                    'ffmpeg',
                    '-i', source_path,
                    '-c:v', 'libopenh264',
                    '-b:v', bitrate_str,
                    '-pix_fmt', 'yuv420p',
                    dest_path
                ]
                try:
                    subprocess.run(command, check=True)
                    print(f"Successfully converted {filename} and saved to {dest_directory}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {filename}: {e}")
            elif codec:
                print(f"{filename} is already H.264. Copying to {dest_directory}...")
                shutil.copy(source_path, dest_path)
                print(f"Successfully copied {filename}")
            else:
                print(f"Could not determine codec for {filename}. Skipping.")

if __name__ == "__main__":
    source_videos_directory = 'videos'
    dest_videos_directory = 'videos2'
    print(f"Processing videos from '{source_videos_directory}' to '{dest_videos_directory}'...")
    process_videos(source_videos_directory, dest_videos_directory)
    print("Video processing complete.")