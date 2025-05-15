import requests

API_URL = 'https://drowsiness-detection-3-4yld.onrender.com'

def analyze_frame_bytes(img_bytes: bytes) -> str:
    files = {'frame': ('frame.jpg', img_bytes, 'image/jpeg')}
    r = requests.post(API_URL, files=files)
    return r.json().get('status', 'unknown')
