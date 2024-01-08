import subprocess
import os
import sys

from PyQt5.QtWidgets import QMessageBox

class OcrMgrMac():
    def __init__(self) -> None:
        pass

    def ocr_file(self, pic_name):
        if getattr(sys, 'frozen', False):
            # 打包后的应用程序
            app_dir = os.path.dirname(sys.executable)
            resource_dir = os.path.join(app_dir, '..', 'Resources')
            bash_name = os.path.join(resource_dir, "ocr.sh")
        else:
            # 开发环境
            app_dir = os.path.dirname(os.path.abspath(__file__))
            bash_name = os.path.join(app_dir, "ocr.sh")

        #pic_name = os.path.join(app_dir, pic_name)  # 确保图片路径也是正确的
        cmd = ["sh", bash_name, pic_name]
        try:
            # 使用subprocess运行Shell脚本，捕获标准输出
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            print("Shell脚本执行成功")
            print("标准输出:")
            print(result.stdout)
            return result.stdout  # 返回OCR的结果
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(None, "执行错误", f"Shell脚本执行失败: {str(e)}\n标准错误: {e.stderr}")
            print("Shell脚本执行失败:", e)
            print("标准错误:")
            print(e.stderr)
            return None  # 发生错误时返回None
        except FileNotFoundError:
            QMessageBox.critical(None, "文件未找到", f"找不到Shell脚本文件: {bash_name}")
            print("找不到Shell脚本文件:", bash_name)
            return None  # 发生错误时返回None

if __name__ == "__main__":
    """
    test用main
    """
    testOcrMac = OcrMgrMac()
    print(testOcrMac.ocr_file("../INPUT/test.jpg"))
