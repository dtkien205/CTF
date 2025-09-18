import requests

url = "http://verbal-sleep.picoctf.net:50765/impossibleLogin.php"

pdf1_url = "https://shattered.io/static/shattered-1.pdf"
pdf2_url = "https://shattered.io/static/shattered-2.pdf"

# Tải nội dung của hai file PDF về dưới dạng bytes
pdf1_content = requests.get(pdf1_url).content
pdf2_content = requests.get(pdf2_url).content

data = {
    "username": pdf1_content,
    "pwd": pdf2_content
}

response = requests.post(url, data=data)

print(response.text)
