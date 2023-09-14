import re
import requests

########## CodeBeamer 관련 클래스
class ProjectMixin:    
    def getProjects(self):
        return self.get('/projects')
        
    def getProject(**kwargs):
        if not len(kwargs) == 1: 
            raise Exception('getProject method takes one argument in : name, id')
        elif kwargs.get('name', None):
            return self.get(f"/project/{kwargs['name']}")
        elif kwargs.get('id', None):
            return self.get(f"/project/{kwargs['id']}")
        else:
            raise Exception('getProject method takes one argument in : name, id')

class Codebeamer(ProjectMixin):
    def __init__(self, url, login, password):
        self.base_url = url
        self.auth = (login, password)

    def get(self, uri):
        url = self.base_url + uri
        res = requests.get(url, auth=self.auth, verify=True)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            print(f"Warning : GET error ({url})")
            return json.loads(res.content)

    def put(self, uri, data):
        url = self.base_url + uri
        res = requests.put(url, json=data, auth=self.auth, verify=True)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            print(f"Warning : PUT error ({url})")
            return json.loads(res.content)

    def post(self, uri, data):
        url = self.base_url + uri
        res = requests.post(url, json=data, auth=self.auth, verify=True)
        if res.status_code == 201:
            return json.loads(res.content)
        else:
            print(f"Warning : POST error ({url})")
            return json.loads(res.content)


id = ''         # ID
passwd = ''     # 패스워드
wiki_link = 'http://avncb.lge.com:8080/cb/wiki/98802445'

cb = Codebeamer(url='http://avncb.lge.com:8080', login=id, password=passwd)
res = requests.get(url=wiki_link, auth=cb.auth, verify=True)
content = str(res.content)

pattern = "<title>.*<\/title>"
title = re.findall(pattern, content)[0][7:-8]

pattern = "![0-9]*\.png!"
filename = re.findall(pattern, content)[0][1:-1]

# 다운로드 링크를 찾아냄
download_link = ""
index = 0
str_to_find = filename
while index < len(content):
    index = content.find(str_to_find, index)
    if index == -1:
        break
    pattern = "img src=\".*(?:%s).*\"\s" % (filename)
    download_link = re.findall(pattern, content[index-100:index+100])
    if download_link != "":
        break
    index += 3

download_link = cb.base_url + download_link[0][9:-2]

print("타이틀:", title)
print("파일명:", filename)
print("다운로드 링크:", download_link)

with open(filename, 'wb') as handle:
    response = requests.get(download_link, stream=True)

    if not response.ok:
        print(response)
    
    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)

# 다운로드 방법 1
# file = open(filename, 'wb')
# response = requests.get(download_link, stream=True)
# if response.status_code == 200:
#     for block in response.iter_content(1024):
#         if not block:
#             break
#         file.write(block)
# file.close()

# 다운로드 방법 2
#urllib.request.urlretrieve(download_link, filename)
