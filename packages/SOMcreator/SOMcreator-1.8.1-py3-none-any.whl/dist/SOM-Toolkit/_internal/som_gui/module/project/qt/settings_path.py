# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsPath.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
                               QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(621, 96)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.la_project_path = QLabel(Form)
        self.la_project_path.setObjectName(u"la_project_path")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.la_project_path)

        self.le_project_path = QLineEdit(Form)
        self.le_project_path.setObjectName(u"le_project_path")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_project_path)

        self.le_save_path = QLineEdit(Form)
        self.le_save_path.setObjectName(u"le_save_path")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.le_save_path)

        self.la_save_path = QLabel(Form)
        self.la_save_path.setObjectName(u"la_save_path")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.la_save_path)

        self.le_open_path = QLineEdit(Form)
        self.le_open_path.setObjectName(u"le_open_path")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.le_open_path)

        self.la_open_path = QLabel(Form)
        self.la_open_path.setObjectName(u"la_open_path")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.la_open_path)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.la_project_path.setText(QCoreApplication.translate("Form", u"Projekt Pfad:", None))
        self.la_save_path.setText(QCoreApplication.translate("Form", u"Speicher Pfad:", None))
        self.la_open_path.setText(QCoreApplication.translate("Form", u"\u00d6ffnen Pfad:", None))
    # retranslateUi

