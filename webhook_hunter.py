#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║   🥷 WEBHOOK-HUNTER XTREME — ULTIMATE USERNAME HUNTER     ║
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
VERSION = "WEBHOOK-HUNTER-XTREME-v2.0"
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
{Colors.RED}║{Colors.CYAN}   🥷 WEBHOOK-HUNTER XTREME  v2.0                   {Colors.RED}║
{Colors.RED}║{Colors.GREEN}   ULTIMATE Username Hunter + Discord             {Colors.RED}║
{Colors.RED}║{Colors.RED}   ⚠️  Educational Purpose Only                    {Colors.RED}║
{Colors.RED}║{Colors.DIM}   {COPYRIGHT}                                      {Colors.RED}║
{Colors.RED}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
    """
    print(banner)

# ================================================================
#  SMART RANDOM USER AGENTS
# ================================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
]

# ================================================================
#  DISCORD USERNAME VALIDATION
# ================================================================
DISCORD_MIN_LENGTH = 2
DISCORD_MAX_LENGTH = 32
DISCORD_ALLOWED = string.ascii_lowercase + string.digits + "._-"

def is_valid_discord_username(username):
    if len(username) < DISCORD_MIN_LENGTH or len(username) > DISCORD_MAX_LENGTH:
        return False
    if username[0] in "._-" or username[-1] in "._-":
        return False
    if ".." in username or "__" in username or "--" in username:
        return False
    for char in username:
        if char not in DISCORD_ALLOWED:
            return False
    return True

def generate_discord_username(length):
    specials = "._-"
    safe_chars = string.ascii_lowercase + string.digits
    all_chars = safe_chars + specials
    
    for _ in range(100):
        username = random.choice(safe_chars)
        for _ in range(length - 1):
            char = random.choice(all_chars)
            if char in specials and username[-1] in specials:
                char = random.choice(safe_chars)
            username += char
        if username[-1] in specials:
            username = username[:-1] + random.choice(safe_chars)
        if is_valid_discord_username(username):
            return username
    return None

# ================================================================
#  SMART PLATFORM CHECKERS
# ================================================================
def check_with_retry(url, check_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": random.choice(USER_AGENTS),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache"
                }
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                status = response.status
                body = response.read().decode('utf-8', errors='ignore')
                return check_func(status, body)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return True
            return check_func(e.code, "")
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(random.uniform(0.5, 1.5))
                continue
            return None
    return None

# ================================================================
#  PLATFORMS WITH SMART CHECKERS
# ================================================================
PLATFORMS = {
    "instagram": {
        "url": "https://www.instagram.com/{}/",
        "check": lambda status, body: status == 404 or "user_not_found" in body or "Page Not Found" in body
    },
    "twitter": {
        "url": "https://twitter.com/{}/",
        "check": lambda status, body: status == 404 or "user-not-found" in body.lower() or "This account doesn't exist" in body
    },
    "github": {
        "url": "https://github.com/{}",
        "check": lambda status, body: status == 404 or "Page not found" in body
    },
    "tiktok": {
        "url": "https://www.tiktok.com/@{}",
        "check": lambda status, body: status == 404 or "Couldn't find" in body or "This account could not be found" in body
    },
    "snapchat": {
        "url": "https://www.snapchat.com/add/{}",
        "check": lambda status, body: status == 404 or "Could not find" in body
    },
    "reddit": {
        "url": "https://www.reddit.com/user/{}/",
        "check": lambda status, body: status == 404 or "Page not found" in body
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
    },
    "discord": {
        "url": "https://discord.com/users/{}",
        "check": lambda status, body: status == 404 or "User not found" in body
    }
}

# ================================================================
#  CHECK USERNAME FUNCTION
# ================================================================
def check_username(username, platform):
    config = PLATFORMS.get(platform)
    if not config:
        return None
    
    url = config["url"].format(username)
    
    if platform == "discord":
        vanity_url = f"https://discord.com/invite/{username}"
        vanity_result = check_with_retry(vanity_url, lambda s, b: s == 404)
        if vanity_result is False:
            return False
        if vanity_result is True:
            profile_result = check_with_retry(url, config["check"])
            return profile_result
        return check_with_retry(url, config["check"])
    
    return check_with_retry(url, config["check"])

# ================================================================
#  WEBHOOK SENDER
# ================================================================
def send_to_webhook(webhook_url, username, platform):
    try:
        embed = {
            "embeds": [{
                "title": "🎯 RARE USERNAME FOUND!",
                "color": 0x00ff00,
                "fields": [
                    {"name": "👤 Username", "value": f"`@{username}`", "inline": True},
                    {"name": "🌐 Platform", "value": platform.capitalize(), "inline": True},
                    {"name": "📅 Date", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False},
                    {"name": "🔗 Link", "value": f"[Click Here]({PLATFORMS[platform]['url'].format(username)})", "inline": False}
                ],
                "footer": {"text": f"{COPYRIGHT} | {AUTHOR}"}
            }]
        }
        
        data = json.dumps(embed).encode('utf-8')
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": random.choice(USER_AGENTS)},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status in [200, 204]
    except:
        return False

# ================================================================
#  USERS GENERATOR
# ================================================================
def generate_username(length, pattern=None):
    chars = string.ascii_lowercase + string.digits
    if pattern == "letters":
        chars = string.ascii_lowercase
    elif pattern == "mix":
        chars = string.ascii_lowercase + string.digits + "._-"
    
    first_chars = string.ascii_lowercase + string.digits
    username = random.choice([c for c in chars if c in first_chars])
    
    for _ in range(length - 1):
        ch = random.choice(chars)
        if ch in "._-" and username[-1] in "._-":
            ch = random.choice(string.ascii_lowercase + string.digits)
        username += ch
    
    if username[-1] in "._-":
        username = username[:-1] + random.choice(string.ascii_lowercase + string.digits)
    
    return username

def generate_batch(length, count, pattern=None, platform=None):
    seen = set()
    result = []
    attempts = 0
    max_attempts = count * 100
    
    while len(result) < count and attempts < max_attempts:
        attempts += 1
        
        if platform == "discord":
            username = generate_discord_username(length)
            if username and username not in seen:
                seen.add(username)
                result.append(username)
        else:
            username = generate_username(length, pattern)
            if username not in seen:
                seen.add(username)
                result.append(username)
    
    return result

# ================================================================
#  MAIN HUNTING ENGINE
# ================================================================
def hunt_with_webhook(length, count, platforms, webhook_url, pattern=None, discord_only=False):
    results = {p: [] for p in platforms}
    total_found = 0
    webhook_sent = 0
    
    print(f"\n{col(Colors.BLUE, '[*]')} Generating {count} usernames (length {length})...")
    
    all_usernames = []
    if discord_only:
        for _ in range(count * 3):
            u = generate_discord_username(length)
            if u and u not in all_usernames:
                all_usernames.append(u)
                if len(all_usernames) >= count:
                    break
    else:
        all_usernames = generate_batch(length, count, pattern)
    
    print(f"{col(Colors.GREEN, '[+]')} Generated {len(all_usernames)} usernames\n")
    
    total_checks = len(all_usernames) * len(platforms)
    checked = 0
    
    for username in all_usernames:
        for platform in platforms:
            checked += 1
            sys.stdout.write(f"\r{col(Colors.CYAN, '[⏳]')} Checking {checked}/{total_checks}...   ")
            sys.stdout.flush()
            
            available = check_username(username, platform)
            
            if available is True:
                results[platform].append(username)
                total_found += 1
                sys.stdout.write(f"\r{col(Colors.GREEN, '[✅]')} {col(Colors.WHITE, username)} → {col(Colors.CYAN, platform)} AVAILABLE!          \n")
                sys.stdout.flush()
                
                if webhook_url:
                    if send_to_webhook(webhook_url, username, platform):
                        webhook_sent += 1
                        print(f"{col(Colors.GREEN, '  📤')} Sent to Webhook")
            
            time.sleep(random.uniform(0.2, 0.5))
    
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()
    
    return results, total_found, webhook_sent

# ================================================================
#  MENU & DISPLAY
# ================================================================
def main_menu():
    print_banner()
    
    menu = f"""
{Colors.YELLOW}┌──────────────────────────────────────────────────────────────┐
{Colors.YELLOW}│{Colors.WHITE}  [1] 3-Letter Usernames  — EXTREMELY RARE       {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [2] 4-Letter Usernames  — VERY RARE            {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [3] 5-Letter Usernames  — RARE                 {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [4] 6-Letter Usernames  — MODERATE             {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [5] Custom Length                              {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [6] Letters Only (No Numbers)                  {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [7] Discord Only (Valid Usernames)             {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.WHITE}  [8] Check Single Username                      {Colors.YELLOW}│
{Colors.YELLOW}│{Colors.RED}  [0] Exit                                       {Colors.YELLOW}│
{Colors.YELLOW}└──────────────────────────────────────────────────────────────┘{Colors.RESET}
    """
    print(menu)
    
    choice = input(f"{col(Colors.CYAN, 'ninja@xtreme ~$ ')}").strip()
    
    print(f"\n{Colors.YELLOW}┌────────────────────────────────────────────────────────────┐")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  Select Platforms (comma separated)               {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  1.Insta  2.Twitter  3.GitHub  4.TikTok           {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  5.Snap   6.Reddit   7.Pinterest  8.Twitch        {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  9.YouTube  10.Telegram  11.Discord               {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  'all' for all  |  'social' for all except Discord {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    platforms_input = input(f"{col(Colors.CYAN, 'Select Platforms > ')}").strip()
    
    platform_map = {
        "1": "instagram", "2": "twitter", "3": "github", "4": "tiktok",
        "5": "snapchat", "6": "reddit", "7": "pinterest", "8": "twitch",
        "9": "youtube", "10": "telegram", "11": "discord"
    }
    
    if platforms_input.lower() == "all":
        platforms = list(PLATFORMS.keys())
    elif platforms_input.lower() == "social":
        platforms = [p for p in PLATFORMS.keys() if p != "discord"]
    else:
        platforms = []
        for p in platforms_input.replace(" ", "").split(","):
            if p in platform_map:
                platforms.append(platform_map[p])
        if not platforms:
            platforms = ["instagram", "twitter", "github"]
    
    try:
        count = int(input(f"{col(Colors.CYAN, 'Count (1-200) > ')}").strip() or "50")
        if count < 1: count = 10
        if count > 200: count = 200
    except:
        count = 50
    
    print(f"\n{Colors.YELLOW}┌────────────────────────────────────────────────────────────┐")
    print(f"{Colors.YELLOW}│{Colors.WHITE}  🔗 Webhook URL (Discord/Telegram)                {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}│{Colors.DIM}  Leave empty for local save only                    {Colors.YELLOW}│")
    print(f"{Colors.YELLOW}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    webhook_url = input(f"{col(Colors.CYAN, 'Webhook URL > ')}").strip()
    
    return choice, platforms, count, webhook_url

def display_results(results, total_found, webhook_sent):
    print(f"\n{Colors.YELLOW}╔═══════════════════════════════════════════════════════════════╗")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  📊 XTREME HUNT RESULTS                           {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  ──────────────────────────────────────────────    {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  ✅ FOUND: {total_found} usernames                    {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}║{Colors.WHITE}  📤 SENT TO WEBHOOK: {webhook_sent}                 {Colors.YELLOW}║")
    print(f"{Colors.YELLOW}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    for platform, usernames in results.items():
        if usernames:
            print(f"{col(Colors.CYAN, f'► {platform.upper()}')} — {len(usernames)} found")
            for i, u in enumerate(usernames[:20], 1):
                print(f"    {i:2}. {col(Colors.GREEN, u)}")
            if len(usernames) > 20:
                print(f"    ... and {len(usernames)-20} more")
            print()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with open(f"xtreme_hunt_{timestamp}.json", "w") as f:
        json.dump({"results": results, "total": total_found, "webhook_sent": webhook_sent}, f, indent=2)
    
    with open(f"xtreme_usernames_{timestamp}.txt", "w") as f:
        f.write("=" * 60 + "\n")
        f.write(f"  {VERSION}\n")
        f.write(f"  {COPYRIGHT}\n")
        f.write(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for platform, usernames in results.items():
            if usernames:
                f.write(f"[{platform.upper()}]\n")
                for u in usernames:
                    f.write(f"  @{u}\n")
                f.write("\n")
    
    print(f"{col(Colors.GREEN, '[+]')} Results saved!")

# ================================================================
#  MAIN
# ================================================================
def main():
    print(f"{Colors.DIM}\n{VERSION} | {COPYRIGHT}{Colors.RESET}")
    time.sleep(0.5)
    
    while True:
        try:
            result = main_menu()
            if result == "0" or result == 0:
                print(f"\n{col(Colors.GREEN, '[+]')} Goodbye! | {VERSION}\n")
                break
            
            if isinstance(result, tuple):
                choice, platforms, count, webhook_url = result
            else:
                continue
            
            length_map = {"1": 3, "2": 4, "3": 5, "4": 6}
            pattern = None
            discord_only = False
            
            if choice in length_map:
                length = length_map[choice]
            elif choice == "5":
                try:
                    length = int(input(f"{col(Colors.CYAN, 'Length (2-20) > ')}").strip() or "4")
                    if length < 2: length = 2
                    if length > 20: length = 20
                except:
                    length = 4
            elif choice == "6":
                length = 4
                pattern = "letters"
            elif choice == "7":
                length = 4
                discord_only = True
                platforms = ["discord"]
            elif choice == "8":
                username = input(f"{col(Colors.CYAN, 'Username > ')}").strip()
                if not username: continue
                print(f"\n{col(Colors.BLUE, '[*]')} Checking @{username}...\n")
                for platform in platforms:
                    available = check_username(username, platform)
                    status = "✅ AVAILABLE" if available is True else "❌ TAKEN" if available is False else "⚠️ UNKNOWN"
                    color = Colors.GREEN if available is True else Colors.RED if available is False else Colors.YELLOW
                    print(f"  {col(color, status)} {platform:12}")
                    if available is True and webhook_url:
                        send_to_webhook(webhook_url, username, platform)
                    time.sleep(0.3)
                input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to continue...")
                continue
            else:
                length = 4
            
            clear_screen()
            print_banner()
            print(f"\n{col(Colors.RED, '[🔥]')} Starting XTREME hunt...")
            print(f"  Length: {length} | Count: {count} | Platforms: {len(platforms)}")
            if webhook_url:
                print(f"  📤 Webhook: {col(Colors.GREEN, 'Enabled')}")
            print()
            
            start = time.time()
            results, total_found, webhook_sent = hunt_with_webhook(
                length, count, platforms, webhook_url, pattern, discord_only
            )
            elapsed = time.time() - start
            
            display_results(results, total_found, webhook_sent)
            print(f"\n{Colors.DIM}[*] Time: {elapsed:.1f}s | {COPYRIGHT}{Colors.RESET}")
            
            input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to continue...")
            
        except KeyboardInterrupt:
            print(f"\n{col(Colors.YELLOW, '[!]')} Interrupted")
            break
        except Exception as e:
            print(f"\n{col(Colors.RED, f'[!] Error: {e}')}")
            input(f"\n{col(Colors.YELLOW, '[*]')} Press Enter to continue...")

if __name__ == "__main__":
    main()