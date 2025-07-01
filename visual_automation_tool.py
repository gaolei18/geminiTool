import pyautogui
import pytesseract
from PIL import Image

class ScreenTextClickHandler:
    """
    一个封装了在屏幕上查找文本并进行鼠标操作的工具类。
    """
    def __init__(self, tesseract_path=r'D:\Program Files\Tesseract-OCR\tesseract.exe'):
        """
        初始化工具类，并设置 Tesseract-OCR 的路径。

        Args:
            tesseract_path (str): Tesseract-OCR 可执行文件的绝对路径。
        """
        # 验证并设置 Tesseract 命令路径
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            # 尝试获取版本号以验证路径是否正确
            pytesseract.get_tesseract_version()
        except (pytesseract.TesseractNotFoundError, FileNotFoundError):
            raise EnvironmentError(
                f"Tesseract-OCR 未在指定路径找到: '{tesseract_path}'. "
                "请确保路径正确，并且 Tesseract 已正确安装。"
            )

    def find_and_click(self, text_to_find, lang='chi_sim', confidence_threshold=60):
        """
        在屏幕上查找指定的文本，并移动鼠标到其中心位置进行单击。

        Args:
            text_to_find (str): 需要在屏幕上查找和点击的文本。
            lang (str): Tesseract 使用的语言包 (例如 'eng' for English, 'chi_sim' for Simplified Chinese)。
            confidence_threshold (int): 识别文本的置信度阈值 (0-100)。只处理高于此阈值的识别结果。

        Returns:
            dict: 一个包含操作结果的字典。
                  成功: {'success': True, 'location': (x, y)}
                  失败: {'success': False, 'message': '错误信息'}
        """
        print(f"正在屏幕上搜索文本: '{text_to_find}' (语言: {lang})")

        # 1. 截取屏幕
        screenshot = pyautogui.screenshot()

        # 2. 使用 Tesseract OCR 识别文字和位置
        try:
            ocr_data = pytesseract.image_to_data(
                screenshot, 
                lang=lang, 
                output_type=pytesseract.Output.DICT
            )
        except pytesseract.TesseractError as e:
            return {'success': False, 'message': f"Tesseract OCR 识别出错: {e}"}

        # 3. 遍历识别结果，查找匹配的文本
        n_boxes = len(ocr_data['level'])
        for i in range(n_boxes):
            # 只关心置信度足够高的单词
            if int(ocr_data['conf'][i]) > confidence_threshold:
                recognized_text = ocr_data['text'][i].strip()
                
                # 使用 'in' 来进行模糊匹配
                if text_to_find.lower() in recognized_text.lower():
                    # 获取位置和大小
                    x, y, w, h = (
                        ocr_data['left'][i],
                        ocr_data['top'][i],
                        ocr_data['width'][i],
                        ocr_data['height'][i],
                    )

                    # 计算中心点
                    center_x = x + w // 2
                    center_y = y + h // 2

                    print(f"成功找到文本! 位置: ({x}, {y}), 大小: ({w}, {h})")
                    print(f"移动鼠标到中心点: ({center_x}, {center_y}) 并点击。")

                    # 4. 移动鼠标并单击
                    pyautogui.moveTo(center_x, center_y, duration=0.5)
                    pyautogui.click()
                    
                    return {'success': True, 'location': (center_x, center_y)}

        print(f"未能在屏幕上找到文本: '{text_to_find}'")
        return {'success': False, 'message': f"Text '{text_to_find}' not found on screen."}

# --- 使用示例 ---
if __name__ == '__main__':
    print("这是一个工具类的使用示例。")
    
    try:
        # 1. 初始化工具
        # Tesseract 的路径在 __init__ 中已经有了默认值，如果你的路径不同，可以在这里传入
        tool = ScreenTextClickHandler()

        # 2. 准备测试环境
        print("脚本将在 3 秒后开始查找并点击“脚本”二字。")
        print("请确保屏幕上清晰可见“脚本”这两个字。")
        pyautogui.sleep(3)

        # 3. 调用方法
        target = "脚本"
        result = tool.find_and_click(target)

        # 4. 打印结果
        print("\n--- 操作结果 ---")
        if result['success']:
            print(f"成功点击了 '{target}'，位于坐标: {result['location']}")
        else:
            print(f"操作失败: {result['message']}")

    except EnvironmentError as e:
        print(f"初始化失败: {e}")
