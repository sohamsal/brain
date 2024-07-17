import requests
import os

#access_key = os.environ.get('UNSPLASH_ACCESS_KEY')
url = 'https://api.unsplash.com/search/photos'
params = {
    'query': 'writing',        
    'page': 1,                
    'per_page': 1,           
    'orientation': 'portrait' 
}

headers = {
    'Authorization': f'Client-ID {access_key}'
}

response = requests.get(url, headers=headers, params=params)
img = response.json()['results'][0]['urls']['full']

def download_image(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image from {url}")
    
download_image(img, 'downloaded_image.jpg')
print(f"Image downloaded")

