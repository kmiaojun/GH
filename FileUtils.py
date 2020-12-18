import json
import os
import traceback
from tkinter import messagebox
import subprocess
import time
import requests
import sys


def chk_file(file: str):
    if not os.path.exists(file):
        messagebox.showwarning('警告: 必要文件不存在', file)
        return False
    return True


def remove_file(file: str):
    try:
        os.remove(file)
        return 'remove file [%s]' % file
    except Exception as e:
        return str('remove file ex[%s]' % str(traceback.format_exc()))


def ensure_file(file: str):
    if '/' in file:
        last_index = file.rindex('/')
        last_index = last_index + 1
        file_dir = file[:last_index]
        file_name = file[last_index:]
        ensure_dir(file_dir)
    f = open(file, 'a', encoding='utf-8')
    f.write('')
    f.close()


def ensure_dir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


def iterator_dir(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def read_file(file: str):
    file = open(file, 'r', encoding='utf-8')
    content = file.read()
    file.close()
    return content


def load_file_with_json(file: str):
    content = read_file(file)
    try:
        return json.loads(content, encoding='utf-8')
    except Exception as ex:
        # print('json解析错误')
        return {}


def file_append(file: str, content: str):
    try:
        f = open(file, 'a', encoding='utf-8')
        f.write(content)
        f.close()
    except FileNotFoundError:
        print('file not found')


def file_override(file: str, content: str):
    f = open(file, 'w', encoding='utf-8')
    f.write(content)
    f.close()

def enable_host_resolver(host_file:str,host:str, ip: str):
    file_override(host_file, "%s %s" % (ip, host))
    for i in range(0,5):
        subprocess.run('ipconfig /displaydns && ipconfig /flushdns', shell=True)
        time.sleep(2)
    pass

def disable_host_resolver(host_file:str, host: str, ip: str):
    file_override(host_file, "")
    subprocess.run('ipconfig /displaydns && ipconfig /flushdns', shell=True)
    pass

def dwn_img(url:str, name:str):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open('dwn\\%s.png' % name, 'wb').write(r.content)
        # 将内容写入图片
        print("done")
    else:
        print("failed")
    pass
    del r

def nginx_proxy(enable_freeze:bool):
    nginx_home = os.path.realpath(sys.argv[0]).replace(os.path.realpath(sys.argv[0]).split('\\')[-1], 'nginx-1.15.8\\')
    # nginx_home = "C:\\Users\drx\\Desktop\\GH\\GH\\nginx-1.15.8\\"
    nginx_proxy_conf = nginx_home + "conf/proxy_cpquery.conf"
    if enable_freeze:
        file_override(nginx_proxy_conf, 'server {\n\
            		listen 80;\n\
            		server_name cpquery.cnipa.gov.cn;\n\
            		location /{\n\
                        proxy_redirect off;\n\
                        proxy_set_header Host $host;\n\
                        proxy_set_header X-Real-IP $remote_addr;\n\
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
            	   		proxy_pass http://219.143.201.68:80;\n\
            		}\n\
            	}')
        subprocess.run('%s: && cd %s && nginx.exe -s reload' % (nginx_home.split(":")[0], nginx_home), shell=True)
        print("enable, nginx -s reload")
    else:
        file_override(nginx_proxy_conf, 'server {\n\
                                		listen 80;\n\
                                		server_name cpquery.cnipa.gov.cn;\n\
                                		location /{\n\
                                            proxy_redirect off;\n\
                                            proxy_set_header Host $host;\n\
                                            proxy_set_header X-Real-IP $remote_addr;\n\
                                            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
                                	   		proxy_pass http://219.143.201.68:80;\n\
                                		}\n\
                                		location /freeze.main{\n\
                                			proxy_pass http://localhost;\n\
                                		}\n\
                                	}')
        subprocess.run('%s: && cd %s && nginx.exe -s reload' % (nginx_home.split(":")[0], nginx_home),
                       shell=True)
        print("disable, nginx -s reload")



pass


if __name__ == "__main__":
    # host_home = "C:\\Windows\\System32\\drivers\\etc\\hosts"
    # disable_host_resolver(host_home, "cpquery.cnipa.gov.cn", "127.0.0.1")
    # enable_host_resolver(host_home, "cpquery.cnipa.gov.cn", "127.0.0.1")
    dwn_img('http://cpquery.cnipa.gov.cn/freeze.main?txn-code=txnImgToken&token=EF4B88ECA228B923BAB554209F3987A0&imgToken=B3EEE92D4B0B4F76A1CFB9614B94BDA1','test')
    pass