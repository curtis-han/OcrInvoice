import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

class InvoiceApp(QWidget):
    # 定义信号
    openImageFolderSignal = pyqtSignal()
    loadPreviousImageSignal = pyqtSignal()
    loadNextImageSignal = pyqtSignal()
    performOCRSignal = pyqtSignal()
    writeToExcelSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1200, 800)  # 增加窗口大小
        self.mainLayout = QHBoxLayout()  # 主布局

        self.leftLayout = QVBoxLayout()  # 左侧布局
        self.rightLayout = QVBoxLayout()  # 右侧布局

        # 左侧布局组件
        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(650, 750)  # 增加图片标签大小
        self.leftLayout.addWidget(self.imageLabel)

        # 右侧布局组件
        self.imagePathLabel = QLabel('图片路径: ', self)
        self.openImageButton = QPushButton('打开图片文件夹', self)
        self.openImageButton.clicked.connect(self.openImageFolderSignal.emit)
        self.prevImageButton = QPushButton('PREVIOUS', self)
        self.prevImageButton.clicked.connect(self.loadPreviousImageSignal.emit)
        self.nextImageButton = QPushButton('NEXT', self)
        self.nextImageButton.clicked.connect(self.loadNextImageSignal.emit)
        self.runOCRButton = QPushButton('OCR識別実行', self)
        self.runOCRButton.clicked.connect(self.performOCRSignal.emit)

        # 日期选择布局
        dateLayout = QHBoxLayout()
        self.dateGroup = QButtonGroup(self)
        self.dateRadioButton1 = QRadioButton("OCR識別日付け", self)
        self.dateRadioButton1.setChecked(True)
        self.dateGroup.addButton(self.dateRadioButton1)
        self.dateLabel1 = QLabel("未識別", self)
        dateLayout.addWidget(self.dateRadioButton1)
        dateLayout.addWidget(self.dateLabel1)

        dateManualLayout = QHBoxLayout()
        self.dateRadioButton2 = QRadioButton("手動入力日付", self)
        self.dateGroup.addButton(self.dateRadioButton2)
        self.dateEdit = QLineEdit(self)
        self.dateEdit.textChanged.connect(lambda: self.dateRadioButton2.setChecked(True))
        dateManualLayout.addWidget(self.dateRadioButton2)
        dateManualLayout.addWidget(self.dateEdit)

        # 金额选择布局
        amountLayout = QHBoxLayout()
        self.amountGroup = QButtonGroup(self)
        self.amountRadioButton1 = QRadioButton("識別最大金額", self)
        self.amountRadioButton1.setChecked(True)
        self.amountGroup.addButton(self.amountRadioButton1)
        self.amountLabel1 = QLabel("未識別", self)
        amountLayout.addWidget(self.amountRadioButton1)
        amountLayout.addWidget(self.amountLabel1)

        self.amountRadioButton2 = QRadioButton("識別第二大金額", self)
        self.amountGroup.addButton(self.amountRadioButton2)
        self.amountLabel2 = QLabel("未識別", self)
        amountLayout.addWidget(self.amountRadioButton2)
        amountLayout.addWidget(self.amountLabel2)

        amountManualLayout = QHBoxLayout()
        self.amountRadioButton3 = QRadioButton("手動入力金額", self)
        self.amountGroup.addButton(self.amountRadioButton3)
        self.amountEdit = QLineEdit(self)
        self.amountEdit.textChanged.connect(lambda: self.amountRadioButton3.setChecked(True))
        amountManualLayout.addWidget(self.amountRadioButton3)
        amountManualLayout.addWidget(self.amountEdit)

        # 写入Excel按钮
        self.writeToExcelButton = QPushButton('Excelに書き込む', self)
        self.writeToExcelButton.clicked.connect(self.writeToExcelSignal.emit)

        # 用途选择组件
        purposeLayout = QHBoxLayout()
        self.purposeGroup = QButtonGroup(self)
        self.purposeRadioButton1 = QRadioButton("招待交際", self)
        self.purposeGroup.addButton(self.purposeRadioButton1)
        purposeLayout.addWidget(self.purposeRadioButton1)

        self.purposeRadioButton2 = QRadioButton("旅費", self)
        self.purposeGroup.addButton(self.purposeRadioButton2)
        purposeLayout.addWidget(self.purposeRadioButton2)

        self.purposeRadioButton3 = QRadioButton("雑費", self)
        self.purposeGroup.addButton(self.purposeRadioButton3)
        purposeLayout.addWidget(self.purposeRadioButton3)

        self.purposeRadioButton4 = QRadioButton("消耗品", self)
        self.purposeGroup.addButton(self.purposeRadioButton4)
        purposeLayout.addWidget(self.purposeRadioButton4)
        self.purposeRadioButton1.setChecked(True)

        # 补充说明文本框
        supplementalInfoLayout = QHBoxLayout()
        self.supplementalInfoLabel = QLabel('補充説明: ', self)
        self.supplementalInfoEdit = QLineEdit(self)
        # 将标签和文本框添加到水平布局中
        supplementalInfoLayout.addWidget(self.supplementalInfoLabel)
        supplementalInfoLayout.addWidget(self.supplementalInfoEdit)

        # 将右侧布局组件添加到右侧布局
        self.rightLayout.addWidget(self.imagePathLabel)
        self.rightLayout.addWidget(self.openImageButton)
        self.rightLayout.addWidget(self.prevImageButton)
        self.rightLayout.addWidget(self.nextImageButton)
        self.rightLayout.addWidget(self.runOCRButton)
        self.rightLayout.addLayout(purposeLayout)
        self.rightLayout.addLayout(dateLayout)
        self.rightLayout.addLayout(dateManualLayout)
        self.rightLayout.addLayout(amountLayout)
        self.rightLayout.addLayout(amountManualLayout)
        self.rightLayout.addLayout(supplementalInfoLayout)
        self.rightLayout.addWidget(self.writeToExcelButton)

        # 设置主布局
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.setLayout(self.mainLayout)
        self.setWindowTitle('OCR実行')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InvoiceApp()
    ex.show()
    sys.exit(app.exec_())
