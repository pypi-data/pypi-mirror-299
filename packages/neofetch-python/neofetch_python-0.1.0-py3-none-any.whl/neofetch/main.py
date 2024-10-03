import platform
import psutil
import datetime
import time
import socket
import os
import wmi
from colorama import init, Fore, Back, Style
import math

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

def get_system_info():
    c = wmi.WMI()
    cpu_info = c.Win32_Processor()[0]
    gpu_info = c.Win32_VideoController()[0]
    
    system = platform.system()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.datetime.now()
    uptime = current_time - boot_time
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    timezone = time.tzname[0]
    cpu_freq = psutil.cpu_freq()

    return f"""OS: {system} {release} ({version})
Architecture: {machine}
Hostname: {hostname}
IP Address: {ip_address}
Timezone: {timezone}

CPU: {cpu_info.Name}
CPU Cores: {psutil.cpu_count(logical=False)}
CPU Threads: {psutil.cpu_count(logical=True)}
CPU Frequency: {cpu_freq.current:.2f} MHz

GPU: {gpu_info.Name}

RAM: {memory.total // (1024**3)} GB Total
     {memory.used // (1024**3)} GB Used
     {memory.free // (1024**3)} GB Free

Disk: {disk.total // (1024**3)} GB Total
      {disk.used // (1024**3)} GB Used
      {disk.free // (1024**3)} GB Free

Boot Time: {boot_time.strftime("%Y-%m-%d %H:%M:%S")}
Current Time: {current_time.strftime("%Y-%m-%d %H:%M:%S")}
Uptime: {str(uptime).split('.')[0]}

User: {os.getlogin()}"""

def main():
    gnu_lines = gnu_art.split('\n')
    info_lines = get_system_info().split('\n')
    max_width = max(len(line) for line in gnu_lines)

    total_lines = max(len(gnu_lines), len(info_lines))
    color_steps = 1000  # Увеличим количество шагов для более плавного перехода
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
                print(f"{color}{gnu_line:<{max_width}}    {info_line}\033[0m")
            
            color_offset = (color_offset + 1) % color_steps
            time.sleep(0.01)  # Уменьшим задержку для более плавного эффекта
    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        print("\033[?25h", end="")  # Показать курсор
        print("\nПрограмма завершена.")

if __name__ == "__main__":
    main()