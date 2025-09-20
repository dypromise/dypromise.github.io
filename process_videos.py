import os
import cv2
from bs4 import BeautifulSoup

def get_video_dimensions(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return None, None
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return width, height
    except Exception as e:
        print(f"Error getting dimensions for {video_path}: {e}")
        return None, None

def update_html_with_video_classes(html_path, base_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    video_tags = soup.find_all('video')
    for video_tag in video_tags:
        src = video_tag.get('src')
        if src:
            video_path = os.path.join(base_path, src)
            
            width, height = get_video_dimensions(video_path)
            
            result_card = video_tag.find_parent(class_='result-card')
            if result_card:
                # remove old classes
                new_classes = [c for c in result_card.get('class', []) if c not in ['widescreen', 'portrait']]
                result_card['class'] = new_classes

                if width and height:
                    if width > height:
                        result_card['class'].append('widescreen')
                    else:
                        result_card['class'].append('portrait')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

if __name__ == '__main__':
    workspace_root = '/Users/bytedance/Downloads/git主页'
    html_file = os.path.join(workspace_root, 'index.html')
    update_html_with_video_classes(html_file, workspace_root)
    print("Finished updating index.html with video classes.")