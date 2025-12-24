import os

FREQUENT_SITES = {
    "anticheat.ac": "Океан",
    "funtime.su": "Сайт фантайм",
    "www.voidtools.com": "еверифинг",
    "github.com": "гбитхаб (JournalTrace\\CachedProgramsList)",
    "www.nirsoft.net": "нирсофт (PreviousFilesRecovery\\ExecutedProgramsList\\USB-Deview\\USB-DriveLog\\LastActivityView\\OpenSaveFilesView)",
    "privazer.com": "привазер (ShellBack)",
    "systeminformer.sourceforge.io": "SystemInformer\\ProcessHacker",
    "back.map4yk.ru": "сайт подкачки автопроверки марчука"
}

APPDATA_DB = os.path.join(os.getenv('APPDATA'), "sys_net_conf.txt")
DEFAULT_PATH = os.path.expanduser("~")