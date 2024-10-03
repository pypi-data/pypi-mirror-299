import platform
import psutil
import datetime
import time
import socket
import os
import wmi
from colorama import init, Fore, Back, Style
import shutil

# Инициализация colorama
init()

def color_gradient(start_color, end_color, steps):
    r1, g1, b1 = int(start_color[1:3], 16), int(start_color[3:5], 16), int(start_color[5:7], 16)
    r2, g2, b2 = int(end_color[1:3], 16), int(end_color[3:5], 16), int(end_color[5:7], 16)
    
    for step in range(steps):
        t = step / (steps - 1)
        r = round(r1 * (1 - t) + r2 * t)
        g = round(g1 * (1 - t) + g2 * t)
        b = round(b1 * (1 - t) + b2 * t)
        yield f'\033[38;2;{r};{g};{b}m'

gnu_art = r"""
    _-`````-,           ,- '- .
  .'   .- - |          | - -.  `.
 /.'  /                     `.   \
:/   :      _...   ..._      ``   :
::   :     /._ .`:'_.._\.    ||   :
::    `._ ./  ,`  :    \ . _.''   .
`:.      /   |  -.  \-. \\_      /
  \:._ _/  .'   .@)  \@) ` `\ ,.'
     _/,--'       .- .\,-.`--`.
       ,'/''     (( \ `  )
        /'/'  \    `-'  (
         '/''  `._,-----'
          ''/'    .,---'
           ''/'      ;:
             ''/''  ''/
               ''/''/''
                 '/'/'
                  `;
"""

def progress_bar(percentage, width=20):
    filled = int(width * percentage // 100)
    bar = '█' * filled + '-' * (width - filled)
    return f'[{bar}] {percentage:.1f}%'

def get_system_info():
    c = wmi.WMI()
    cpu_info = c.Win32_Processor()[0]
    gpu_info = c.Win32_VideoController()[0]
    
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    bits = '64-bit' if platform.machine().endswith('64') else '32-bit'
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.datetime.now()
    uptime = current_time - boot_time
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    timezone = time.tzname[0]
    cpu_freq = psutil.cpu_freq()
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = memory.percent
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else 0

    return f"""Hostname: {hostname}
{'-' * len(f'Hostname: {hostname}')}
OS: {system} {release} ({version}) [{bits}]
Architecture: {machine}
IP Address: {ip_address}
Timezone: {timezone}
CPU: {cpu_info.Name}
CPU Cores: {psutil.cpu_count(logical=False)}
CPU Threads: {psutil.cpu_count(logical=True)}
CPU Frequency: {cpu_freq.current:.2f} MHz
CPU Usage: {progress_bar(cpu_usage)}
GPU: {gpu_info.Name}
Memory: {progress_bar(memory_usage)}
Disk: {disk.used // (1024**3)} GB / {disk.total // (1024**3)} GB
Battery: {progress_bar(battery_percent)}
Boot Time: {boot_time.strftime("%Y-%m-%d %H:%M:%S")}
Uptime: {str(uptime).split('.')[0]}
User: {os.getlogin()}"""

def main():
    terminal_width = shutil.get_terminal_size().columns
    gnu_lines = gnu_art.split('\n')
    info_lines = get_system_info().split('\n')
    max_art_width = max(len(line) for line in gnu_lines)
    max_info_width = max(len(line) for line in info_lines)

    total_width = max_art_width + max_info_width + 4  # 4 for spacing
    left_padding = (terminal_width - total_width) // 2
    
    total_lines = max(len(gnu_lines), len(info_lines))
    color_steps = 1000
    colors = list(color_gradient("#FF0000", "#0000FF", color_steps))

    try:
        print("\033[?25l", end="")  # Скрыть курсор
        print("\033[2J", end="")    # Очистить экран

        color_offset = 0
        while True:
            print("\033[H", end="")  # Переместить курсор в начало
            
            for i in range(total_lines):
                gnu_line = gnu_lines[i] if i < len(gnu_lines) else ''
                info_line = info_lines[i] if i < len(info_lines) else ''
                color_index = (color_offset + i) % color_steps
                color = colors[color_index]
                print(f"{' ' * left_padding}{color}{gnu_line:<{max_art_width}}    {info_line}\033[0m")
            
            color_offset = (color_offset + 1) % color_steps
            time.sleep(0.01)  # Уменьшим задержку для более плавного эффекта
            
            # Обновляем информацию каждые 100 итераций (примерно раз в секунду)
            if color_offset % 100 == 0:
                info_lines = get_system_info().split('\n')

    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        print("\033[?25h", end="")  # Показать курсор
        print("\nПрограмма завершена.")

if __name__ == "__main__":
    main()