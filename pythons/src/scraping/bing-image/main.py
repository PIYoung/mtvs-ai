from bing_image_downloader import downloader

EMOTIONS_LIST = ["Angry Face", "Disgust Face", "Fear Face", "Neutral Face", "Sad Face", "Surprise Face"]

for emotion in EMOTIONS_LIST:
    query_string = emotion
    downloader.download(
        query_string,
        limit=100,
        output_dir="images",
        adult_filter_off=True,
        force_replace=False,
        timeout=60,
    )
