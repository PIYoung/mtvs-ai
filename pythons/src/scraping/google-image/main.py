# !pip install git+https://github.com/Joeclinton1/google-images-download.git
from google_images_download import google_images_download


def google_image_crawling(keyword, limit):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": keyword,
        "limit": limit,
        "print_urls": True,
        "format": "jpg",
    }
    paths = response.download(arguments)
    print(paths)

    return paths


google_image_crawling("cat,dog", 10)
