import os
import sys
from os import environ
import requests
import json
import tarfile


class UploadResponse(object):
    def __init__(self, Key: str, uploadURL: str):
        self.Key = Key
        self.UploadURL = uploadURL


UploadsApiEndpoint = (
    "https://e1ti7jjec5.execute-api.eu-central-1.amazonaws.com/uploads?target=xray"
)

if not len(sys.argv) == 3:
    print("python3 upload-results.py test-results.xml test-results.json")
    exit()

if not os.path.exists(sys.argv[1]):
    print(sys.argv[1] + " does not exists.")
    exit()

if not sys.argv[1].endswith("xml"):
    print(sys.argv[1] + " invalid results file, please enter a xml file.")
    exit()

if not sys.argv[2].endswith("json"):
    print(sys.argv[2] + " invalid schema file, please enter a json file.")
    exit()

if not os.path.exists(sys.argv[2]):
    print(sys.argv[2] + " does not exists.")
    exit()

upload_key = None

if environ.get("UploadAPIKey") is not None:
    upload_key = os.environ["UploadAPIKey"]

if not upload_key:
    print("Please define the UploadAPIKey in env")
    exit()

print("Requesting upload to %s" % UploadsApiEndpoint)

response = requests.get(UploadsApiEndpoint, headers={"authorization": upload_key})

if response.status_code == 200:
    print("Authenticated.")
    upload_response = UploadResponse(**json.loads(response.text))

    upload_tar = "./file1.tar.gz"

    if os.path.exists(upload_tar):
        os.remove(upload_tar)

    tar = tarfile.open(upload_tar, "w:gz")
    tar.add(sys.argv[1], arcname=os.path.basename(sys.argv[1]))
    tar.add(sys.argv[2], arcname=os.path.basename(sys.argv[2]))
    tar.close()

    upload_data = open(upload_tar, "rb").read()

    print("Uploading %s ..." % upload_tar)
    response = requests.put(
        upload_response.UploadURL,
        data=upload_data,
        headers={"Content-Type": "application/binary"},
    )
    print(
        "Upload was: %s with Http status: %s" % (response.reason, response.status_code)
    )

else:
    print("Requesting upload failed. Http Status:%s" % response.status_code)
    exit()
