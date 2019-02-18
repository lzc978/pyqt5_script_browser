#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用 PyQt5 内嵌浏览器浏览网页，并注入 Javascript 脚本实现自动化操作。"""
import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout,
    QDesktopWidget, QTextEdit, QLabel, QLineEdit, QPushButton,
    QFileDialog, QProgressBar,
)
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript, QWebEnginePage


class Browser(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

        # 脚本
        self.profile = QWebEngineProfile.defaultProfile()
        self.script = QWebEngineScript()
        self.prepare_script()

    def init_ui(self):
        self.webView = QWebEngineView()

        self.logEdit = QTextEdit()
        self.logEdit.setFixedHeight(100)

        self.addrEdit = QLineEdit()
        self.addrEdit.returnPressed.connect(self.load_url)
        self.webView.urlChanged.connect(
            lambda i: self.addrEdit.setText(i.toDisplayString()))

        self.jsEdit = QLineEdit()
        self.jsEdit.setText('inject.js')

        loadUrlBtn = QPushButton('加载')
        loadUrlBtn.clicked.connect(self.load_url)

        chooseJsBtn = QPushButton('选择脚本文件')
        chooseJsBtn.clicked.connect(self.choose_js_file)

        # 导航/工具
        top = QWidget()
        top.setFixedHeight(80)
        topBox = QVBoxLayout(top)
        topBox.setSpacing(0)
        topBox.setContentsMargins(5, 0, 0, 5)

        progBar = QProgressBar()
        progBox = QHBoxLayout()
        progBox.addWidget(progBar)
        topBox.addLayout(progBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('网址'))
        naviBox.addWidget(self.addrEdit)
        naviBox.addWidget(loadUrlBtn)
        topBox.addLayout(naviBox)

        naviBox = QHBoxLayout()
        naviBox.addWidget(QLabel('注入脚本文件'))
        naviBox.addWidget(self.jsEdit)
        naviBox.addWidget(chooseJsBtn)
        topBox.addLayout(naviBox)

        self.webView.loadProgress.connect(progBar.setValue)

        # 主界面
        layout = QVBoxLayout(self)
        layout.addWidget(self.webView)
        layout.addWidget(top)
        layout.addWidget(self.logEdit)

        self.show()
        self.resize(1024, 900)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def load_url(self):
        url = self.addrEdit.text().strip()
        if not url.lower().startswith('http://') \
                and not url.lower().startswith('https://'):
            url = 'http://{}'.format(url)
        self.load(url)

    @pyqtSlot()
    def choose_js_file(self):
        f, _ = QFileDialog.getOpenFileName(filter="Javascript files(*.js)")
        if os.path.isfile(f):
            self.jsEdit.setText(f)
            self.prepare_script()

    def prepare_script(self):
        path = self.jsEdit.text().strip()
        if not os.path.isfile(path):
            self.log('invalid js path')
            return

        self.profile.scripts().remove(self.script)
        with open(path, 'r') as f:
            self.script.setSourceCode(f.read())
        self.profile.scripts().insert(self.script)
        self.log('injected js ready')

    def log(self, msg, *args, **kwargs):
        m = msg.format(*args, **kwargs)
        self.logEdit.append('{} {}'.format(
            datetime.now().strftime('%H:%M:%S'), m))

    def load(self, url):
        self.log(f'loading {url}')
        self.addrEdit.setText(url)
        self.webView.load(QUrl(url))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    b = Browser()
    b.load('http://www.flyscoot.com/')
    sys.exit(app.exec_())