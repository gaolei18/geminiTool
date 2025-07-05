"""
Desktop Automation Framework
智能桌面自动化框架

一个基于视觉识别的桌面自动化框架，支持：
- OCR文字识别和定位
- 智能点击和操作验证
- 工作流管理和执行
- 操作日志记录
"""

__version__ = "1.0.0"
__author__ = "Desktop Automation Team"

from .core import (
    # 基础功能
    take_screenshot,
    move_and_click,
    type_text,
    press_hotkey,
    wait,
    
    # 智能视觉功能
    analyze_screen_state,
    find_text_on_screen,
    smart_click_text,
    wait_for_text_appear,
    verify_operation_result,
    
    # 日志功能
    start_task_log,
    end_task_with_verdict,
)

__all__ = [
    # 基础功能
    'take_screenshot',
    'move_and_click', 
    'type_text',
    'press_hotkey',
    'wait',
    
    # 智能功能
    'analyze_screen_state',
    'find_text_on_screen',
    'smart_click_text', 
    'wait_for_text_appear',
    'verify_operation_result',
    
    # 日志功能
    'start_task_log',
    'end_task_with_verdict',
]