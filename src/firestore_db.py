from google.cloud import firestore
import os

# TODO: Set vie env variables
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8082"
os.environ["GCLOUD_PROJECT"] = "test-project"


firestore_db = firestore.Client()
