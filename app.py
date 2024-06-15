import requests
import os
import hashlib


def get_sha1_hash(file_path):
    with open(file_path, "rb") as file:
        file_hash = hashlib.sha1()
        while chunk := file.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()


URLS = [
    (
        "aurora-logo.png",
        "https://jamesg.blog/assets/aurora-logo.png",
        "e104d2d326ec0033f8cf537f64dd3fc1fffacc46",
    )
]

for file_name, url, hash in URLS:
    file_exists = os.path.exists(file_name)
    if file_exists and get_sha1_hash(file_name) == url[1]:
        print("File already exists.")
        continue
    elif file_exists:
        print("File exists but is outdated or corrupt. Redownloading...")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
        continue
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        continue

    # check hash of file
    file_hash = hashlib.sha1(response.content).hexdigest()

    if file_hash != hash:
        print("Hash mismatch, file will not be saved.")
        continue

    with open("aurora-logo.png", "wb") as file:
        file.write(response.content)
