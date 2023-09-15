import re
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
#import docx
#from docx.shared import Inches,Cm

#doc_path = 'D:/cp_code/HKMC_ccIC24_Project_-_CLU-HUD_RS.docx'
#doc = docx.Document(doc_path)
#search_string = "GUI"

url = 'http://avncb.lge.com:8080/cb/wiki/'

# for paragraph in doc.paragraphs:
#     if not paragraph._element.xpath('.//w:tbl'):
#         if search_string in paragraph.text:
#             wikipage = str(paragraph._p.xpath(".//w:hyperlink/@w:tooltip"))
#             matches = re.search(r'\d+', wikipage)

#             if matches:
#                 number = matches.group()
#                 print(url+number)
#                 url = url+number
#             else:
#                 print("일치하는 숫자를 찾을 수 없습니다.")
#             # print(paragraph.text)

id = ''         # ID
passwd = '!'     # 패스워드
# wiki_link = 'http://avncb.lge.com:8080/cb/wiki/98802445'
wiki_link = url
base_url = 'http://avncb.lge.com:8080'

#드라이버
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(wiki_link)
driver.find_element_by_id('user').send_keys(id)
driver.find_element_by_id('password').send_keys(passwd)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/input').click()

s = requests.Session()
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
s.headers.update(headers)

for cookie in driver.get_cookies():
    c = {cookie['name'] : cookie['value']}
    s.cookies.update(c)

res = s.get(wiki_link)
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

download_link = base_url + download_link[0][9:-2]

print("타이틀:", title)
print("파일명:", filename)
print("다운로드 링크:", download_link)

file = open(filename, 'wb')
response = s.get(download_link)
if response.status_code == 200:
    file.write(response.content)
file.close()

#이미지 삽입
# doc.add_picture(filename,width=Inches(4),height=Inches(3))

# for paragraph in doc.paragraphs:
#     if search_string in paragraph.text:
#         doc.add_picture('D:/cp_code/' + filename,width=Inches(4),height=Inches(3))
#         doc.save(doc_path)
