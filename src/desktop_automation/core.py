
import pyautogui
import pytesseract
from PIL import Image
import time
import json
import os
from datetime import datetime
import io
import base64

# --- Configuration ---
LOGS_DIR = "logs"
SUCCESSFUL_WORKFLOWS_DIR = "successful_workflows"
TEMP_DIR = os.path.join(LOGS_DIR, "temp") # For temporary files like templates
os.makedirs(TEMP_DIR, exist_ok=True)

# --- Core Logging Functions ---

def _log_action(log_file_path, action_name, params, status, result):
    if not log_file_path: return
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action_name,
        "parameters": params,
        "status": status,
        "result": result
    }
    try:
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Error writing to log file {log_file_path}: {e}")

def start_task_log():
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"task_{timestamp}.jsonl"
    log_file_path = os.path.join(LOGS_DIR, filename)
    with open(log_file_path, 'w') as f: pass
    print(f"Task started. Logging to: {log_file_path}")
    return log_file_path

def end_task_with_verdict(log_file_path, status, user_feedback=""):
    params = {"status": status, "user_feedback": user_feedback}
    _log_action(log_file_path, "task_verdict", params, status, f"Task ended with status: {status}")
    print(f"Task ended. Verdict '{status}' recorded in {log_file_path}")


# --- Helper Functions ---
def _get_image_from_base64(base64_string):
    """Decodes a base64 string into a PIL Image."""
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data))

# --- Enhanced Vision Functions ---
def analyze_screen_state(log_file_path=None):
    """
    Captures screenshot and performs OCR to understand current screen content.
    Returns a dictionary with screen analysis results.
    """
    params = {}
    try:
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Perform OCR on entire screen with better config
        # 尝试多种语言和配置
        try:
            # 首先尝试中英文混合识别
            screen_text = pytesseract.image_to_string(screenshot, lang='chi_sim+eng', config='--psm 6')
        except:
            try:
                # 如果没有中文包，尝试英文
                screen_text = pytesseract.image_to_string(screenshot, config='--psm 6')
            except:
                # 最后使用默认配置
                screen_text = pytesseract.image_to_string(screenshot)
        
        # Get screen dimensions
        screen_width, screen_height = screenshot.size
        
        # Analyze screen content
        analysis = {
            "screen_size": {"width": screen_width, "height": screen_height},
            "detected_text": screen_text.strip(),
            "text_lines": [line.strip() for line in screen_text.split('\n') if line.strip()],
            "timestamp": datetime.now().isoformat()
        }
        
        result = f"Screen analyzed: {len(analysis['text_lines'])} text lines detected"
        _log_action(log_file_path, "analyze_screen_state", params, "success", result)
        return analysis
        
    except Exception as e:
        result = f"Error analyzing screen state: {e}"
        _log_action(log_file_path, "analyze_screen_state", params, "error", result)
        return {"error": str(e)}

def find_text_on_screen(target_text, log_file_path=None):
    """
    Searches for specific text on screen and returns its approximate location.
    Returns coordinates if found, None if not found.
    """
    params = {"target_text": target_text}
    try:
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Get OCR data with bounding boxes using better config
        try:
            # 首先尝试中英文混合识别
            ocr_data = pytesseract.image_to_data(screenshot, lang='chi_sim+eng', config='--psm 6', output_type=pytesseract.Output.DICT)
        except:
            try:
                # 如果没有中文包，尝试英文
                ocr_data = pytesseract.image_to_data(screenshot, config='--psm 6', output_type=pytesseract.Output.DICT)
            except:
                # 最后使用默认配置
                ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        
        # Search for target text
        for i, text in enumerate(ocr_data['text']):
            if target_text.lower() in text.lower() and int(ocr_data['conf'][i]) > 30:  # confidence threshold
                x = ocr_data['left'][i] + ocr_data['width'][i] // 2
                y = ocr_data['top'][i] + ocr_data['height'][i] // 2
                
                result = f"Found '{target_text}' at ({x}, {y})"
                _log_action(log_file_path, "find_text_on_screen", params, "success", result)
                return {"x": x, "y": y, "confidence": ocr_data['conf'][i]}
        
        result = f"Text '{target_text}' not found on screen"
        _log_action(log_file_path, "find_text_on_screen", params, "not_found", result)
        return None
        
    except Exception as e:
        result = f"Error searching for text: {e}"
        _log_action(log_file_path, "find_text_on_screen", params, "error", result)
        return None

def wait_for_text_appear(target_text, timeout=10, check_interval=1, log_file_path=None):
    """
    Waits for specific text to appear on screen within timeout period.
    Returns True if text appears, False if timeout.
    """
    params = {"target_text": target_text, "timeout": timeout, "check_interval": check_interval}
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if find_text_on_screen(target_text, log_file_path):
                result = f"Text '{target_text}' appeared after {time.time() - start_time:.1f} seconds"
                _log_action(log_file_path, "wait_for_text_appear", params, "success", result)
                return True
            
            time.sleep(check_interval)
        
        result = f"Text '{target_text}' did not appear within {timeout} seconds"
        _log_action(log_file_path, "wait_for_text_appear", params, "timeout", result)
        return False
        
    except Exception as e:
        result = f"Error waiting for text: {e}"
        _log_action(log_file_path, "wait_for_text_appear", params, "error", result)
        return False

# --- Automation Functions (Eyes & Hands) ---

def take_screenshot(file_path="screenshot.png", log_file_path=None):
    params = {"file_path": file_path}
    try:
        screenshot_dir = os.path.dirname(file_path)
        if screenshot_dir: os.makedirs(screenshot_dir, exist_ok=True)
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        result = f"Screenshot saved to {file_path}"
        _log_action(log_file_path, "take_screenshot", params, "success", result)
        return result
    except Exception as e:
        result = f"Error taking screenshot: {e}"
        _log_action(log_file_path, "take_screenshot", params, "error", result)
        return result

def move_and_click(x, y, button='left', log_file_path=None):
    params = {"x": x, "y": y, "button": button}
    try:
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click(button=button)
        result = f"Clicked {button} button at ({x}, {y})"
        _log_action(log_file_path, "move_and_click", params, "success", result)
        return result
    except Exception as e:
        result = f"Error moving or clicking mouse: {e}"
        _log_action(log_file_path, "move_and_click", params, "error", result)
        return result

def smart_click_text(target_text, button='left', max_retries=3, log_file_path=None):
    """
    Intelligently finds and clicks on text. More reliable than hardcoded coordinates.
    """
    params = {"target_text": target_text, "button": button, "max_retries": max_retries}
    
    for attempt in range(max_retries):
        try:
            # Find text location
            location = find_text_on_screen(target_text, log_file_path)
            if location:
                # Click on the text
                pyautogui.moveTo(location['x'], location['y'], duration=0.5)
                pyautogui.click(button=button)
                
                result = f"Successfully clicked '{target_text}' at ({location['x']}, {location['y']}) on attempt {attempt + 1}"
                _log_action(log_file_path, "smart_click_text", params, "success", result)
                return result
            else:
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                else:
                    result = f"Failed to find text '{target_text}' after {max_retries} attempts"
                    _log_action(log_file_path, "smart_click_text", params, "not_found", result)
                    return result
                    
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
                continue
            else:
                result = f"Error clicking text '{target_text}': {e}"
                _log_action(log_file_path, "smart_click_text", params, "error", result)
                return result
    
    result = f"All {max_retries} attempts failed for clicking '{target_text}'"
    _log_action(log_file_path, "smart_click_text", params, "failed", result)
    return result

def verify_operation_result(expected_text, timeout=5, log_file_path=None):
    """
    Verifies that an operation was successful by checking if expected text appears.
    """
    params = {"expected_text": expected_text, "timeout": timeout}
    try:
        success = wait_for_text_appear(expected_text, timeout, 0.5, log_file_path)
        if success:
            result = f"Operation verified: '{expected_text}' found on screen"
            _log_action(log_file_path, "verify_operation_result", params, "success", result)
            return True
        else:
            result = f"Operation verification failed: '{expected_text}' not found within {timeout} seconds"
            _log_action(log_file_path, "verify_operation_result", params, "failed", result)
            return False
            
    except Exception as e:
        result = f"Error verifying operation: {e}"
        _log_action(log_file_path, "verify_operation_result", params, "error", result)
        return False

def find_and_click_image(image_description, model_analysis_base64, log_file_path=None):
    params = {"image_description": image_description}
    template_image = None
    temp_template_path = None
    try:
        template_image = _get_image_from_base64(model_analysis_base64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_template_path = os.path.join(TEMP_DIR, f"template_{timestamp}.png")
        template_image.save(temp_template_path)
        location = pyautogui.locateCenterOnScreen(temp_template_path, confidence=0.9)
        if location is None:
            raise FileNotFoundError(f"Could not find the image for '{image_description}' on the screen.")
        move_and_click(location.x, location.y, log_file_path=log_file_path)
        result = f"Successfully found and clicked '{image_description}' at {location}."
        _log_action(log_file_path, "find_and_click_image", params, "success", result)
        return result
    except Exception as e:
        result = f"Error in find_and_click_image: {e}"
        _log_action(log_file_path, "find_and_click_image", params, "error", result)
        return result
    finally:
        if temp_template_path and os.path.exists(temp_template_path):
            os.remove(temp_template_path)

def ocr_from_screen_area(x1, y1, x2, y2, log_file_path=None):
    params = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    try:
        region = (x1, y1, x2 - x1, y2 - y1)
        screenshot = pyautogui.screenshot(region=region)
        text = pytesseract.image_to_string(screenshot)
        result = text.strip()
        _log_action(log_file_path, "ocr_from_screen_area", params, "success", result)
        return result
    except Exception as e:
        result = f"Error during OCR: {e}"
        _log_action(log_file_path, "ocr_from_screen_area", params, "error", result)
        return result

def type_text(text, interval=0.1, log_file_path=None):
    params = {"text": text, "interval": interval}
    try:
        pyautogui.typewrite(text, interval=interval)
        result = f"Typed text: {text}"
        _log_action(log_file_path, "type_text", params, "success", result)
        return result
    except Exception as e:
        result = f"Error typing text: {e}"
        _log_action(log_file_path, "type_text", params, "error", result)
        return result

def paste_text(text, log_file_path=None):
    """
    通过剪贴板直接粘贴文字，避免输入法问题
    """
    params = {"text": text}
    try:
        # 导入剪贴板模块
        import pyperclip
        
        # 保存当前剪贴板内容
        original_clipboard = ""
        try:
            original_clipboard = pyperclip.paste()
        except:
            pass
        
        # 将文字放入剪贴板
        pyperclip.copy(text)
        
        # 执行粘贴操作 (Ctrl+V)
        pyautogui.hotkey('ctrl', 'v')
        
        # 恢复原剪贴板内容
        try:
            if original_clipboard:
                pyperclip.copy(original_clipboard)
        except:
            pass
        
        result = f"Pasted text: {text}"
        _log_action(log_file_path, "paste_text", params, "success", result)
        return result
    except Exception as e:
        result = f"Error pasting text: {e}"
        _log_action(log_file_path, "paste_text", params, "error", result)
        return result

def press_hotkey(*keys, log_file_path=None):
    actual_keys = keys
    params = {"keys": actual_keys}
    try:
        pyautogui.hotkey(*actual_keys)
        result = f"Pressed hotkey: {'+'.join(actual_keys)}"
        _log_action(log_file_path, "press_hotkey", params, "success", result)
        return result
    except Exception as e:
        result = f"Error pressing hotkey: {e}"
        _log_action(log_file_path, "press_hotkey", params, "error", result)
        return result

# --- NEW wait FUNCTION ---
def wait(seconds, log_file_path=None):
    """Pauses execution for a specified number of seconds."""
    params = {"seconds": seconds}
    try:
        time.sleep(seconds)
        result = f"Waited for {seconds} seconds."
        _log_action(log_file_path, "wait", params, "success", result)
        return result
    except Exception as e:
        result = f"Error during wait: {e}"
        _log_action(log_file_path, "wait", params, "error", result)
        return result

def sleep(seconds, log_file_path=None):
    """Pauses execution for a specified number of seconds (alias for wait)."""
    return wait(seconds, log_file_path)
