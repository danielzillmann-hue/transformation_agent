from google.cloud import storage
import logging

logger = logging.getLogger(__name__)

class IngestionEngine:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def list_files(self):
        """Lists all files in the bucket."""
        try:
            blobs = list(self.client.list_blobs(self.bucket_name))
            logger.info(f"Listed {len(blobs)} blobs from {self.bucket_name}")
            return blobs
        except Exception as e:
            logger.error(f"Error accessing bucket {self.bucket_name}: {e}")
            return []

    def read_file(self, blob_name):
        """Reads content of a blob."""
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()
