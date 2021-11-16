import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
import logging
import tarfile

s3_client = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_results_bucket(test_result_file, download_path):
    """uploads the test results into the results bucket for keeping journal report"""
    ResultsBucket = os.environ["ResultsBucket"]

    for file in test_result_file:
        test_result_file = "{}/{}".format(download_path, file.name)
        upload_path = "{}-{}".format(download_path.replace("/tmp/", ""), file.name)
        s3_client.upload_file(test_result_file, ResultsBucket, upload_path)
        logger.info("uploaded to %s ...", ResultsBucket)


def publish_test_results(test_result_file, download_path):
    """Process the test results and upload them to the configured endpoint"""
    # Place your data processing here
    #
    #

    upload_results_bucket(test_result_file, download_path)


def unpack_test_results(test_result_file, download_path):
    """unpacks the tar gz test results package"""
    # Validates the packaged file type: tar.gz allowed
    if test_result_file.endswith("tar.gz"):
        members = []
        try:
            tar = tarfile.open("{}-{}".format(download_path, test_result_file), "r:gz")
            members = tar.getmembers()

            if len(members) == 0:
                logger.info("Invalid test results file. Tar file is empty.")
                return

            tar.extractall(path=download_path)
            tar.close()
            logger.info("Unpacked %s.", test_result_file)
        except:
            logger.info("unpacking %s failed. %s", test_result_file, sys.exc_info()[0])
            return

        publish_test_results(members, download_path)


def s3_publish_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        logger.info("%s received from %s ...", key, bucket)
        download_path = "/tmp/{}".format(uuid.uuid4())
        test_results_file = "{}-{}".format(download_path, key)
        s3_client.download_file(bucket, key, test_results_file)
        unpack_test_results(key, download_path)
