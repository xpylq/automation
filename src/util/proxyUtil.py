import urllib
import json


# 获取代理

def get_proxy():
    content = urllib.request.urlopen(
        'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=4837417faf1f475b8ae49e58aa8ee5fb&orderno=YZ2018656775FjuvA6&returnType=2&count=1').read()
    proxy_list = json.loads(content)['RESULT']
    return proxy_list[0]


# 获取手机号码
# pid:1.知乎-13899
# token:http://api.eobzz.com/httpApi.do?action=loginIn&uid=xpylq&pwd=you120147
def get_mobile():
    pid = 13899
    uid = 'xpylq'
    token = '84cd7b128d7b8b7ee07c044aab42615b'
    content = urllib.request.urlopen(
        'http://api.eobzz.com/httpApi.do?action=getMobilenum&pid=' + str(
            pid) + '&uid=' + uid + '&token=' + token + '&mobile=&size=1').read()
    mobile = str(content, encoding="utf-8").split('|').__getitem__(0)
    print("[op:get_mobile]", mobile)
    return mobile


def get_specified_mobile():
    pid = 13899
    uid = 'xpylq'
    token = '84cd7b128d7b8b7ee07c044aab42615b'
    content = urllib.request.urlopen(
        'http://api.eobzz.com/httpApi.do?action=getMobilenum&pid=' + str(
            pid) + '&uid=' + uid + '&token=' + token + '&mobile=&size=1').read()
    mobile = str(content, encoding="utf-8").split('|').__getitem__(0)
    print("[op:get_mobile]", mobile)
    return mobile


def get_code(mobile):
    uid = 'xpylq'
    token = '84cd7b128d7b8b7ee07c044aab42615b'
    content = urllib.request.urlopen(
        'http://api.eobzz.com/httpApi.do?action=getVcodeAndReleaseMobile&uid=' + uid + '&token=' + token + '&mobile=' + str(
            mobile)).read()
    print("[op:get_code]", content)
    code = str(content, encoding="utf-8")
    if code == 'not_receive':
        return code
    else:
        return code.split('|').__getitem__(1)


if __name__ == "__main__":
    mobile = get_mobile()
    get_code(mobile)
    print('17196958245')
