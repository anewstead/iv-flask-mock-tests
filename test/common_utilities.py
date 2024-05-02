from src.firestore_db import firestore_db


def delete_all_documents(collection_name):
    collection_ref = firestore_db.collection(collection_name)
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()
