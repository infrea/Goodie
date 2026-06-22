from setuptools import setup, find_packages

setup(
    name="goodie-ai-assistant",
    version="1.0.0",
    description="GOODIE AI Assistant - Desktop companion powered by Qwen3 4B",
    author="Infrea",
    url="https://github.com/infrea/Goodie",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "llama-cpp-python>=0.2.0",
        "faster-whisper>=0.10.0",
        "piper-tts>=1.2.0",
        "pyaudio>=0.2.13",
        "pydantic>=2.0",
        "httpx>=0.24.0",
        "pynput>=1.7.6",
        "pywin32>=305",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "goodie=goodie.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
)
