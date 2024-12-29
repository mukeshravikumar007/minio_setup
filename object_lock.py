from minio import Minio
from minio.error import S3Error
from minio.commonconfig import GOVERNANCE
from minio.retention import Retention
from datetime import datetime, timedelta

client = Minio(
    "10.10.192.9:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

source_file = "/home/nitish/Documents/lion.jpg"
bucket_name = "python-test-bucket"
destination_file = "test_lion.jpg"

try:
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name, object_lock=True)
        print(f"Created bucket :'{bucket_name}'")
    else:
        print(f"Bucket '{bucket_name}' already have.")
    client.fput_object(bucket_name, destination_file, source_file)
    print(
        f"File '{source_file}' uploaded as object "
        f"'{destination_file}' to bucket '{bucket_name}'."
    )
    retention_period = timedelta(days=30)
    client.set_object_retention(
        bucket_name,
        destination_file,
        Retention(GOVERNANCE, datetime.utcnow() + retention_period),
    )
    print(f"Retention applied for {retention_period.days} days.")
except S3Error as exc:
    print("S3 error occurred:", exc)
except Exception as exc:
    print("An unexpected error occurred:", exc)
