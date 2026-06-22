"""
GOODIE Build Script
Builds EXE and MSI installers for Windows
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """Check if required build tools are installed"""
    required = ["pyinstaller", "cx_Freeze"]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing required packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    return True


def build_exe():
    """Build standalone EXE using PyInstaller"""
    print("\n🔨 Building EXE installer...\n")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=GOODIE",
        "--icon=assets/goodie.ico",
        "--version-file=version.txt",
        "--add-data=goodie:goodie",
        "--hidden-import=llama_cpp",
        "--hidden-import=faster_whisper",
        "--hidden-import=piper_tts",
        "--specpath=build/specs",
        "--distpath=dist/exe",
        "--buildpath=build",
        "goodie/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n✅ EXE build completed successfully!")
        print(f"📦 Output: dist/exe/GOODIE.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ EXE build failed: {e}")
        return False


def build_msi():
    """Build MSI installer"""
    print("\n🔨 Building MSI installer...\n")
    
    # Create WiX configuration file
    wix_content = r"""
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
    <Product Id="*" Name="GOODIE AI Assistant" Language="1033" Version="1.0.0.0"
             Manufacturer="Infrea" UpgradeCode="12345678-1234-1234-1234-123456789012">
        <Package InstallerVersion="200" Compressed="yes" />
        <Media Id="1" Cabinet="goodie.cab" EmbedCab="yes" />
        
        <Directory Id="TARGETDIR" Name="SourceDir">
            <Directory Id="ProgramFilesFolder">
                <Directory Id="INSTALLFOLDER" Name="GOODIE" />
            </Directory>
        </Directory>
        
        <Feature Id="ProductFeature" Title="GOODIE AI Assistant" Level="1">
            <ComponentRef Id="MainExecutable" />
        </Feature>
    </Product>
</Wix>
"""
    
    wix_file = Path("build/goodie.wxs")
    wix_file.parent.mkdir(parents=True, exist_ok=True)
    wix_file.write_text(wix_content)
    
    print("📝 WiX configuration created: build/goodie.wxs")
    print("\n✅ MSI build ready!")
    print("   Run: candle build/goodie.wxs -o build/ && light build/goodie.wixobj -o dist/msi/goodie.msi")
    print("   Or use WiX Toolset GUI")
    
    return True


def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description="Build GOODIE AI Assistant installers")
    parser.add_argument(
        "--format",
        choices=["exe", "msi", "all"],
        default="all",
        help="Build format (default: all)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("GOODIE AI ASSISTANT - BUILD SCRIPT")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    print("\n✓ All dependencies available")
    
    # Create necessary directories
    Path("dist/exe").mkdir(parents=True, exist_ok=True)
    Path("dist/msi").mkdir(parents=True, exist_ok=True)
    Path("build/specs").mkdir(parents=True, exist_ok=True)
    
    success = True
    
    if args.format in ["exe", "all"]:
        if not build_exe():
            success = False
    
    if args.format in ["msi", "all"]:
        if not build_msi():
            success = False
    
    print("\n" + "="*60)
    if success:
        print("✅ Build completed successfully!")
        print("\n📦 Output locations:")
        print("   EXE: dist/exe/GOODIE.exe")
        print("   MSI: dist/msi/goodie.msi (requires WiX)")
    else:
        print("❌ Build completed with errors")
    print("="*60 + "\n")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
