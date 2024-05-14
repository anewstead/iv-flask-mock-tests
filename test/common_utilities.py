from src.firestore_db import firestore_db
from src.products import PRODUCTS_COLLECTION_NAME
from src.shop import SHOP_COLLECTION_NAME


def delete_all_documents():
    for collection_name in [SHOP_COLLECTION_NAME, PRODUCTS_COLLECTION_NAME]:
        collection_ref = firestore_db.collection(collection_name)
        docs = collection_ref.stream()
        for doc in docs:
            doc.reference.delete()
