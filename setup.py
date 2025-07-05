from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="desktop-automation",
    version="1.0.0",
    author="Desktop Automation Team",
    author_email="your.email@example.com",
    description="智能桌面自动化框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/desktop-automation",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyautogui>=0.9.54",
        "pytesseract>=0.3.10",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
        "gui": [
            "tkinter; sys_platform != 'darwin'",
        ],
    },
    entry_points={
        "console_scripts": [
            "desktop-automation=desktop_automation.cli:main",
            "automation-gui=gui.automation_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "desktop_automation": ["workflows_manifest.json", "successful_workflows/*.json"],
    },
)