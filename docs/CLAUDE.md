# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

This is a desktop automation framework designed for intelligent, vision-based automation. The system has evolved from basic automation to a sophisticated CLI-driven tool that can "see" and operate reliably on desktop applications.

## Core Components

1. **Core automation library** (`src/desktop_automation/core.py`) - Provides intelligent automation with OCR capabilities
2. **CLI interface** (`src/desktop_automation/cli.py`) - Command-line interface for executing actions and workflows
3. **WeChat automation tool** (`send_wechat.py`) - Simple command-line tool for sending WeChat messages

## Architecture

### Core Philosophy
The project solves the "blind operation" problem by combining:
- **Vision** - OCR-based screen analysis and text recognition
- **Intelligence** - Smart element location based on content, not coordinates
- **Reliability** - Operation verification and retry mechanisms
- **Parameterization** - Flexible workflow execution with custom parameters

### Key Features
- ✅ Intelligent OCR-based automation (no hardcoded coordinates)
- ✅ Stable workflow execution with proper delays
- ✅ Parameterized workflows for flexibility
- ✅ Cross-environment support (WSL → Windows automation)
- ✅ Simple CLI interface for easy use

## Main Usage

### WeChat Message Sending (Primary Feature)
```bash
# Send message to any contact
python send_wechat.py "联系人名字" "消息内容"

# Examples
python send_wechat.py "张三" "你好，这是自动发送的消息"
python send_wechat.py "文件传输助手" "测试消息发送成功"
```

### CLI Commands
```bash
# Execute parameterized WeChat workflow
python -m src.desktop_automation.cli execute_workflow --name send_wechat_parameterized --params '{"contact_name": "张三", "message_content": "消息内容"}'

# Take screenshot
python -m src.desktop_automation.cli take_screenshot --file_path screenshot.png

# Smart text-based operations
python -m src.desktop_automation.cli smart_click_text --target_text "确定"
python -m src.desktop_automation.cli wait_for_text_appear --target_text "保存成功"
```

## Workflow System

### Current Workflows
- `send_wechat_parameterized` - Main WeChat messaging workflow with delays and parameters
- `save_notepad_test` - Notepad automation demo
- `smart_notepad_test` - Intelligent Notepad workflow using OCR

### Workflow Features
- JSON-based workflow definitions
- Parameter substitution using `{{parameter_name}}` syntax
- Built-in delays for stable UI transitions
- Clipboard-based text input to avoid input method issues

## Technical Details

### Core Functions (src/desktop_automation/core.py)
- `analyze_screen_state()` - OCR analysis of screen content
- `smart_click_text()` - Click on text elements
- `paste_text()` - Clipboard-based text input
- `wait_for_text_appear()` - Wait for UI elements
- `verify_operation_result()` - Operation verification
- `sleep()` - Delay control for stable operations

### Cross-Environment Bridge
The system successfully operates from WSL environment to control Windows applications using:
- `cmd.exe /c` bridge commands
- Clipboard-based text input (pyperclip)
- OCR for visual feedback

### Dependencies
- `pyautogui>=0.9.54` - GUI automation
- `pytesseract>=0.3.10` - OCR functionality
- `Pillow>=8.0.0` - Image processing
- `pyperclip>=1.8.2` - Clipboard operations

## Project Structure
```
desktop-automation/
├── src/desktop_automation/    # Core automation code
│   ├── core.py               # Main automation functions
│   ├── cli.py                # Command-line interface
│   ├── workflows_manifest.json
│   └── successful_workflows/ # Proven workflow definitions
├── send_wechat.py           # Simple WeChat messaging tool
├── scripts/                 # Utility scripts
├── docs/CLAUDE.md           # This file
├── requirements.txt
└── README.md
```

## Development Guidelines

### When Adding New Features
1. Use OCR and text-based operations instead of coordinates
2. Add proper delays between operations for stability
3. Implement parameter substitution for flexibility
4. Test in cross-environment scenarios (WSL → Windows)

### Best Practices
- Always use `paste_text()` instead of `type_text()` for Chinese text
- Add 1-2 second delays between UI operations
- Use `smart_click_text()` for reliable element interaction
- Implement operation verification where possible

### Success Criteria
The framework has successfully achieved:
- Reliable WeChat message automation
- Cross-environment operation (WSL → Windows)
- Parameterized workflow execution
- Stable operation with proper delay management
- Simple CLI interface for end users