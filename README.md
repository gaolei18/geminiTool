# 桌面自动化框架 (Desktop Automation Framework)

一个基于视觉识别的智能桌面自动化框架，专注于可靠的CLI驱动自动化操作。

## 核心特性

- 🔍 **智能视觉识别** - OCR技术解决"盲目操作"问题
- 🎯 **精准文字定位** - 基于内容而非坐标的元素定位  
- ⚡ **一键消息发送** - 简单命令行工具发送微信消息
- 🔧 **参数化工作流** - 灵活的模板参数系统
- 🌉 **跨环境支持** - WSL环境控制Windows应用
- ⏱️ **稳定延迟控制** - 确保UI响应的时序管理

## 快速开始

### 环境要求

- Python 3.7+
- Windows系统（支持WSL环境）
- Tesseract OCR

### 安装

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Tesseract OCR (Windows)
# 下载: https://github.com/UB-Mannheim/tesseract/wiki
# 安装到: C:\Program Files\Tesseract-OCR\
```

### 主要功能 - 微信消息发送

这是框架的核心功能，支持一键发送微信消息：

```bash
# 基本用法
python send_wechat.py "联系人名字" "消息内容"

# 实际示例
python send_wechat.py "张三" "你好，这是自动发送的消息"
python send_wechat.py "文件传输助手" "测试消息发送成功"
python send_wechat.py "李四" "代码如诗韵律美，自动化程序展神威"
```

### 高级用法 - CLI命令

```bash
# 执行参数化工作流
python -m src.desktop_automation.cli execute_workflow --name send_wechat_parameterized --params '{"contact_name": "张三", "message_content": "消息内容"}'

# 屏幕分析和智能操作
python -m src.desktop_automation.cli analyze_screen_state
python -m src.desktop_automation.cli smart_click_text --target_text "确定"
python -m src.desktop_automation.cli wait_for_text_appear --target_text "保存成功"
```

## 项目结构

```
desktop-automation/
├── src/desktop_automation/    # 核心代码
│   ├── core.py               # 核心自动化功能
│   ├── cli.py                # 命令行接口
│   ├── workflows_manifest.json # 工作流注册表
│   └── successful_workflows/ # 验证过的工作流
├── send_wechat.py            # 微信消息发送工具 ⭐
├── scripts/                  # 实用脚本
├── docs/CLAUDE.md           # 开发文档
├── requirements.txt
└── README.md
```

## 技术架构

### 核心功能模块

**智能视觉系统**
- `analyze_screen_state()` - OCR屏幕内容分析
- `smart_click_text()` - 基于文字的智能点击
- `find_text_on_screen()` - 文字位置检测
- `wait_for_text_appear()` - 智能等待机制

**自动化引擎**  
- `paste_text()` - 剪贴板文字输入（避免输入法问题）
- `press_hotkey()` - 快捷键操作
- `sleep()` - 精确延迟控制
- `take_screenshot()` - 屏幕截图

**工作流系统**
- JSON格式的工作流定义
- `{{parameter}}` 模板参数替换
- 稳定的步骤间延迟控制

### 技术亮点

- **跨环境桥接** - WSL环境通过`cmd.exe`控制Windows应用
- **OCR优化** - 中英混合识别，PSM6模式最佳效果  
- **输入法兼容** - 使用剪贴板避免中文输入问题
- **延迟管理** - 每步操作间1-2秒延迟确保UI响应

## 使用案例

### 实际应用示例

```bash
# 发送工作报告
python send_wechat.py "项目经理" "今日工作完成，自动化框架测试通过"

# 发送诗歌
python send_wechat.py "朋友" "代码如诗韵律美，自动化程序展神威"

# 批量通知
python send_wechat.py "团队群" "会议提醒：明天下午2点开会"
```

### 成功验证

✅ **跨环境运行** - WSL环境成功控制Windows微信  
✅ **中文支持** - 完美处理中文联系人和消息内容  
✅ **稳定操作** - 通过延迟控制解决UI响应问题  
✅ **参数化** - 无需修改代码即可发送不同内容  

## 开发信息

- **核心语言**: Python 3.7+
- **主要依赖**: pyautogui, pytesseract, PIL, pyperclip
- **测试环境**: Windows 10/11, WSL2
- **许可证**: MIT