# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QLabel,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 750)
        self.actionSave_Video = QAction(MainWindow)
        self.actionSave_Video.setObjectName(u"actionSave_Video")
        self.actionFlip_Horizontally = QAction(MainWindow)
        self.actionFlip_Horizontally.setObjectName(u"actionFlip_Horizontally")
        self.actionFlip_Vertically = QAction(MainWindow)
        self.actionFlip_Vertically.setObjectName(u"actionFlip_Vertically")
        self.actionFlip_Both_Sides = QAction(MainWindow)
        self.actionFlip_Both_Sides.setObjectName(u"actionFlip_Both_Sides")
        self.actionAdd_Image = QAction(MainWindow)
        self.actionAdd_Image.setObjectName(u"actionAdd_Image")
        self.actionAdd_Text = QAction(MainWindow)
        self.actionAdd_Text.setObjectName(u"actionAdd_Text")
        self.actionChange_Text = QAction(MainWindow)
        self.actionChange_Text.setObjectName(u"actionChange_Text")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionAdd_Frame = QAction(MainWindow)
        self.actionAdd_Frame.setObjectName(u"actionAdd_Frame")
        self.actionDelete_Frame = QAction(MainWindow)
        self.actionDelete_Frame.setObjectName(u"actionDelete_Frame")
        self.actionSave_Image = QAction(MainWindow)
        self.actionSave_Image.setObjectName(u"actionSave_Image")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(1020, 620, 104, 31))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(960, 620, 61, 31))
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(19, 10, 1111, 600))
        self.graphicsView.setFrameShape(QFrame.Shape.Box)
        self.graphicsView.setFrameShadow(QFrame.Shadow.Sunken)
        self.graphicsView_2 = QGraphicsView(self.centralwidget)
        self.graphicsView_2.setObjectName(u"graphicsView_2")
        self.graphicsView_2.setGeometry(QRect(20, 659, 1111, 31))
        self.graphicsView_2.setFrameShape(QFrame.Shape.Box)
        self.graphicsView_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.graphicsView_2.setLineWidth(2)
        self.graphicsView_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 25))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionSave_Image)
        self.menuFile.addAction(self.actionSave_Video)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAdd_Image)
        self.menuFile.addAction(self.actionAdd_Text)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAdd_Frame)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Create A Video", None))
        self.actionSave_Video.setText(QCoreApplication.translate("MainWindow", u"Save Video", None))
        self.actionFlip_Horizontally.setText(QCoreApplication.translate("MainWindow", u"Flip Horizontally", None))
        self.actionFlip_Vertically.setText(QCoreApplication.translate("MainWindow", u"Flip Vertically", None))
        self.actionFlip_Both_Sides.setText(QCoreApplication.translate("MainWindow", u"Flip Both Sides", None))
        self.actionAdd_Image.setText(QCoreApplication.translate("MainWindow", u"Add Image", None))
        self.actionAdd_Text.setText(QCoreApplication.translate("MainWindow", u"Add Text", None))
        self.actionChange_Text.setText(QCoreApplication.translate("MainWindow", u"Change Text", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionAdd_Frame.setText(QCoreApplication.translate("MainWindow", u"Add Frame", None))
        self.actionDelete_Frame.setText(QCoreApplication.translate("MainWindow", u"Delete Frame", None))
        self.actionSave_Image.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"seconds", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Duration:", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

