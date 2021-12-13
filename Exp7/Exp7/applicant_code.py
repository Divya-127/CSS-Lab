import qrcode as qr
import rsa
from cryptography.fernet import Fernet

def file_open(file_name):
    file = open(file_name, 'rb')
    file_data = file.read()
    file.close()
    return file_data

resume_text = file_open("resume.txt").decode("UTF-8")

qr_object = qr.QRCode(None, error_correction=qr.constants.ERROR_CORRECT_L,
box_size=3, border=4)
qr_object.add_data(resume_text)
qr_object.make(fit=True)
qrcode = qr_object.make_image()
qrcode.save('qr_cv.png')

privkey_applicant = rsa.PrivateKey.load_pkcs1(file_open('my_priv_key.pem'))
pubkey_company = rsa.PublicKey.load_pkcs1(file_open('company_public_key.pem'))
symkey = file_open('symmetric_key.pem')
qrcode_png = file_open("qr_cv.png")

signature = rsa.sign(qrcode_png, privkey_applicant, 'SHA-512')
s = open('signature_file.bin', 'wb')
s.write(signature)
cipher = Fernet(symkey)
qrcode_encrypted = cipher.encrypt(qrcode_png)
e = open('encrypted_qrcode.bin', 'wb')
e.write(qrcode_encrypted)
symkey_encrypted = rsa.encrypt(symkey, pubkey_company)
e = open('encrypted_symmetric_key.bin', 'wb')
e.write(symkey_encrypted)