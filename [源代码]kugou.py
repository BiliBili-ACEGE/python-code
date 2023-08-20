import sys
import urllib.request
import eyed3
import requests
import re
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt

class SongDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("酷狗音乐下载器")
        self.setGeometry(0, 0, 1920, 1080)
        self.center_window()


        # 设置图标
        self.setWindowIcon(QIcon("icon.png"))

        self.label = QLabel("请输入需要下载的酷狗歌曲播放页网址:", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 200, 1920, 50)

        self.url_entry = QLineEdit(self)
        self.url_entry.setGeometry(400, 300, 1120, 50)
        self.url_entry.setAlignment(Qt.AlignCenter)

        self.download_button = QPushButton("下载音乐", self)
        self.download_button.setGeometry(700, 400, 520, 50)
        self.download_button.clicked.connect(self.download_song)

        self.music_info_label = QLabel("", self)
        self.music_info_label.setAlignment(Qt.AlignCenter)
        self.music_info_label.setGeometry(0, 500, 1920, 50)

    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        self.move(screen_rect.center() - self.rect().center())

    def set_background_color(self, color):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def download_song(self):
        url = self.url_entry.text()

        matches = ["https://www.kugou.com/mixsong/", ".html"]

        if all(x in url for x in matches):
            # 构造请求头
            heads = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
            }

            # 发送请求包
            myrequest = urllib.request.Request(url=url, headers=heads)
            mylogin = urllib.request.urlopen(myrequest)

            # 正则表达式
            rule = r'\["(.*?)\.mp3\"\]'

            # 将文本转化为字符串
            contentwb = mylogin.read()
            tempstr = contentwb.decode('utf-8')

            # 读取链接
            webpage = re.findall(rule, tempstr)
            pagestr = (webpage[0].replace('\\/', '/')) + ".mp3"

            # 文件命名
            audiofile = requests.get(pagestr)
            counter = 1
            flag = True

            # 写到文件，避免同名覆盖
            while flag:
                if os.path.exists(f"./download_{counter}.mp3"):
                    counter += 1
                else:
                    open(f"./download_{counter}.mp3", "wb").write(audiofile.content)
                    flag = False

            # 读取音频信息
            audio = eyed3.load(f"./download_{counter}.mp3")
            title = audio.tag.title
            artist = audio.tag.artist

            # 判断是否有音频信息
            if title:
                os.rename(f"./download_{counter}.mp3", f"./{title}.mp3")
                self.music_info_label.setText(f"音乐名称：{title}\n艺术家：{artist}")
                QMessageBox.information(self, "下载完成", f"音频 {title}.mp3 已下载完成！")
            else:
                self.music_info_label.setText("音频下载完成，但读取音频名失败，请自行命名！")
                QMessageBox.warning(self, "下载完成", f"音频下载完成，但读取音频名失败，请自行命名！")
        else:
            QMessageBox.critical(self, "错误", "不正确的网址！请输入酷狗的歌曲播放页网址！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SongDownloaderApp()
    window.show()
    sys.exit(app.exec_())
