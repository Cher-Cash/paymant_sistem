import hashlib
import smtplib
import os


def generate_signature(params):
    order_id = params.get('order_id')
    company_id = params.get('company_id')
    secret_key = params.get('secret_key')
    sigma = f"{order_id}{company_id}{secret_key}"
    hash_object = hashlib.sha256(sigma.encode())
    signature = hash_object.hexdigest()
    return signature
