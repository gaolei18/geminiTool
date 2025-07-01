

import pyautogui
import pytesseract
from PIL import Image

# --- 配置 ---
# !! 重要：请将下面的路径修改为你自己电脑上 Tesseract-OCR 的安装路径 !!
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def find_and_click_text(text_to_find):
    """
    在屏幕上查找指定的文本，并将其定位，然后用鼠标点击它。

    Args:
        text_to_find (str): 你想要在屏幕上查找和点击的字符串。
    """
    print(f"正在屏幕上搜索文本: '{text_to_find}'...")

    # 1. 截取整个屏幕的图像
    screenshot = pyautogui.screenshot()
    # 你也可以保存截图来调试，取消下面的注释即可
    # screenshot.save("debug_screenshot.png")

    # 2. 使用 Tesseract OCR 来识别图像中的文字和位置信息
    # 使用 image_to_data 而不是 image_to_string 来获取每个词的详细数据
    try:
        ocr_data = pytesseract.image_to_data(screenshot, lang='chi_sim', output_type=pytesseract.Output.DICT)
    except pytesseract.TesseractNotFoundError:
        print("错误：Tesseract-OCR 未找到。")
        print(f"请确保 Tesseract 已安装，并且 pytesseract.pytesseract.tesseract_cmd 的路径设置正确。")
        print(f"当前设置的路径是: '{pytesseract.pytesseract.tesseract_cmd}'")
        return

    # 3. 遍历识别结果，查找匹配的文本
    found = False
    n_boxes = len(ocr_data['level'])
    for i in range(n_boxes):
        # 我们只关心识别出的单词
        if int(ocr_data['conf'][i]) > 60: # conf 是置信度 (0-100)
            recognized_text = ocr_data['text'][i].strip()
            if text_to_find.lower() in recognized_text.lower():
                # 找到了！获取它的位置和大小
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]

                # 计算中心点
                center_x = x + w // 2
                center_y = y + h // 2

                print(f"成功找到文本! 位置: (x={x}, y={y}), 大小: (w={w}, h={h})")
                print(f"移动鼠标到: ({center_x}, {center_y}) 并点击。")

                # 4. 移动鼠标并点击
                pyautogui.moveTo(center_x, center_y, duration=0.5)
                pyautogui.click()
                
                found = True
                break # 找到第一个匹配项后就退出循环

    if not found:
        print(f"未能在屏幕上找到文本: '{text_to_find}'")

# --- 测试 ---
if __name__ == "__main__":
    # ** 使用前请修改下面的文本为你想要测试的字符串 **
    # 例如，你可以打开一个记事本窗口，然后尝试查找 "文件" 或 "编辑"
    
    # 等待几秒钟，给你时间切换到目标窗口
    print("脚本将在 3 秒后开始运行，请准备好你要操作的窗口...")
    pyautogui.sleep(3)

    # 要查找的文本 (请修改)
    target_text = "脚本" # 这是一个英文例子，你可以改成 "文件"
    
    find_and_click_text(target_text)

