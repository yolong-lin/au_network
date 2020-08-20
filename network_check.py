# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Init console
import sys
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich import box
console = Console()
error_console = Console(file=sys.stderr)
console.clear()

# Get account and password
from dotenv import load_dotenv, find_dotenv
import os
if not find_dotenv():
    student_id = Prompt.ask("Student ID")
    password   = Prompt.ask("Password", password = True)
else:
    load_dotenv()
    student_id = os.getenv('student_id')
    password   = os.getenv('password')
    if not student_id or not password:
        error_console.print("Cannot find [u]student_id[/] or [u]password[/] in .env file!!", style='bright_red')
        exit(1)

# Get Host IP
import socket
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

host_ip = get_host_ip()

# Crawl Needed
import requests
from bs4 import BeautifulSoup
import pandas as pd

console.show_cursor(False)
def fetch_traffic():
    console.clear()
    console.print()

    res = requests.post("https://nsp.asia.edu.tw/register/activate.php", verify= False, data= {
        "action": "register",
        "zh_tw": 1,
        "student_id": student_id,
        "mpwd": password,
    })
    soup = BeautifulSoup(res.text, 'lxml')

    dfs = pd.read_html(str(soup))
    df = dfs[1]
    df = df[df[1] == host_ip]
    df.reset_index(drop=True, inplace = True)

    location          = df.loc[0,0]
    mac               = df.loc[0,2]
    traffic_status    = df.loc[0,10]

    traffic_data = {
        "traffic_in"        : df.loc[0,3],
        "traffic_out"       : df.loc[0,4],
        "preuse_traffic"    : df.loc[0,8],
        "day_traffic_in"    : df.loc[0,6],
        "day_traffic_out"   : df.loc[0,7],
        "day_traffic_total" : df.loc[0,9],
        "traffic_total"     : df.loc[0,5],
    }

    table = Table(header_style="bold magenta")
    table.title = "[#ff9100]%s[/] | [#ff9100]%s[/] | [#ff9100]%s[/]" % (location, host_ip, mac)
    table.caption = ":sunglasses: %s :sunglasses:" % (traffic_status)
    table.box = box.SQUARE
    table.add_column("流入量", justify="right")
    table.add_column("流出量", justify="right")
    table.add_column("預用量", justify="right")
    table.add_column("日流入量", justify="right")
    table.add_column("日流出量", justify="right")
    table.add_column("日總量", justify="right")
    table.add_column("總量", justify="right")

    table.add_row(
        *traffic_data.values()
    )
    
    console.print(table, justify="center")


while True:
    try:
        fetch_traffic()
        kb = Prompt.get_input(console, '', password=True)
    except KeyboardInterrupt:
        console.show_cursor(True)
        exit(0)

