import hashlib
import smtplib
import os


def generate_signature(params):
    hash_object = hashlib.sha256()
    for key in ['status', 'company_id', 'order_id']:
        hash_object.update(params.get(key).encode())
        print(hash_object.hexdigest(), params.get(key))
    signature = hash_object.hexdigest()
    return signature

