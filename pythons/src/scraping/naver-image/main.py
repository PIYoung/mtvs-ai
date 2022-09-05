import json
import urllib.request

client_id = "ulW9QRhGCUEPJnIyGxFc"
client_secret = "Y3GYB8CTzY"

# 검색할 단어
display = 100
encText = urllib.parse.quote("고양이")
for start in range(1, 1000, 100):
    url = f"https://openapi.naver.com/v1/search/image?query={encText}&start={start}&display={display}"  # json 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)

    res_code = response.getcode()
    if res_code == 200:
        response_body = response.read()
        response_body = json.loads(response_body)

        for item in response_body["items"]:
            # item["title"] item["link"] item["sizeheight"] item["sizewidth"] item["thumbnail"]
            link = item["link"]
            link_parser = link.split("/")
            save_name = link_parser[-1]

            try:
                urllib.request.urlretrieve(link, f"images/{save_name}")
            except Exception as e:
                print(e, save_name)
    else:
        print("Error Code:" + res_code)
