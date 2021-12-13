import qrcode as qr
import rsa
from cryptography.fernet import Fernet

def file_open(file_name):
    file = open(file_name, 'rb')
    file_data = file.read()
    file.close()
    return file_data

encrypted_qrcode = file_open('encrypted_qrcode.bin')

encrypted_symmetric_key = file_open('encrypted_symmetric_key.bin')
signature = file_open('signature_file.bin')

privkey_company = rsa.PrivateKey.load_pkcs1(file_open('company_private_key.pem'))
pubkey_applicant = rsa.PublicKey.load_pkcs1(file_open('my_public_key.pem'))
symkey = rsa.decrypt(encrypted_symmetric_key, privkey_company)

cipher = Fernet(symkey)
qrcode_png = cipher.decrypt(encrypted_qrcode)

try:
    rsa.verify(qrcode_png, signature, pubkey_applicant)
    print("Signature has been verified.")
    q = open("decrypted_qrcode.png", "wb")
    q.write(qrcode_png)
except:
    print("Signature could not be verified!!!")
