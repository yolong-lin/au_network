import warnings
import colorama
import requests
from bs4 import BeautifulSoup
import pandas as pd
import socket
import os

# Get Host IP
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

warnings.filterwarnings("ignore")
colorama.init(autoreset=True)

student_id = input('StudentID: ')
password   = input('Password : ')

while True:
    os.system("cls")

    res = requests.post("https://nsp.asia.edu.tw/register/activate.php", data= {
        "action": "register",
        "zh_tw": 1,
        "student_id": student_id,
        "mpwd": password,
    }, verify= False)
    soup = BeautifulSoup(res.text, 'lxml')

    tables = pd.read_html(str(soup))
    df = tables[1]
    df = df[df[1] == get_host_ip()]
    df.reset_index(drop=True, inplace = True)
    print("流入量:   " + df.loc[0,3] + "\t\t流出量:   " + df.loc[0,4])
    print("日流入量: " + df.loc[0,6] + "\t\t日流出量: " + df.loc[0,7])
    print("預用量:   " + df.loc[0,8] + "\t\t日總量:   " + df.loc[0,9])

    total_traffic = int(df.loc[0,5][:-1])
    if total_traffic < 2000:
        print("總量:     " + colorama.Fore.GREEN + df.loc[0,5])
    elif total_traffic < 3000:
        print("總量:     " + colorama.Fore.YELLOW + df.loc[0,5])
    elif total_traffic < 4000:
        print("總量:     " + colorama.Fore.MAGENTA + df.loc[0,5])
    else:
        print("總量:     " + colorama.Fore.RED + df.loc[0,5])

    print(df.loc[0,10])

    not_exit = input("")
    if not_exit:
        break
