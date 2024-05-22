"""Module to access EXP and UCM certs and get validity"""
import json
import base64
import ssl
import datetime
import requests
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def encode_to_base64(login_cred):
    """Function to decode ASCII to base64"""
    encode_to_ascii = login_cred.encode("ascii")
    base64_bytes = base64.b64encode(encode_to_ascii)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def certificate_decode(api_path):
    """Function to decode certificate and get its validity"""

    if "platformcom" in api_path:
        #username = input("enter username:")
        #password = input("enter password:")
        login_cred = 'user:password'
        headers = {
        'Authorization': f'Basic {encode_to_base64(login_cred)}'
        }

        response = requests.request(
            "GET",
            api_path,
            headers=headers,
            verify=False,
            timeout=30
        )
        jsonoutput = json.loads(response.text)
        cert = jsonoutput.get("certificate")
        cert_decoded = x509.load_pem_x509_certificate(
            str.encode(cert), default_backend())
        return cert_decoded.not_valid_after
    port = 443
    cert = ssl.get_server_certificate((api_path, port))
    cert_decoded = x509.load_pem_x509_certificate(str.encode(cert),
                                                default_backend())
    #print(type(cert_decoded.not_valid_after))
    return cert_decoded.not_valid_after.date()
