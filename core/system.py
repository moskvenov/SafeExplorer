import ctypes
import sys
import platform
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def get_hosts_path():
    return r"C:\Windows\System32\drivers\etc\hosts" if platform.system() == "Windows" else "/etc/hosts"

def get_file_properties(path):
    if not os.path.exists(path):
        return {}
    
    try:
        stats = os.stat(path)
        return {
            'mtime': stats.st_mtime,
            'size': stats.st_size,
            'is_dir': os.path.isdir(path)
        }
    except:
        return {}