import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.utils import parseaddr, formataddr

    
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = "1827108135@qq.com"
password = "sgqghfqgzsjhhgdf"
to_addr = "shilishuoya@gmail.com"
smtp_server = "smtp.qq.com"

# 邮件对象:
msg = MIMEMultipart()
#msg = MIMEText('hello, the file as follows...', 'plain', 'utf-8')
msg['From'] = _format_addr('Server <%s>' % from_addr)
msg['To'] = _format_addr('Master <%s>' % to_addr)
msg['Subject'] = Header('Some Text……', 'utf-8').encode()
msg.attach(MIMEText('hello, the file as follows...', 'plain', 'utf-8'))

#附件

#for txtFile in xx:
#	with open(txtFile, 'rb') as f:
#		pass

# 添加附件就是加上一个MIMEBase，从本地读取一个文件:
with open('李硕.txt', 'rb') as f:
    # 设置附件的MIME和文件名，这里是text类型:
    mime = MIMEBase('text', 'plain', filename='李硕.txt')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='李硕.txt')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)


server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()



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
 	
