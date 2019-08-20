import sys
import os
# from PySide2.QtWidgets import QStyle
from PyQt5.QtCore import Qt
import PyQt5.QtCore as Core
import PyQt5.QtMultimedia as Media
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QSlider, QVBoxLayout, QComboBox, QHBoxLayout)


class Player(QWidget):
    def __init__(self, filename):
        self.app = QApplication(sys.argv)
        self.filename = filename
        self.player = Media.QMediaPlayer()
        self.value = 0

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 50)
        self.setWindowTitle(self.filename)
        self.setFixedSize(300, 50)

        btn = QPushButton('Play/Pause', self)
        btn.setToolTip('Play/Pause')
        # btn.resize(50, 50)
        btn.clicked.connect(self.pause)

        volumeSlider =\
            QSlider(Qt.Vertical, sliderMoved=self.player.setVolume)
        volumeSlider.setRange(0, 100)
        volumeSlider.setValue(100)
        volumeSlider.setToolTip('Volume')

        self.slider = QSlider(Qt.Horizontal, sliderMoved=self.seek)
        self.slider.setToolTip('Seek')
        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.valueChanged.connect(self.slider_click)
        # self.slider.mousePressEvent = self.rewind
        # self.slider.resize(100, 50)

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(self.slider)
        hbox.addWidget(volumeSlider)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.app.quit()
        elif e.key() == Qt.Key_Space:
            self.pause()

    def play(self):
        url = Core.QUrl.fromLocalFile(os.path.abspath(self.filename))
        content = Media.QMediaContent(url)

        self.player.setMedia(content)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.set_duration)
        self.player.play()
        # self.player.stateChanged.connect(self.app.quit)

        self.app.exec_()

    def pause(self):
        if self.player.state() == Media.QMediaPlayer.PausedState:
            self.player.play()
        else:
            self.player.pause()

    def seek(self, seconds):
        self.player.setPosition(seconds * 1000)

    def position_changed(self, position):
        position /= 1000
        self.slider.setValue(position)
        self.value = position

    def set_duration(self, e):
        self.slider.setRange(0, self.player.duration() / 1000)

    def slider_click(self, position):
        if abs(position - self.value) > 9:
            self.player.setPosition(position * 1000)
        self.value = position
