#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║   🥷 WEBHOOK-HUNTER — Shadow Username Hunter               ║
║   Hunt Rare Usernames + Send to Webhook                    ║
║   Discord: in7j  |  Python 3 Only                          ║
║   ⚠️ Educational Purpose Only                              ║
║   ═════════════════════════════════════════════════════════ ║
║   © 2026 NINJA ™ — All Rights Reserved                    ║
╚═══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import random
import string
import threading
import json
import urllib.request
import urllib.error
from datetime import datetime

# ================================================================
#  Python Version Check
# ================================================================
if sys.version_info < (3, 6):
    print("\033[91m[!] Error: Python 3.6 or higher required\033[0m")
    sys.exit(1)

# ================================================================
#  NINJA Signature
# ================================================================
VERSION = "WEBHOOK-HUNTER-v1.0"
AUTHOR = "in7j"
CONTACT = "DISCORD: in7j"
COPYRIGHT = "© 2026 NINJA ™ — All Rights Reserved"

# ================================================================
#  Colors
# ================================================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    DIM = '\033[2m'
    BOLD = '\033[1m'

def col(color, text):
    return f"{color}{text}{Colors.RESET}"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ================================================================
#  Banner
# ================================================================
def print_banner():
    clear_screen()
    banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║{Colors.YELLOW}   ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗  {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}   ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗ {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}   ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝ {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}   ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗ {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}   ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║ {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   🥷 WEBHOOK-HUNTER  v1.0                           {Colors.RED}║
{Colors.RED}║{Colors.GREEN}   Hunt Rare Usernames + Send to Webhook            {Colors.RED}║
{Colors.RED}║{Colors.RED}   ⚠️  Educational Purpose Only                        {Colors.RED}║
{Colors.RED}║{Colors.DIM}   {COPYRIGHT}                                          {Colors.RED}║
{Colors.RED}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
    """
    print(banner)

# ================================================================
#  Supported Platforms
# ================================================================
PLATFORMS = {
    "instagram": {
        "url": "https://www.instagram.com/{}/",
        "check": lambda status, body: status == 404 or "user_not_found" in body
    },
    "twitter": {
        "url": "https://twitter.com/{}/",
        "check": lambda status, body: status == 404 or "user-not-found" in body.lower()
    },
    "github": {
        "url": "https://github.com/{}",
        "check": lambda status, body: status == 404
    },
    "tiktok": {
        "url": "https://www.tiktok.com/@{}",
        "check": lambda status, body: status == 404 or "Couldn’t find" in body
    },
    "snapchat": {
        "url": "https://www.snapchat.com/add/{}",
        "check": lambda status, body: status == 404
    },
    "reddit": {
        "url": "https://www.reddit.com/user/{}/",
        "check": lambda status, body: status == 404
    },
    "pinterest": {
        "url": "https://www.pinterest.com/{}/",
        "check": lambda status, body: status == 404 or "Sorry! We couldn" in body
    },
    "twitch": {
        "url": "https://www.twitch.tv/{}",
        "check": lambda status, body: status == 404 or "isNotFound" in body
    },
    "youtube": {
        "url": "https://www.youtube.com/@{}",
        "check": lambda status, body: status == 404 or "channelId" not in body
    },
    "telegram": {
        "url": "https://t.me/{}",
        "check": lambda status, body: "tgme_page_extra" not in body and "If you have Telegram" not in body
    }
}

# ================================================================
#  Username Generator
# ================================================================
def generate_username(length, pattern=None):
    chars = string.ascii_lowercase + string.digits
    if pattern == "letters":
        chars = string.ascii_lowercase
    elif pattern == "mix":
        chars = string.ascii_lowercase + string.digits + "._"
    
    first_chars = string.ascii_lowercase + string.digits
    username = random.choice([c for c in chars if c in first_chars])
    
    for _ in range(length - 1):
        ch = random.choice(chars)
        if ch in "._" and username[-1] in "._":
            ch = random.choice(string.ascii_lowercase + string.digits)
        username += ch
    
    if username[-1] in "._":
        username = username[:-1] + random.choice(string.ascii_lowercase + string.digits)
    
    return username

def generate_batch(length, count, pattern=None):
    seen = set()
    result = []
    attempts = 0
    max_attempts = count * 50
    
    while len(result) < count and attempts < max_attempts:
        attempts += 1
        u = generate_username(length, pattern)
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result

# ================================================================
#  Username Checker
# ================================================================
def check_username(username, platform):
    config = PLATFORMS.get(platform)
    if not config:
        return None
    
    url = config["url"].format(username)
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            return config["check"](status, body)
    except urllib.error.HTTPError as e:
        return config["check"](e.code, "")
    except:
        return None

# ================================================================
#  Webhook Sender
# ================================================================
def send_to_webhook(webhook_url, username, platform):
    """Send discovered username to Webhook"""
    try:
        embed = {
            "embeds": [{
                "title": "🎯 Rare Username Found!",
                "color": 0x00ff00,
                "fields": [
                    {
                        "name": "👤 Username",
                        "value": f"`@{username}`",
                        "inline": True
                    },
                    {
                        "name": "🌐 Platform",
                        "value": platform.capitalize(),
                        "inline": True
                    },
                    {
                        "name": "📅 Date",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": False
                    },
                    {
                        "name": "🔗 Link",
                        "value": f"[Click Here]({PLATFORMS[platform]['url'].format(username)})",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"{COPYRIGHT} | {AUTHOR}"
                }
            }]
        }
        
        data = json.dumps(embed).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 204 or response.status == 200
            
    except Exception as e:
        print(f"{col(Colors.RED, f'[!] Failed to send to Webhook: {e}')}")
        return False

# ================================================================
#  Loading Animation
# ================================================================
def loading_animation(stop_event, text="Searching"):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{col(Colors.CYAN, chars[i % len(chars)])} {col(Colors.WHITE, text)}...   ")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ================================================================
#  Main Hunting Function
# ================================================================
def hunt_with_webhook(length, count, platforms, webhook_url, pattern=None):
    """Hunt for usernames and send to Webhook"""
    results = {p: [] for p in platforms}
    total_found = 0
    webhook_sent = 0
    
    print(f"\n{col(Colors.BLUE, '[*]')} Generating {count} usernames with length {length}...")
    usernames = generate_batch(length, count, pattern)
    print(f"{col(Colors.GREEN, '[+]')} Generated {len(usernames)} usernames\n")
    
    total_checks = len(usernames) * len(platforms)
    checked = 0
    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(
        target=loading_animation,
        args=(stop_spinner, f"Checking 0/{total_checks}")
    )
    spinner_thread.daemon = True
    spinner_thread.start()
    
    for username in usernames:
        for platform in platforms:
            checked += 1
            if checked % 5 == 0:
                stop_spinner.set()
                time.sleep(0.1)
                stop_spinner = threading.Event()
                spinner_thread = threading.Thread(
                    target=loading_animation,
                    args=(stop_spinner, f"Checking {checked}/{total_checks}")
                )
                spinner_thread.daemon = True
                spinner_thread.start()
            
            available = check_username(username, platform)
            if available is True:
                results[platform].append(username)
                total_found += 1
                
                # Display on screen
                sys.stdout.write(
                    f"\r{col(Colors.GREEN, '[+]')} {col(Colors.WHITE, username)} → "
                    f"{col(Colors.CYAN, platform)} AVAILABLE!          \n"
                )
                sys.stdout.flush()
                
                # Send to Webhook
                if webhook_url:
                    if send_to_webhook(webhook_url, username, platform):
                        webhook_sent += 1
                        print(f"{col(Colors.GREEN, '  📤')} Sent @{username} to Webhook")
            
            time.sleep(0.05)
    
    stop_spinner.set()
    time.sleep(0.2)
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()
    
    return results, total_found, webhook_sent

# ================================================================
#  Display Results
# ================================================================
def display_results(results, total_found, webhook_sent):
    """Display results in a fancy way"""
    print(f"\n{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  📊 WEBHOOK-HUNTER Report                          {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  ──────────────────────────────────────────────    {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  ✅ Found: {total_found} usernames                     {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  📤 Sent to Webhook: {webhook_sent}                   {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    for platform, usernames in results.items():
        if usernames:
            print(f"{col(Colors.CYAN, f'► {platform.upper()}')} — {len(usernames)} usernames")
            for i, u in enumerate(usernames[:20], 1):
                print(f"    {i:2}. {col(Colors.GREEN, u)}")
            if len(usernames) > 20:
                print(f"    ... and {len(usernames)-20} more")
            print()
    
    # Save JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"webhook_hunt_{timestamp}.json"
    try:
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump({
                "results": results,
                "total": total_found,
                "webhook_sent": webhook_sent,
                "date": timestamp,
                "version": VERSION,
                "author": AUTHOR
            }, f, indent=2, ensure_ascii=False)
        print(f"{col(Colors.GREEN, '[+]')} Saved JSON to: {col(Colors.WHITE, json_file)}")
    except Exception as e:
        print(f"{col(Colors.RED, f'[!] Failed to save JSON: {e}')}")
    
    # Save TXT
    txt_file = f"webhook_usernames_{timestamp}.txt"
    try:
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"  {VERSION}\n")
            f.write(f"  {COPYRIGHT}\n")
            f.write(f"  Author: {AUTHOR} ({CONTACT})\n")
            f.write(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"  Sent to Webhook: {webhook_sent}\n")
            f.write("=" * 60 + "\n\n")
            for platform, usernames in results.items():
                if usernames:
                    f.write(f"[{platform.upper()}]\n")
                    for u in usernames:
                        f.write(f"  @{u}\n")
                    f.write("\n")
            f.write(f"\nTotal: {total_found} usernames\n")
        print(f"{col(Colors.GREEN, '[+]')} Saved TXT to: {col(Colors.WHITE, txt_file)}")
    except Exception as e:
        print(f"{col(Colors.RED, f'[!] Failed to save TXT: {e}')}")
    
    print(f"\n{Colors.DIM}[*] {COPYRIGHT}{Colors.RESET}")

# ================================================================
#  Main Menu
# ================================================================
def main_menu():
    """Display main menu"""
    print_banner()
    
    menu = f"""
{Colors.YELLOW}┌────────────────────────────────────────────────────────────────┐
{Colors.YELLOW}│{Colors.WHITE}  [1] 3-Letter Usernames  — Extremely Rare           {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [2] 4-Letter Usernames  — Rare                     {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [3] 5-Letter Usernames  — Moderately Rare          {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [4] 6-Letter Usernames  — Common                   {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [5] Custom Length Usernames                         {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [6] Letters Only (No Numbers or Symbols)           {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [7] Mixed (Letters + Numbers + Symbols)            {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [8] Check Single Username                           {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.RED}  [0] Exit                                            {Colors.YELLOW}│
{Colors.YELLOW}└────────────────────────────────────────────────────────────────┘{Colors.RESET}
    """
    print(menu)
    
    try:
        choice = input(f"{col(Colors.CYAN, 'ninja@webhook ~$ ')}").strip()
    except (EOFError, KeyboardInterrupt):
        return "0"
    
    # Select platforms
    print(f"\n{Colors.YELLOW}┌────────────────────────────────────────────────────────────┐")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  Select Platforms (comma separated numbers)            {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  1.Instagram  2.Twitter  3.GitHub  4.TikTok           {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  5.Snapchat   6.Reddit   7.Pinterest  8.Twitch        {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  9.YouTube    10.Telegram  (or 'all' for all)        {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    platforms_input = input(f"{col(Colors.CYAN, 'Select Platforms > ')}").strip()
    
    platform_map = {
        "1": "instagram", "2": "twitter", "3": "github", "4": "tiktok",
        "5": "snapchat", "6": "reddit", "7": "pinterest", "8": "twitch",
        "9": "youtube", "10": "telegram"
    }
    
    if platforms_input.lower() == "all":
        platforms = list(PLATFORMS.keys())
    else:
        platforms = []
        for p in platforms_input.replace(" ", "").split(","):
            if p in platform_map:
                platforms.append(platform_map[p])
        if not platforms:
            platforms = ["instagram", "twitter", "github"]
    
    try:
        count = int(input(f"{col(Colors.CYAN, 'Number of usernames to check (1-500) > ')}").strip() or "50")
        if count < 1:
            count = 50
        if count > 500:
            count = 500
    except ValueError:
        count = 50
    
    # Ask for Webhook URL
    print(f"\n{Colors.YELLOW}┌────────────────────────────────────────────────────────────┐")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  🔗 Enter Webhook URL (Discord/Telegram)            {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.DIM}  Leave empty if you don't want to send               {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    webhook_url = input(f"{col(Colors.CYAN, 'Webhook URL > ')}").strip()
    
    return choice, platforms, count, webhook_url

# ================================================================
#  Main Execution
# ================================================================
def main():
    """Main function"""
    print(f"{Colors.DIM}\n{VERSION} | {COPYRIGHT}{Colors.RESET}")
    time.sleep(0.5)
    
    while True:
        try:
            result = main_menu()
            if result == "0" or result == 0:
                print(f"\n{col(Colors.GREEN, '[+]')} Goodbye! | {VERSION}\n")
                print(f"{Colors.DIM}[*] {COPYRIGHT}{Colors.RESET}")
                break
            
            if isinstance(result, tuple):
                choice, platforms, count, webhook_url = result
            else:
                continue
            
            # Determine length and pattern
            length_map = {"1": 3, "2": 4, "3": 5, "4": 6}
            pattern = None
            
            if choice in length_map:
                length = length_map[choice]
            elif choice == "5":
                try:
                    length = int(input(f"{col(Colors.CYAN, 'Enter length (2-20) > ')}").strip() or "5")
                    if length < 2:
                        length = 2
                    if length > 20:
                        length = 20
                except ValueError:
                    length = 5
            elif choice == "6":
                length = 4
                pattern = "letters"
            elif choice == "7":
                length = 4
                pattern = "mix"
            elif choice == "8":
                username = input(f"{col(Colors.CYAN, 'Enter username to check > ')}").strip()
                if not username:
                    continue
                print(f"\n{col(Colors.BLUE, '[*]')} Checking @{username}...\n")
                for platform in platforms:
                    available = check_username(username, platform)
                    if available is True:
                        print(f"  {col(Colors.GREEN, '✅')} {platform:12} → AVAILABLE")
                        if webhook_url:
                            send_to_webhook(webhook_url, username, platform)
                    elif available is False:
                        print(f"  {col(Colors.RED, '❌')} {platform:12} → TAKEN")
                    else:
                        print(f"  {col(Colors.YELLOW, '⚠️')} {platform:12} → UNKNOWN")
                    time.sleep(0.2)
                input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to return...")
                continue
            else:
                length = 4
            
            # Start hunting
            clear_screen()
            print_banner()
            print(f"\n{col(Colors.RED, '[🔥]')} Starting hunt...")
            print(f"  Length: {length} | Count: {count} | Platforms: {len(platforms)}")
            print(f"  {', '.join(platforms[:5])}{'...' if len(platforms) > 5 else ''}")
            if webhook_url:
                print(f"  📤 Webhook: {col(Colors.GREEN, 'Enabled')}")
            else:
                print(f"  📤 Webhook: {col(Colors.RED, 'Disabled')}")
            print()
            
            start_time = time.time()
            results, total_found, webhook_sent = hunt_with_webhook(
                length, count, platforms, webhook_url, pattern
            )
            elapsed = time.time() - start_time
            
            display_results(results, total_found, webhook_sent)
            print(f"\n{Colors.DIM}[*] Time taken: {elapsed:.1f} seconds{Colors.RESET}")
            print(f"{Colors.DIM}[*] {COPYRIGHT}{Colors.RESET}")
            
            input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to return to menu...")
            
        except KeyboardInterrupt:
            print(f"\n{col(Colors.YELLOW, '[!]')} Interrupted by user")
            print(f"{Colors.DIM}[*] {COPYRIGHT}{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{col(Colors.RED, f'[!] Error: {e}')}")
            input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to continue...")

# ================================================================
#  Entry Point
# ================================================================
if __name__ == "__main__":
    main()