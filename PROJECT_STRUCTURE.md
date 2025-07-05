# 项目结构说明

## 当前项目结构

```
desktop-automation/
├── 📁 src/                          # 源代码目录
│   └── 📁 desktop_automation/        # 主包
│       ├── 📄 __init__.py           # 包初始化文件
│       ├── 📄 core.py               # 核心自动化功能 ⭐
│       ├── 📄 cli.py                # 命令行接口
│       ├── 📄 workflows_manifest.json # 工作流注册表
│       └── 📁 successful_workflows/  # 工作流库
│           ├── 📄 send_wechat_parameterized.json ⭐
│           ├── 📄 save_notepad_test.json
│           └── 📄 smart_notepad_test.json
│
├── 📄 send_wechat.py                # 微信消息发送工具 ⭐
│
├── 📁 scripts/                      # 实用脚本
│   ├── 📄 gemini.bat               # Gemini启动脚本
│   └── 📄 install_deps.bat         # 依赖安装脚本
│
├── 📁 tests/                        # 测试文件
│   ├── 📄 __init__.py
│   └── 📄 test_core.py
│
├── 📁 docs/                         # 文档目录
│   └── 📄 CLAUDE.md                # Claude Code开发文档
│
├── 📁 logs/                         # 操作日志目录
│   └── 📁 temp/                     # 临时文件
│
├── 📄 README.md                     # 项目说明
├── 📄 requirements.txt              # Python依赖
├── 📄 setup.py                     # 安装配置
└── 📄 PROJECT_STRUCTURE.md         # 本文件
```

## 核心文件说明

### 🌟 主要功能文件

| 文件 | 说明 | 重要性 |
|------|------|--------|
| `send_wechat.py` | **一键微信消息发送工具** - 核心功能 | ⭐⭐⭐ |
| `src/desktop_automation/core.py` | 核心自动化引擎，智能视觉系统 | ⭐⭐⭐ |
| `src/desktop_automation/cli.py` | 命令行接口，工作流执行器 | ⭐⭐ |
| `src/desktop_automation/successful_workflows/send_wechat_parameterized.json` | 参数化微信工作流定义 | ⭐⭐ |

### 📋 配置文件

| 文件 | 说明 |
|------|------|
| `src/desktop_automation/workflows_manifest.json` | 工作流注册表 |
| `requirements.txt` | Python依赖列表 |
| `docs/CLAUDE.md` | 开发指导文档 |

## 使用方式

### 🚀 主要使用方式 (推荐)

```bash
# 发送微信消息 - 最简单的使用方式
python send_wechat.py "联系人名字" "消息内容"

# 示例
python send_wechat.py "张三" "你好，这是自动发送的消息"
```

### 🛠️ 高级使用方式

```bash
# 使用CLI执行工作流
python -m src.desktop_automation.cli execute_workflow --name send_wechat_parameterized --params '{"contact_name": "张三", "message_content": "消息内容"}'

# 智能操作命令
python -m src.desktop_automation.cli smart_click_text --target_text "确定"
python -m src.desktop_automation.cli analyze_screen_state
```

### 🔧 开发模式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/

# 查看帮助
python -m src.desktop_automation.cli --help
```

## 技术架构

### 🧠 核心功能模块

**智能视觉系统** (core.py)
- `analyze_screen_state()` - OCR屏幕分析
- `smart_click_text()` - 基于文字的智能点击
- `find_text_on_screen()` - 文字位置检测
- `wait_for_text_appear()` - 智能等待机制

**自动化引擎** (core.py)
- `paste_text()` - 剪贴板文字输入 (解决输入法问题)
- `press_hotkey()` - 快捷键操作
- `sleep()` - 精确延迟控制
- `take_screenshot()` - 屏幕截图

**工作流系统** (cli.py + workflows)
- JSON格式工作流定义
- `{{parameter}}` 模板参数替换
- 稳定的步骤间延迟控制

### 🎯 设计亮点

- **简化接口** - `send_wechat.py` 提供最简单的使用方式
- **跨环境支持** - WSL环境控制Windows应用
- **OCR智能** - 基于内容而非坐标的操作
- **稳定性** - 通过延迟控制确保UI响应
- **参数化** - 灵活的模板系统

## 项目演进

### ✅ 已完成
- 智能视觉识别系统
- 参数化工作流引擎  
- 跨环境自动化桥接
- 稳定的微信消息发送
- 简化的CLI工具

### 🗑️ 已移除
- GUI界面 (简化为CLI专用)
- 多余的测试文件
- 过时的工作流定义
- 调试用临时文件

这个项目现在专注于可靠的CLI驱动自动化，特别是微信消息发送功能。