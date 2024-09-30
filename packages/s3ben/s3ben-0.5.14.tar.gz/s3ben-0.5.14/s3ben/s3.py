import datetime
import itertools
import multiprocessing
import os
import shutil
import sys
from logging import getLogger
from typing import Union

import boto3
import botocore
import botocore.errorfactory
import rgwadmin
from rgwadmin import RGWAdmin

from s3ben.constants import AMQP_HOST, NOTIFICATION_EVENTS, TOPIC_ARN

_logger = getLogger(__name__)


class S3Events:
    """
    Class for configuring or showing config of the bucket
    :param str secret_key: Secret key fro s3
    :param str access_key: Access key for s3
    :param str endpoint: S3 endpoint uri
    """

    def __init__(
        self,
        secret_key: str,
        access_key: str,
        hostname: str,
        secure: bool,
        backup_root: str = None,
    ) -> None:
        self._download = os.path.join(backup_root, "active") if backup_root else None
        self._remove = os.path.join(backup_root, "deleted") if backup_root else None
        protocol = "https" if secure else "http"
        endpoint = f"{protocol}://{hostname}"
        self.client_s3 = boto3.client(
            service_name="s3",
            region_name="default",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.client_sns = boto3.client(
            service_name="sns",
            region_name="default",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=botocore.client.Config(signature_version="s3"),
        )
        self.client_admin = RGWAdmin(
            access_key=access_key, secret_key=secret_key, server=hostname, secure=secure
        )
        self.session = boto3.Session(
            region_name="default",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.resouce = self.session.resource(service_name="s3", endpoint_url=endpoint)

    def get_config(self, bucket: str):
        return self.client_s3.get_bucket_notification_configuration(Bucket=bucket)

    def create_bucket(self, bucket: str) -> None:
        """
        Create empty bucket with no configuration
        :param str bucket: Bucket name to create
        :return: None
        """
        self.client_s3.create_bucket(Bucket=bucket)

    def create_topic(
        self,
        mq_host: str,
        mq_user: str,
        mq_password: str,
        exchange: str,
        mq_port: int,
        mq_virtualhost: str,
    ) -> None:
        """
        Create bucket event notification config
        :param str bucket: Bucket name for config update
        :param str amqp: rabbitmq address
        """
        amqp = AMQP_HOST.format(
            user=mq_user,
            password=mq_password,
            host=mq_host,
            port=mq_port,
            virtualhost=mq_virtualhost,
        )
        attributes = {
            "push-endpoint": amqp,
            "amqp-exchange": exchange,
            "amqp-ack-level": "broker",
            "persistent": "true",
        }
        self.client_sns.create_topic(Name=exchange, Attributes=attributes)

    def create_notification(self, bucket: str, exchange: str) -> None:
        """
        Create buclet notification config
        :param str bucket: Bucket name
        :param str exchange: Exchange name were to send notification
        """
        notification_config = {
            "TopicConfigurations": [
                {
                    "Id": f"s3ben-{exchange}",
                    "TopicArn": TOPIC_ARN.format(exchange),
                    "Events": NOTIFICATION_EVENTS,
                }
            ]
        }
        self.client_s3.put_bucket_notification_configuration(
            Bucket=bucket, NotificationConfiguration=notification_config
        )

    def get_admin_buckets(self) -> list:
        """
        Admin api get buckets
        :return: list
        """
        return self.client_admin.get_buckets()

    def get_bucket(self, bucket: str) -> dict:
        """
        Get bucket info via admin api
        :param str bucket: Bucket name to fetch info
        :return: dictionary with bucket info
        """
        try:
            return self.client_admin.get_bucket(bucket=bucket)
        except rgwadmin.exceptions.NoSuchBucket:
            _logger.warning(f"Bucket {bucket} not found")
            sys.exit()

    def __decuple_download(self, input: tuple) -> None:
        bucket, path = input
        self.download_object(bucket, path)

    def download_object(self, bucket: str, path: Union[str, dict]):
        """
        Get an object from a bucket

        :param str bucket: Bucket name from which to get object
        :param str path: object path
        """

        s3_obj = path
        if isinstance(path, dict):
            dst = next(iter(path.values()))
            s3_obj = "/" + next(iter(path.keys()))
            destination = os.path.join(self._download, bucket, dst)
        else:
            destination = os.path.join(self._download, bucket, path)
        dst_dir = os.path.dirname(destination)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        try:
            self.client_s3.head_object(Bucket=bucket, Key=s3_obj)
        except botocore.exceptions.ClientError as err:
            if err.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                _logger.warning("%s not found in bucket: %s", path, bucket)
        _logger.info("Downloading: %s:%s to %s", bucket, s3_obj, destination)
        self.client_s3.download_file(Bucket=bucket, Key=s3_obj, Filename=destination)

    def remove_object(self, bucket: str, path: str) -> None:
        """
        Move object to deleted items
        :param str bucket: Bucket eame
        :param str path: object path which should be moved
        :return: None
        """
        _logger.info(f"Moving {path} to deleted items for bucket: {bucket}")
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        dest = os.path.dirname(os.path.join(self._remove, current_date, bucket, path))
        src = os.path.join(self._download, bucket, path)
        file_name = os.path.basename(path)
        d_file = os.path.join(dest, file_name)
        if not os.path.exists(src):
            _logger.warning(f"{src} doesn't exist")
            return
        if not os.path.exists(dest):
            os.makedirs(dest)
        if os.path.isfile(d_file):
            _logger.warning(
                f"Removing {d_file} as another with same name must be moved to deleted items"
            )
            os.remove(d_file)
        shutil.move(src, dest)

    def download_all_objects(self, bucket_name: str, obj_keys: list) -> None:
        """
        Method for getting all objects from one bucket
        :param str bucket_name: Name of the bucket
        :param str dest: Directory root to append
        :param int threads: Number of threads to start
        :return: None
        """
        threads = 2
        with multiprocessing.pool.ThreadPool(threads) as threads:
            iterate = zip(itertools.repeat(bucket_name), obj_keys)
            threads.map(self.__decuple_download, iterate)

    def _get_all_objects(self, bucket_name) -> list:
        """
        Method to get all objects from the bucket
        :param str bucket_name: Name of the bucket
        :return: List all objects in the bucket
        """
        objects = self.resouce.Bucket(bucket_name).objects.all()
        return [o.key for o in objects]

    # def download_all_objects_v2(
    #     self, baucket_name: str, step: int, page_queue: multiprocessing.Queue
    # ) -> None:
    #     """
    #     Download objects from page object iterating every n'th page
    #     :param str bucket_name: Name of the bucket
    #     :param page: bot paginator
    #     :param int step: For loop step for multiprocess support
    #     :param multiprocessing.Queue queu: Multiprocess queu for exchanging information
    #     """
    #     import time
    #
    #     while True:
    #         data = page_queue.get(block=True, timeout=10)
    #         print(len(data[0]["Contents"]))
    #         if page_queue.empty():
    #             print("breaking")
    #             break
    #         time.sleep(0.5)

    def _check_if_object_exists(self, path):
        pass
