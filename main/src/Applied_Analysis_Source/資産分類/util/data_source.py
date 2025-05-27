from typing import Dict, Any
import pymongo
import psycopg2
from azure.storage.blob import BlobServiceClient
import boto3
from google.cloud import storage

class DataSourceManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_connections = {}
        self.cloud_clients = {}
        self._init_connections()

    def _init_connections(self):
        # PostgreSQL接続
        if 'asset_db' in self.config:
            self.db_connections['postgres'] = psycopg2.connect(**self.config['asset_db'])

        # MongoDB接続
        if 'pattern_db' in self.config:
            self.db_connections['mongo'] = pymongo.MongoClient(**self.config['pattern_db'])

        # クラウドストレージ接続
        if 'azure' in self.config:
            self.cloud_clients['azure'] = BlobServiceClient.from_connection_string(
                self.config['azure']['connection_string']
            )
        
        if 'aws' in self.config:
            self.cloud_clients['s3'] = boto3.client('s3')
        
        if 'gcp' in self.config:
            self.cloud_clients['gcs'] = storage.Client()

    def save_result(self, result: Dict[str, Any]):
        # 結果をデータベースに保存
        with self.db_connections['postgres'].cursor() as cur:
            cur.execute("""
                INSERT INTO asset_results 
                (file_name, language, confidence, metadata)
                VALUES (%s, %s, %s, %s)
            """, (
                result['file_name'],
                result['language'],
                result['confidence'],
                result
            ))
        self.db_connections['postgres'].commit()

        # MongoDB（pattern_db）への保存
        if 'mongo' in self.db_connections:
            db = self.db_connections['mongo'].get_database()
            collection = db['your_collection_name']  # ここは実際のコレクション名に置き換えてください
            collection.insert_one(result)

    def upload_to_cloud(self, file_path: str, destination: str):
        # クラウドストレージにアップロード
        if 'azure' in self.cloud_clients:
            blob_client = self.cloud_clients['azure'].get_blob_client(
                container=self.config['azure']['container'],
                blob=destination
            )
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
