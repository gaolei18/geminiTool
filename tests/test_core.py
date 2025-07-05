"""
测试核心功能模块
"""
import pytest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from desktop_automation import core


class TestBasicFunctions:
    """测试基础功能"""
    
    def test_wait_function_exists(self):
        """测试wait函数是否存在"""
        assert hasattr(core, 'wait')
        
    def test_log_action_function_exists(self):
        """测试日志功能是否存在"""
        assert hasattr(core, '_log_action')
        
    def test_analyze_screen_state_function_exists(self):
        """测试屏幕分析功能是否存在"""
        assert hasattr(core, 'analyze_screen_state')
        
    def test_smart_click_text_function_exists(self):
        """测试智能点击功能是否存在"""
        assert hasattr(core, 'smart_click_text')


class TestSmartFunctions:
    """测试智能功能"""
    
    def test_find_text_on_screen_function_exists(self):
        """测试文字查找功能是否存在"""
        assert hasattr(core, 'find_text_on_screen')
        
    def test_wait_for_text_appear_function_exists(self):
        """测试条件等待功能是否存在"""
        assert hasattr(core, 'wait_for_text_appear')
        
    def test_verify_operation_result_function_exists(self):
        """测试操作验证功能是否存在"""
        assert hasattr(core, 'verify_operation_result')


if __name__ == "__main__":
    pytest.main([__file__])