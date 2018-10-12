import json
import os
import time
import urllib.request
import win32api
import win32con
import win32gui
import sys

from urllib import request

# Windows下实时动态更新地球壁纸！
# 地球照片抓自日本himawari-8气象卫星官网
# 当天视频
# http://himawari8-dl.nict.go.jp/himawari8/movie/720/20180619_pifd.mp4

# 卫星照片10分钟更新一次 本地可计算时间规律
# 2018-06-20 01:10:00

base_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/"  # 官网图片地址前半部分

cwd = os.getcwd()  # 当前目录
file = "/earth_down/" + str(time.strftime('%Y_%m_%d', time.localtime(time.time()))) + "/"


def set_desktop(pic_path):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "0.5")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic_path, 1 + 2)


# 获取当前图片url
# http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json?uid=时间戳 获取最新的图片时间
def getPic_url():
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/67.0.3396.87 Safari/537.36', "Content-Type": "application/json"}
    url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json?uid=' + str(int(round(time.time() * 1000)))
    print(url)
    try:
        # 代理
        # proxy = "http://202.182.117.203:443"
        # proxy_support = request.ProxyHandler({'http': proxy})
        # opener = request.build_opener(proxy_support)
        # request.install_opener(opener)

        req = request.Request(url=url, headers=header_dict)
        res = request.urlopen(req)
        res_json = json.loads(res.read())
        date = res_json["date"]
        # date = '2018-06-20 01:10:00'
        hour_url = time.strftime("%Y/%m/%d/%H%M%S", time.strptime(date, "%Y-%m-%d %H:%M:%S"))
        pic_url = base_url + hour_url + "_0_0.png"
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return pic_url
    except urllib.error.URLError as e:
        print(e.reason)
        return None


# 下载图片
def down_pic(pic_url):
    hour = str(time.strftime('%H-%M-%S', time.localtime(time.time())))
    pic_name = cwd + file + hour + ".png"
    try:
        conn = urllib.request.urlopen(pic_url)
        f = open(pic_name, 'wb')
        f.write(conn.read())
        f.close()
        print(pic_name + ' Saved!')
        return pic_name
    except urllib.error.URLError as e:
        print(e.reason)
        down_pic(pic_url)


def main():
    if not os.path.exists(cwd + file):
        os.mkdir(cwd + file)
    while True:
        pic_url = getPic_url()
        if pic_url is None:
            print("连接异常2S后继续获取")
            time.sleep(2)
        else:
            print("pic_url:"+pic_url)
            pic_name = down_pic(pic_url)
            set_desktop(pic_name)
            time.sleep(60 * 10)


main()
