import ctypes
import sys
import platform
import os
import subprocess
import shutil

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

def restart_anydesk():
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'AnyDesk.exe'], 
                      capture_output=True, shell=True)
    except Exception as e:
        pass
    
    try:
        potential_paths = [
            r'C:\ProgramData\AnyDesk',
            r'C:\ProgramData (x86)\AnyDesk'
        ]
        
        target_path = None
        for path in potential_paths:
            if os.path.exists(path):
                target_path = path
                break
        
        if target_path:
            for filename in os.listdir(target_path):
                file_path = os.path.join(target_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    continue
            
            return True, f"AnyDesk перезапущен. Данные очищены в: {target_path}"
        else:
            error_msg = "Папка AnyDesk не найдена по стандартным путям:\n"
            error_msg += "\n".join(potential_paths)
            return False, error_msg
            
    except Exception as e:
        return False, f"Ошибка при очистке: {str(e)}"