from datetime import datetime

class InvoiceLogic:
    def __init__(self, ui_instance):
        self.ui = ui_instance
        self.setup_connections()
        self.imageFiles = []
        self.currentImageIndex = -1

    def setup_connections(self):
        # 连接信号和槽
        self.ui.openImageFolderSignal.connect(self.openImageFolder)
        self.ui.loadPreviousImageSignal.connect(self.loadPreviousImage)
        self.ui.loadNextImageSignal.connect(self.loadNextImage)
        self.ui.performOCRSignal.connect(self.performOCR)
        self.ui.writeToExcelSignal.connect(self.writeToExcel)

    def openImageFolder(self):
        # 使用 QFileDialog 打开文件夹并更新 imageFiles 列表
        folder = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        if folder:
            self.imageFiles = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            if self.imageFiles:
                self.currentImageIndex = 0
                self.showImageByIndex(self.currentImageIndex)

    def loadPreviousImage(self):
        if self.currentImageIndex > 0:
            self.currentImageIndex -= 1
            self.showImageByIndex(self.currentImageIndex)

    def loadNextImage(self):
        if self.currentImageIndex < len(self.imageFiles) - 1:
            self.currentImageIndex += 1
            self.showImageByIndex(self.currentImageIndex)

    def showImageByIndex(self, index):
        if 0 <= index < len(self.imageFiles):
            pixmap = QPixmap(self.imageFiles[index])
            scaledPixmap = pixmap.scaled(self.ui.imageLabel.width(), self.ui.imageLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.imageLabel.setPixmap(scaledPixmap)
            self.ui.imagePathLabel.setText(f'图片路径: {self.imageFiles[index]}')

    def resetRadioButtons(self):
        # 断开文本框内容变化信号，以避免自动触发单选按钮选中
        self.ui.dateEdit.textChanged.disconnect()
        self.ui.amountEdit.textChanged.disconnect()

        # 重置单选按钮和文本框
        self.ui.dateRadioButton1.setChecked(True)
        self.ui.amountRadioButton1.setChecked(True)
        self.ui.purposeRadioButton1.setChecked(True)
        self.ui.dateEdit.clear()
        self.ui.amountEdit.clear()
        self.ui.supplementalInfoEdit.clear()
        self.ui.dateLabel1.setText("未識別")
        self.ui.amountLabel1.setText("未識別")
        self.ui.amountLabel2.setText("未識別")

        # 重新连接文本框内容变化信号
        self.ui.dateEdit.textChanged.connect(lambda: self.ui.dateRadioButton2.setChecked(True))
        self.ui.amountEdit.textChanged.connect(lambda: self.ui.amountRadioButton3.setChecked(True))


    def performOCR(self):
        if self.currentImageIndex != -1 and self.imageFiles:
            ocrMgr = OcrMgrMac()
            ocrResult = ocrMgr.ocr_file(self.imageFiles[self.currentImageIndex])
            # 检查 ocrResult 是否是有效的字符串
            if not isinstance(ocrResult, str):
                print("OCR 識別した結果は有効な文字列ではない。結果：", ocrResult)
                return  # 或者处理错误
            ocrDate, ocrValueMax, ocrValueSecondMax = extract_date_amount(ocrResult)

            # 更新OCR结果到界面
            self.ui.dateLabel1.setText(ocrDate[0] if ocrDate else "未識別")
            self.ui.amountLabel1.setText(f"¥{ocrValueMax}" if ocrValueMax is not None else "未識別")
            self.ui.amountLabel2.setText(f"¥{ocrValueSecondMax}" if ocrValueSecondMax is not None else "未識別")
            


    def writeToExcel(self):
        # 获取选中的日期
        selected_date = self.ui.dateEdit.text() if self.ui.dateRadioButton2.isChecked() else self.ui.dateLabel1.text()
        # 检查日期格式是否正确，假设正确格式为 'YYYYMMDD'
        try:
            # 尝试将日期字符串转换为日期对象，以验证其格式
            datetime.strptime(selected_date, "%Y%m%d")
        except ValueError:
            # 如果转换失败，显示错误消息并返回
            QMessageBox.warning(self.ui, "警告", "日期格式不正确，应为 'YYYYMMDD'")
            return

        # 获取选中的金额
        if self.ui.amountRadioButton1.isChecked():
            selected_amount = self.ui.amountLabel1.text()
        elif self.ui.amountRadioButton2.isChecked():
            selected_amount = self.ui.amountLabel2.text()
        else:
            selected_amount = self.ui.amountEdit.text()

        # 获取选中的用途
        if self.ui.purposeRadioButton1.isChecked():
            selected_purpose = "招待交際"
        elif self.ui.purposeRadioButton2.isChecked():
            selected_purpose = "旅費"
        elif self.ui.purposeRadioButton3.isChecked():
            selected_purpose = "雑費"
        else:
            selected_purpose = "消耗品"

        # 获取补充说明
        supplemental_info = self.ui.supplementalInfoEdit.text()

        # 获取文件路径和文件名
        if self.currentImageIndex != -1 and self.imageFiles:
            file_path = self.imageFiles[self.currentImageIndex]
            file_name = os.path.basename(file_path)

            # 调用处理函数，如 process_file
            # 此处您需要确保 process_file 函数接受所有这些参数
            process_file(selected_date, selected_amount, selected_purpose, supplemental_info, file_path)

            # 显示信息
            msg = (f"日付: {selected_date}\n"
                f"金額: {selected_amount}\n"
                f"目的: {selected_purpose}\n"
                f"補足: {supplemental_info}\n"
                f"ファイルパス: {file_path}\n"
                f"ファイル名: {file_name}")
            QMessageBox.information(self.ui, "情報", msg)
        else:
            QMessageBox.warning(self.ui, "警告", "没有选择任何文件")

        self.resetRadioButtons()


# 在您的主程序文件中，创建UI和逻辑实例
if __name__ == '__main__':
    from PyQt5.QtWidgets import QMessageBox, QFileDialog
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtCore import Qt
    import os
    from PyQt5.QtWidgets import QApplication
    from invoiceAppUI import InvoiceApp
    import sys

    from ocr_mgr_mac import OcrMgrMac
    from valueAndDate import extract_date_amount
    from dealExcel import process_file

    app = QApplication(sys.argv)
    ui = InvoiceApp()
    logic = InvoiceLogic(ui)
    ui.show()
    sys.exit(app.exec_())
