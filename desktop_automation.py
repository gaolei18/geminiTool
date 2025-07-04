
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
