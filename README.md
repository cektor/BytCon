<a href="#">
    <img src="https://raw.githubusercontent.com/pedromxavier/flag-badges/main/badges/TR.svg" alt="made in TR">
</a>

# BytCon
BytCon (Byte Converter), between MB, GB and TB units is a tool that allows you to make easy conversions. Cross Platform

<h1 align="center">BytCon Logo</h1>

<p align="center">
  <img src="bytconlo.png" alt="BytCon Logo" width="150" height="150">
</p>

----------------------------------

# Linux Screenshot
![Linux(pardus)](screenshot/bytcon_linux.png)  

# Windows Screenshot
![Windows(11)](screenshot/bytcon_windows.png) 

--------------------
Install Git Clone and Python3

Github Package Must Be Installed On Your Device..

git
```bash
sudo apt install git -y
```

Python3
```bash
sudo apt install python3 -y 

```

pip
```bash
sudo apt install python3-pip

```

# Required Libraries

PyQt5
```bash
pip install PyQt5
```
PyQt5-sip
```bash
pip install PyQt5 PyQt5-sip
```

PyQt5-tools
```bash
pip install PyQt5-tools
```

Required Libraries for Debian/Ubuntu
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install qttools5-dev-tools
```

----------------------------------


# Installation
Install BytCon

```bash
sudo git clone https://github.com/cektor/BytCon.git
```
```bash
cd BytCon
```

```bash
python3 bytcon.py

```

# To compile

NOTE: For Compilation Process pyinstaller must be installed. To Install If Not Installed.

pip install pyinstaller 

Linux Terminal 
```bash
pytohn3 -m pyinstaller --onefile --windowed bytcon.py
```

Windows VSCode Terminal 
```bash
pyinstaller --onefile --noconsole bytcon.py
```

MacOS VSCode Terminal 
```bash
pyinstaller --onefile --noconsole bytcon.py
```

# To install directly on Windows or Linux


Linux (based debian) Terminal: Linux (debian based distributions) To install directly from Terminal.
```bash
wget -O Setup_Linux64.deb https://github.com/cektor/BytCon/releases/download/1.00/Setup_Linux64.deb && sudo apt install ./Setup_Linux64.deb && sudo apt-get install -f -y
```

Windows Installer CMD (PowerShell): To Install from Windows CMD with Direct Connection.
```bash
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cektor/BytCon/releases/download/1.00/Setup_Win64.exe' -OutFile 'Setup_Win64.exe'" && start /wait Setup_Win64.exe
```

Release Page: https://github.com/cektor/BytCon/releases/tag/1.00

