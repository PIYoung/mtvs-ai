from bing_image_downloader import downloader

query_string = "우영우"
downloader.download(
    query_string,
    limit=10,
    output_dir="images",
    adult_filter_off=True,
    force_replace=False,
    timeout=60,
)
