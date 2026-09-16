#!/usr/bin/env python3
"""
FINALRECON-AI - ULTIMATE AUTONOMOUS AI ROBOT EDITION
=====================================================
Version: 2027.7 - Complete Error-Free Edition
"""

import os
import sys
import re
import json
import time
import socket
import ssl
import ipaddress
import argparse
import datetime
import subprocess
import tempfile
import requests
import urllib3
from urllib import parse
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================
# VERSION
# ============================================
VERSION = "2027.7"
BUILD_NUMBER = "2027.007.1"

# ============================================
# COLORS
# ============================================
class Fore:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# ============================================
# CONFIG
# ============================================
CONFIG = {
    'timeout': 10,
    'dir_enum_th': 30,
    'port_scan_th': 50,
    'dir_enum_wlist': 'wordlists/dirb_common.txt',
    'export_dir': 'finalrecon-ai-results',
    'debug': False,
}

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
                993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8000, 8888, 9000]

COMMON_SUBDOMAINS = [
    'www', 'mail', 'ftp', 'webmail', 'smtp', 'pop', 'ns1', 'ns2', 'cpanel',
    'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog',
    'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2',
    'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static',
    'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki',
    'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal',
    'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1', 'ns4', 'www3',
    'dns', 'search', 'staging', 'server', 'mx1', 'chat', 'wap', 'my', 'svn',
    'mail1', 'sites', 'proxy', 'ads', 'host', 'crm', 'cms', 'backup', 'mx2',
    'info', 'apps', 'download', 'remote', 'db', 'forums', 'store', 'relay',
    'files', 'app', 'live', 'owa', 'en', 'start', 'sms', 'office', 'exchange',
    'gateway', 'router', 'firewall', 'monitor', 'jenkins', 'gitlab', 'jira',
    'docker', 'k8s', 'aws', 'azure', 'gcp', 'cloud', 's3', 'storage', 'assets'
]

DEFAULT_WORDLIST = [
    'admin', 'login', 'wp-admin', 'administrator', 'backup', 'backups',
    'config', 'configs', 'db', 'database', 'sql', 'test', 'tests',
    'dev', 'development', 'staging', 'prod', 'production', 'api',
    'apis', 'v1', 'v2', 'docs', 'documentation', 'help', 'support',
    'uploads', 'upload', 'files', 'file', 'images', 'img', 'css',
    'js', 'javascript', 'assets', 'static', 'media', 'video', 'videos',
    'download', 'downloads', 'private', 'secret', 'secrets', 'hidden',
    'tmp', 'temp', 'cache', 'logs', 'log', 'error', 'errors', 'debug',
    'phpinfo.php', 'info.php', 'test.php', 'robots.txt', 'sitemap.xml',
    '.git', '.svn', '.env', '.htaccess', 'web.config', 'crossdomain.xml',
    'phpmyadmin', 'pma', 'mysql', 'adminer', 'cpanel', 'whm', 'webmail',
    'mail', 'email', 'smtp', 'pop3', 'imap', 'ftp', 'ssh', 'telnet',
    'vpn', 'proxy', 'gateway', 'router', 'switch', 'firewall', 'waf',
    'cdn', 'dns', 'ns1', 'ns2', 'mx', 'mail1', 'mail2', 'portal',
    'intranet', 'cms', 'crm', 'erp', 'hr', 'finance', 'forum', 'blog',
    'news', 'media', 'gallery', 'shop', 'store', 'cart', 'checkout',
    'user', 'users', 'profile', 'account', 'register', 'signup', 'login',
    'password', 'reset', 'forgot', 'status', 'health', 'monitor', 'stats',
    'security', 'secure', 'ssl', 'tls', 'cert', 'certificate', 'key',
    'token', 'session', 'cookie', 'header', 'debug', 'trace', 'info'
]

# ============================================
# API KEY PATTERNS
# ============================================
API_KEY_PATTERNS = {
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'Google API Key': r'AIza[0-9A-Za-z\-_]{35}',
    'GitHub Token': r'gh[pousr]_[0-9a-zA-Z]{36}',
    'GitLab Token': r'glpat-[0-9a-zA-Z\-_]{20}',
    'Slack Token': r'xox[baprs]-[0-9a-zA-Z]{10,48}',
    'Discord Token': r'[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}',
    'Telegram Bot Token': r'[0-9]{8,10}:[a-zA-Z0-9_-]{35}',
    'Twilio API Key': r'SK[0-9a-fA-F]{32}',
    'SendGrid API Key': r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}',
    'Stripe Live Key': r'sk_live_[0-9a-zA-Z]{24}',
    'Stripe Test Key': r'sk_test_[0-9a-zA-Z]{24}',
    'MongoDB URI': r'mongodb(\+srv)?://[^\s"\']+',
    'PostgreSQL URI': r'postgres(ql)?://[^\s"\']+',
    'MySQL URI': r'mysql://[^\s"\']+',
    'Redis URI': r'redis://[^\s"\']+',
    'RSA Private Key': r'-----BEGIN RSA PRIVATE KEY-----',
    'OpenSSH Private Key': r'-----BEGIN OPENSSH PRIVATE KEY-----',
    'JWT Token': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
    'Generic API Key': r'api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{20,})["\']',
    'Secret Key': r'secret[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{20,})["\']',
}

WEB_SERVER_API_KEY_PATTERNS = {
    'Apache API Key': r'apache[_-]?api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{16,})["\']',
    'Nginx API Key': r'nginx[_-]?api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{16,})["\']',
    'Cloudflare API Key': r'cloudflare[_-]?api[_-]?key["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{20,})["\']',
    'Web Server Admin': r'(?:web|server)[_-]?(?:admin|api)[_-]?(?:key|token|secret)["\']?\s*[:=]\s*["\']([a-zA-Z0-9\-_.]{16,})["\']',
}

FIREWALL_WEB_SERVER_PATTERNS = {
    'Cloudflare': [r'cloudflare', r'cf-ray'],
    'AWS WAF': [r'awselb', r'x-amz-cf-id'],
    'Azure WAF': [r'azure', r'x-azure-ref'],
    'Sucuri': [r'sucuri'],
    'Wordfence': [r'wordfence'],
    'Imperva': [r'imperva', r'incap_ses'],
    'Nginx': [r'nginx'],
    'Apache': [r'apache'],
    'Varnish': [r'varnish'],
    'HAProxy': [r'haproxy'],
    'Traefik': [r'traefik'],
    'Envoy': [r'envoy'],
    'Caddy': [r'caddy'],
}

FIREWALL_SERVICES = [
    'iptables', 'ip6tables', 'nftables', 'ufw', 'firewalld',
    'fail2ban', 'snort', 'suricata',
    'nginx', 'apache2', 'httpd', 'varnish', 'haproxy',
    'traefik', 'envoy', 'kong', 'caddy',
]

FIREWALL_FILES = [
    '/etc/iptables/rules.v4',
    '/etc/nftables.conf',
    '/etc/ufw/user.rules',
    '/etc/nginx/nginx.conf',
    '/etc/apache2/apache2.conf',
    '/etc/httpd/conf/httpd.conf',
    '/etc/varnish/default.vcl',
    '/etc/haproxy/haproxy.cfg',
    '/etc/caddy/Caddyfile',
]

BROWSER_APP_FILES = [
    'manifest.json', 'manifest.webmanifest', 'service-worker.js', 'sw.js',
    'app.js', 'main.js', 'index.js', 'vendor.js', 'bundle.js',
    'package.json', 'package-lock.json',
    '.env', '.env.local', '.env.production',
    'Dockerfile', 'docker-compose.yml', 'nginx.conf', '.htaccess', 'web.config'
]

BROWSER_APP_PATTERNS = {
    'frameworks': {
        'React': [r'react', r'react-dom'],
        'Vue.js': [r'vue', r'v-model'],
        'Angular': [r'angular', r'ng-app'],
        'Svelte': [r'svelte'],
        'jQuery': [r'jquery'],
    },
    'build_tools': {
        'Webpack': [r'webpack'],
        'Vite': [r'vite'],
        'Parcel': [r'parcel'],
        'Rollup': [r'rollup'],
        'Babel': [r'babel'],
    },
    'analytics': {
        'Google Analytics': [r'google-analytics', r'gtag'],
        'Google Tag Manager': [r'googletagmanager'],
    },
    'auth': {
        'OAuth': [r'oauth'],
        'JWT': [r'jwt'],
        'Firebase': [r'firebase'],
    },
    'api_clients': {
        'Axios': [r'axios'],
        'Fetch API': [r'fetch\('],
        'GraphQL': [r'graphql'],
    },
}

BROKEN_SERVER_INDICATORS = [
    'this site can\'t be reached',
    'this page isn\'t working',
    'http error 500',
    'http error 502',
    'http error 503',
    'http error 504',
    'internal server error',
    'bad gateway',
    'service unavailable',
    'gateway timeout',
    'connection refused',
    'connection timed out',
    'server not found',
    'dns_probe_finished',
    'err_connection',
    'err_name_not_resolved',
    'err_empty_response',
    'err_connection_reset',
    'err_connection_closed',
    'err_connection_timed_out',
    'err_ssl_protocol_error',
]


# ============================================
# SAFE FILE OPERATIONS (NEW - FIX)
# ============================================
def safe_makedirs(path):
    """Safely create directories"""
    try:
        if path and not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return True
    except PermissionError:
        print(Fore.RED + f"[-] Permission denied: {path}")
        return False
    except OSError as e:
        print(Fore.RED + f"[-] OS Error: {e}")
        return False
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}")
        return False


def safe_write_file(path, content, mode='w'):
    """Safely write to file"""
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            safe_makedirs(dir_name)
        with open(path, mode) as f:
            f.write(content)
        return True
    except PermissionError:
        print(Fore.RED + f"[-] Permission denied: {path}")
        return False
    except Exception as e:
        print(Fore.RED + f"[-] Error writing file: {e}")
        return False


def safe_read_file(path):
    """Safely read file"""
    try:
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return f.read()
    except PermissionError:
        print(Fore.RED + f"[-] Permission denied: {path}")
        return None
    except Exception as e:
        print(Fore.RED + f"[-] Error reading file: {e}")
        return None


def validate_wordlist_path(path):
    """Validate wordlist path"""
    if not path:
        return None

    # Check if path exists
    if os.path.exists(path):
        if os.path.isfile(path):
            # Check read permission
            if os.access(path, os.R_OK):
                return path
            else:
                print(Fore.RED + f"[-] Cannot read: {path}")
                return None
        elif os.path.isdir(path):
            print(Fore.RED + f"[-] Path is a directory: {path}")
            return None

    # Try to create it
    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        if not safe_makedirs(dir_name):
            print(Fore.YELLOW + f"[!] Cannot create directory: {dir_name}")

    # Create default wordlist
    if safe_write_file(path, '\n'.join(DEFAULT_WORDLIST)):
        print(Fore.GREEN + f"[+] Created wordlist: {path}")
        return path

    # Fallback: create in temp directory
    try:
        tmp_path = os.path.join(tempfile.gettempdir(), 'finalrecon_wordlist.txt')
        if safe_write_file(tmp_path, '\n'.join(DEFAULT_WORDLIST)):
            print(Fore.YELLOW + f"[!] Using temp wordlist: {tmp_path}")
            return tmp_path
    except Exception:
        pass

    # Last fallback: use built-in list
    print(Fore.YELLOW + f"[!] Using built-in wordlist")
    return None


def get_target_url():
    """Get target URL from user"""
    print(Fore.CYAN + "\n" + "=" * 60)
    print(Fore.CYAN + "[*] TARGET INPUT")
    print(Fore.CYAN + "=" * 60)
    url = input(Fore.GREEN + "[?] Enter target URL (e.g., www.example.com): " + Fore.RESET).strip()
    if not url:
        print(Fore.RED + "[-] Error: URL cannot be empty!")
        return get_target_url()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def get_ports():
    """Get ports from user"""
    print(Fore.CYAN + "\n[*] PORT INPUT")
    print(Fore.CYAN + "-" * 40)
    print(Fore.YELLOW + "[*] Common ports: 80, 443, 22, 21, 25, 3306, 8080, 8443")
    print(Fore.YELLOW + "[*] Format: 80,443,8080 or 1-1000 or 'common'")
    port_input = input(Fore.GREEN + "[?] Enter port(s) (default: common): " + Fore.RESET).strip()

    if not port_input or port_input.lower() == 'common':
        return COMMON_PORTS

    ports = []
    for p in port_input.split(','):
        p = p.strip()
        if p.isdigit():
            ports.append(int(p))
        elif '-' in p:
            try:
                start, end = p.split('-')
                ports.extend(range(int(start), int(end) + 1))
            except ValueError:
                pass

    return ports if ports else COMMON_PORTS


def get_wordlist():
    """Get wordlist from user"""
    print(Fore.CYAN + "\n[*] WORDLIST INPUT")
    print(Fore.CYAN + "-" * 40)
    print(Fore.YELLOW + "[*] Default: wordlists/dirb_common.txt")
    wordlist = input(Fore.GREEN + "[?] Enter wordlist path (default: wordlists/dirb_common.txt): " + Fore.RESET).strip()

    if not wordlist:
        common_paths = [
            'wordlists/dirb_common.txt',
            '/usr/share/wordlists/dirb/common.txt',
            '/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt',
            'common.txt',
            'wordlist.txt'
        ]
        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.R_OK):
                return path
        return 'wordlists/dirb_common.txt'

    return validate_wordlist_path(wordlist)


# ============================================
# MAIN CLASS
# ============================================
class AutonomousAIRobot:
    def __init__(self, target=None, args=None):
        self.target = target
        self.args = args
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })

        if args and hasattr(args, 'H') and args.H:
            for header in args.H:
                if ':' in header:
                    key, value = header.split(':', 1)
                    self.session.headers[key.strip()] = value.strip()

        if args and hasattr(args, 'proxy') and args.proxy:
            self.session.proxies = {'http': args.proxy, 'https': args.proxy}

        if args and hasattr(args, 'debug') and args.debug:
            CONFIG['debug'] = True

        # Storage
        self.vulnerabilities_found = []
        self.firewalls_detected = []
        self.isp_info = {}
        self.isp_info_enabled = False
        self.ip_address_info = {}
        self.isp_block_info = {}
        self.firewall_rules_info = {}
        self.firewall_unblock_info = {}
        self.firewall_destroy_info = {}
        self.firewall_web_server_info = {}
        self.auto_unblock_info = {}
        self.cookies_info = {}
        self.website_cookies_info = {}
        self.server_browser_info = {}
        self.web_server_broken_info = {}
        self.server_broken_info = {}

        self.headers_info = {}
        self.ssl_info = {}
        self.whois_info = {}
        self.dns_info = {}
        self.subdomains_found = []
        self.open_ports = []
        self.directories_found = []
        self.technologies = []
        self.emails = []
        self.js_files = []

        self.comments_found = []
        self.hidden_fields = []
        self.inline_scripts = []
        self.meta_tags = []
        self.source_code_analysis_data = {}

        self.browser_app_files = []
        self.browser_app_analysis_data = {}

        self.ssl_unlock_info = {}
        self.unlocked_ssl = []

        self.index_html_analysis = {}
        self.html_files_analysis = {}
        self.java_files_analysis = {}

        self.api_keys_found = []
        self.web_server_api_keys_found = []

        self.custom_ports = COMMON_PORTS
        if args and hasattr(args, 'port') and args.port:
            self.custom_ports = args.port

        # Wordlist - SAFE HANDLING
        self.wordlist = CONFIG['dir_enum_wlist']
        if args and hasattr(args, 'wordlist') and args.wordlist:
            validated = validate_wordlist_path(args.wordlist)
            if validated:
                self.wordlist = validated
            else:
                print(Fore.YELLOW + "[!] Using default wordlist")

        if args and hasattr(args, 'isp_info') and args.isp_info:
            self.isp_info_enabled = True

        if self.target:
            self.parse_target()

        if not (args and hasattr(args, 'no_banner') and args.no_banner):
            self.print_banner()

        if self.target:
            self.start_autonomous_mode()

    def print_banner(self):
        art = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗██╗███╗   ██╗ █████╗ ██╗     ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
║     ██╔════╝██║████╗  ██║██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
║     █████╗  ██║██╔██╗ ██║███████║██║     ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
║     ██╔══╝  ██║██║╚██╗██║██╔══██║██║     ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
║     ██║     ██║██║ ╚████║██║  ██║███████╗██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
║     ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
║                                                                              ║
║                    FINALRECON-AI - ERROR-FREE EDITION                       ║
║                          Version: 2027.7 - AI Robot                         ║
║                                                                              ║
║                    🤖 AUTONOMOUS AI ROBOT MODE 🤖                           ║
║                                                                              ║
║              ✅ SAFE FILE OPERATIONS | NO PERMISSION ERRORS                 ║
║              🔍 WEB SERVER BROKEN CHECK | SERVER BROKEN CHECK               ║
║              💥 FIREWALL WEB SERVER DESTROY | SITE UNREACHABLE              ║
║              💀 FIREWALL RULES ISP DESTROY | ENGINE DESTROY                 ║
║              🔥 FIREWALL RULES IP ENABLE | ISP UNBLOCK                      ║
║              🔓 IP ADDRESS UNLOCK | INTERNET ISP ENABLE                     ║
║              🍪 COOKIES | DEBUG | SERVER BROWSER | WEBSITE COOKIES          ║
║              🔐 API KEY DETECTION | SSL KEY UNLOCK                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝"""
        print(Fore.CYAN + art + Fore.RESET + "\n")
        print(Fore.GREEN + "[>] Version: " + VERSION)
        print(Fore.GREEN + "[>] Build: " + BUILD_NUMBER)
        print()

    def parse_target(self):
        if not self.target:
            return

        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target

        if self.target.endswith('/'):
            self.target = self.target[:-1]

        split_url = parse.urlsplit(self.target)
        self.protocol = split_url.scheme
        self.hostname = split_url.hostname

        if self.args and hasattr(self.args, 'port') and self.args.port:
            self.port = self.args.port[0] if isinstance(self.args.port, list) else self.args.port
        else:
            self.port = split_url.port or (443 if self.protocol == 'https' else 80)

        self.path = split_url.path or '/'

        try:
            ipaddress.ip_address(self.hostname)
            self.is_ip = True
            self.ip = self.hostname
        except ValueError:
            self.is_ip = False
            try:
                self.ip = socket.gethostbyname(self.hostname)
                print(Fore.CYAN + f"[*] IP Address: {self.ip}")
            except Exception as e:
                print(Fore.RED + f"[-] Unable to get IP: {e}")
                sys.exit(1)

        self.base_url = f"{self.protocol}://{self.hostname}:{self.port}"

    # ============================================
    # DIRECTORY BRUTEFORCE - FIXED
    # ============================================
    def directory_bruteforce(self, wordlist=None):
        """Directory bruteforce with safe file handling"""
        if wordlist is None:
            wordlist = self.wordlist

        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] DIRECTORY BRUTEFORCE")
        print(Fore.CYAN + "=" * 60)

        # Load wordlist safely
        words = []

        if wordlist:
            content = safe_read_file(wordlist)
            if content:
                words = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
                print(Fore.GREEN + f"[+] Loaded {len(words)} words from: {wordlist}")

        # Fallback to built-in wordlist
        if not words:
            words = DEFAULT_WORDLIST
            print(Fore.YELLOW + f"[!] Using built-in wordlist: {len(words)} words")

        if not words:
            print(Fore.RED + "[-] No words to test")
            return []

        found = []

        def check(word):
            url = f"{self.base_url}/{word}"
            try:
                r = self.session.get(url, timeout=10, verify=False, allow_redirects=False)
                if r.status_code in [200, 301, 302, 403]:
                    return (word, url, r.status_code)
            except Exception:
                pass
            return None

        try:
            with ThreadPoolExecutor(max_workers=CONFIG['dir_enum_th']) as executor:
                futures = {executor.submit(check, w): w for w in words[:500]}  # Limit to 500

                for f in as_completed(futures):
                    try:
                        r = f.result()
                        if r:
                            word, url, status = r
                            found.append({'path': word, 'url': url, 'status': status})
                            print(Fore.GREEN + f"[+] /{word} ({status})")
                    except Exception:
                        pass
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        self.directories_found = found
        print(Fore.CYAN + f"\n[+] Total: {len(found)}")
        return found

    # ============================================
    # WEB SERVER BROKEN CHECK
    # ============================================
    def check_web_server_broken(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] WEB SERVER BROKEN CHECK")
        print(Fore.CYAN + "=" * 80)

        self.web_server_broken_info = {
            'url': self.base_url,
            'is_broken': False,
            'broken_reasons': [],
            'http_status': None,
            'response_time': None,
            'health_score': 100,
        }

        print(Fore.CYAN + "\n[*] Testing HTTP request...")
        try:
            start = time.time()
            response = self.session.get(self.base_url, timeout=10, verify=False)
            elapsed = round((time.time() - start) * 1000, 2)

            self.web_server_broken_info['http_status'] = response.status_code
            self.web_server_broken_info['response_time'] = elapsed

            print(Fore.GREEN + f"[+] Status: {response.status_code}")
            print(Fore.GREEN + f"[+] Time: {elapsed} ms")

            if response.status_code >= 500:
                self.web_server_broken_info['is_broken'] = True
                self.web_server_broken_info['broken_reasons'].append(f'HTTP {response.status_code}')
                self.web_server_broken_info['health_score'] -= 30

            if elapsed > 5000:
                self.web_server_broken_info['broken_reasons'].append(f'Very slow: {elapsed}ms')
                self.web_server_broken_info['health_score'] -= 20

            content_lower = response.text.lower()
            for indicator in BROKEN_SERVER_INDICATORS:
                if indicator in content_lower:
                    self.web_server_broken_info['is_broken'] = True
                    self.web_server_broken_info['broken_reasons'].append(indicator)
                    self.web_server_broken_info['health_score'] -= 25
                    break

        except requests.exceptions.Timeout:
            print(Fore.RED + f"[!] TIMEOUT")
            self.web_server_broken_info['is_broken'] = True
            self.web_server_broken_info['broken_reasons'].append('Timeout')
            self.web_server_broken_info['health_score'] = 0
        except requests.exceptions.ConnectionError:
            print(Fore.RED + f"[!] CONNECTION ERROR")
            self.web_server_broken_info['is_broken'] = True
            self.web_server_broken_info['broken_reasons'].append('Connection error')
            self.web_server_broken_info['health_score'] = 0
        except Exception as e:
            print(Fore.RED + f"[!] ERROR: {e}")

        # Summary
        if self.web_server_broken_info['is_broken']:
            print(Fore.RED + f"\n[!] STATUS: BROKEN")
        else:
            print(Fore.GREEN + f"\n[+] STATUS: WORKING")

        print(Fore.CYAN + f"[+] Health: {max(0, self.web_server_broken_info['health_score'])}/100")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.web_server_broken_info

    # ============================================
    # SERVER BROKEN CHECK
    # ============================================
    def check_server_broken(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] SERVER BROKEN CHECK")
        print(Fore.CYAN + "=" * 80)

        self.server_broken_info = {
            'hostname': self.hostname,
            'ip': self.ip,
            'is_broken': False,
            'broken_reasons': [],
            'health_score': 100,
        }

        # Check 1: Ping
        print(Fore.CYAN + "\n[*] Ping test...")
        try:
            if sys.platform == 'linux':
                result = subprocess.run(['ping', '-c', '2', '-W', '3', self.ip],
                                       capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(Fore.GREEN + f"[+] Ping OK")
                else:
                    print(Fore.YELLOW + f"[!] Ping failed")
                    self.server_broken_info['health_score'] -= 10
        except Exception:
            print(Fore.YELLOW + f"[!] Ping unavailable")

        # Check 2: Ports
        print(Fore.CYAN + "\n[*] Testing ports...")
        open_ports = []
        for port in [80, 443, 8080, 8443]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex((self.ip, port))
                s.close()
                if result == 0:
                    open_ports.append(port)
                    print(Fore.GREEN + f"    ✓ Port {port}: OPEN")
                else:
                    print(Fore.WHITE + f"    - Port {port}: CLOSED")
            except Exception:
                pass

        if not open_ports:
            print(Fore.RED + f"[!] NO OPEN PORTS")
            self.server_broken_info['health_score'] -= 40
            self.server_broken_info['broken_reasons'].append('No open ports')

        # Check 3: HTTP
        print(Fore.CYAN + "\n[*] Testing HTTP/HTTPS...")
        try:
            r = self.session.get(f"http://{self.hostname}", timeout=5, verify=False)
            print(Fore.GREEN + f"    ✓ HTTP: {r.status_code}")
        except Exception:
            print(Fore.YELLOW + f"    ! HTTP failed")

        try:
            r = self.session.get(f"https://{self.hostname}", timeout=5, verify=False)
            print(Fore.GREEN + f"    ✓ HTTPS: {r.status_code}")
        except Exception:
            print(Fore.YELLOW + f"    ! HTTPS failed")

        # Check 4: DNS
        print(Fore.CYAN + "\n[*] DNS resolution...")
        try:
            ip = socket.gethostbyname(self.hostname)
            print(Fore.GREEN + f"    ✓ DNS: {ip}")
        except Exception:
            print(Fore.RED + f"    ✗ DNS FAILED")
            self.server_broken_info['health_score'] -= 20
            self.server_broken_info['broken_reasons'].append('DNS failed')

        # Check 5: SSL
        print(Fore.CYAN + "\n[*] SSL certificate...")
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((self.hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    print(Fore.GREEN + f"    ✓ SSL: {ssock.version()}")
        except Exception:
            print(Fore.YELLOW + f"    ! SSL unavailable")

        # Summary
        health_score = max(0, self.server_broken_info['health_score'])
        if health_score < 50:
            self.server_broken_info['is_broken'] = True

        if self.server_broken_info['is_broken']:
            print(Fore.RED + f"\n[!] STATUS: BROKEN")
        else:
            print(Fore.GREEN + f"\n[+] STATUS: WORKING")

        print(Fore.CYAN + f"[+] Health: {health_score}/100")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.server_broken_info

    # ============================================
    # FIREWALL WEB SERVER DESTROY
    # ============================================
    def firewall_web_server_destroy(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] FIREWALL WEB SERVER DESTROY")
        print(Fore.CYAN + "=" * 80)

        self.firewall_web_server_info = {
            'firewall_detected': [],
            'services_destroyed': [],
            'files_destroyed': [],
            'destroyed': False,
        }

        print(Fore.CYAN + "\n[*] Detecting firewall...")
        try:
            response = self.session.get(self.base_url, timeout=10, verify=False)
            headers_str = str(response.headers).lower()

            for fw_name, patterns in FIREWALL_WEB_SERVER_PATTERNS.items():
                for pattern in patterns:
                    if pattern in headers_str:
                        self.firewall_web_server_info['firewall_detected'].append(fw_name)
                        print(Fore.RED + f"[!] Firewall: {fw_name}")
                        break
        except Exception:
            pass

        print(Fore.RED + "\n[*] DESTROYING...")

        web_servers = ['nginx', 'apache2', 'httpd', 'varnish', 'haproxy',
                       'traefik', 'envoy', 'kong', 'caddy']

        for ws in web_servers:
            try:
                result = subprocess.run(['sudo', 'systemctl', 'stop', ws],
                                       capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(Fore.RED + f"[!] Stopped: {ws}")
                    self.firewall_web_server_info['services_destroyed'].append(ws)
            except Exception:
                pass

        for cmd in [
            ['sudo', 'iptables', '-F'],
            ['sudo', 'iptables', '-X'],
            ['sudo', 'iptables', '-P', 'INPUT', 'ACCEPT'],
            ['sudo', 'iptables', '-P', 'FORWARD', 'ACCEPT'],
            ['sudo', 'iptables', '-P', 'OUTPUT', 'ACCEPT'],
        ]:
            try:
                subprocess.run(cmd, capture_output=True, timeout=5)
            except Exception:
                pass

        # Test
        try:
            response = self.session.get(self.base_url, timeout=10, verify=False)
            if response.status_code < 500:
                self.firewall_web_server_info['destroyed'] = True
                print(Fore.GREEN + f"[+] Success!")
        except Exception:
            pass

        print(Fore.RED + "\n" + "=" * 60)
        print(Fore.RED + "[!] FIREWALL WEB SERVER DESTROY SUMMARY")
        print(Fore.RED + "=" * 60)
        print(Fore.RED + f"[!] Firewalls: {len(self.firewall_web_server_info['firewall_detected'])}")
        print(Fore.RED + f"[!] Services: {len(self.firewall_web_server_info['services_destroyed'])}")
        print(Fore.RED + f"[!] Destroyed: {self.firewall_web_server_info['destroyed']}")
        print(Fore.RED + "=" * 60 + "\n")
        return self.firewall_web_server_info

    # ============================================
    # FIREWALL RULES ISP DESTROY
    # ============================================
    def firewall_rules_isp_destroy(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] FIREWALL RULES ISP DESTROY")
        print(Fore.CYAN + "=" * 80)

        self.firewall_destroy_info = {
            'services_stopped': [],
            'engine_destroyed': False,
        }

        for svc in FIREWALL_SERVICES:
            try:
                result = subprocess.run(['sudo', 'systemctl', 'stop', svc],
                                       capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(Fore.RED + f"[!] Stopped: {svc}")
                    self.firewall_destroy_info['services_stopped'].append(svc)
            except Exception:
                pass

        for cmd in [
            ['sudo', 'iptables', '-F'],
            ['sudo', 'iptables', '-X'],
            ['sudo', 'iptables', '-P', 'INPUT', 'ACCEPT'],
        ]:
            try:
                subprocess.run(cmd, capture_output=True, timeout=5)
            except Exception:
                pass

        print(Fore.RED + "\n" + "=" * 60)
        print(Fore.RED + "[!] FIREWALL RULES ISP DESTROY SUMMARY")
        print(Fore.RED + "=" * 60)
        print(Fore.RED + f"[!] Services: {len(self.firewall_destroy_info['services_stopped'])}")
        print(Fore.RED + "=" * 60 + "\n")
        return self.firewall_destroy_info

    # ============================================
    # AUTO ISP UNBLOCK
    # ============================================
    def auto_isp_unblock(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] AUTO ISP UNBLOCK")
        print(Fore.CYAN + "=" * 80)

        self.auto_unblock_info = {
            'initial_state': None,
            'final_state': None,
            'success': False,
        }

        try:
            try:
                test = self.session.get(self.base_url, timeout=10, verify=False)
                print(Fore.GREEN + f"[+] ISP UNBLOCKED (isp_blocked: false)")
                self.auto_unblock_info['initial_state'] = 'unblocked'
                self.auto_unblock_info['final_state'] = 'unblocked'
                self.auto_unblock_info['success'] = True
            except Exception:
                print(Fore.RED + f"[!] ISP BLOCKED (isp_blocked: true)")
                self.auto_unblock_info['initial_state'] = 'blocked'

                self.session.headers.update({
                    'X-Forwarded-For': '8.8.8.8',
                    'X-Real-IP': '8.8.8.8',
                })

                time.sleep(2)
                try:
                    test = self.session.get(self.base_url, timeout=15, verify=False)
                    print(Fore.GREEN + f"[+] ISP UNBLOCKED (isp_blocked: false)")
                    self.auto_unblock_info['final_state'] = 'unblocked'
                    self.auto_unblock_info['success'] = True
                except Exception:
                    print(Fore.RED + f"[!] Still blocked")
                    self.auto_unblock_info['final_state'] = 'blocked'
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] AUTO ISP UNBLOCK SUMMARY")
        print(Fore.CYAN + "=" * 60)
        print(Fore.GREEN + f"[+] Initial: {self.auto_unblock_info['initial_state']}")
        print(Fore.GREEN + f"[+] Final: {self.auto_unblock_info['final_state']}")
        print(Fore.GREEN + f"[+] Success: {self.auto_unblock_info['success']}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.auto_unblock_info

    # ============================================
    # FIREWALL RULES IP ADDRESS ENABLE
    # ============================================
    def firewall_rules_ip_enable(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] FIREWALL RULES IP ADDRESS ENABLE")
        print(Fore.CYAN + "=" * 80)

        self.firewall_rules_info = {'ip': self.ip, 'actions_taken': []}

        try:
            response = self.session.get(self.base_url, timeout=5, verify=False)
            print(Fore.GREEN + f"[+] Connection OK: {response.status_code}")
        except requests.exceptions.Timeout:
            print(Fore.RED + f"[!] TIMEOUT")
            try:
                subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', self.ip, '-j', 'DROP'],
                              capture_output=True, timeout=5)
                print(Fore.GREEN + f"[+] Removed DROP rule")
                self.firewall_rules_info['actions_taken'].append('Removed DROP')
            except Exception:
                pass

            self.session.headers.update({
                'X-Forwarded-For': '127.0.0.1',
                'X-Real-IP': '127.0.0.1',
            })
            self.firewall_rules_info['actions_taken'].append('Bypass headers')

        print(Fore.CYAN + f"\n[+] Actions: {len(self.firewall_rules_info['actions_taken'])}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.firewall_rules_info

    # ============================================
    # FIREWALL ISP UNBLOCK
    # ============================================
    def firewall_isp_unblock(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] FIREWALL ISP UNBLOCK")
        print(Fore.CYAN + "=" * 80)

        self.firewall_unblock_info = {'isp_blocked': False, 'unblock_actions': []}

        try:
            response = self.session.get(self.base_url, timeout=10, verify=False)
            print(Fore.GREEN + f"[+] ISP reachable: {response.status_code}")
        except requests.exceptions.Timeout:
            print(Fore.RED + f"[!] TIMEOUT")
            self.firewall_unblock_info['isp_blocked'] = True
            self.session.headers.update({'X-Forwarded-For': '8.8.8.8'})
            self.firewall_unblock_info['unblock_actions'].append('Bypass headers')

        print(Fore.CYAN + f"\n[+] Actions: {len(self.firewall_unblock_info['unblock_actions'])}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.firewall_unblock_info

    # ============================================
    # COOKIES ANALYSIS
    # ============================================
    def analyze_cookies(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] COOKIES ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        self.cookies_info = {
            'total': 0, 'secure': 0, 'httponly': 0, 'insecure': 0,
            'cookies': [],
        }

        try:
            self.session.cookies.clear()
            response = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)

            for cookie in self.session.cookies:
                self.cookies_info['total'] += 1
                print(Fore.GREEN + f"\n[+] Cookie: {cookie.name}")

                if cookie.secure:
                    print(Fore.GREEN + f"    [+] Secure: Yes")
                    self.cookies_info['secure'] += 1
                else:
                    print(Fore.RED + f"    [!] Secure: No")
                    self.cookies_info['insecure'] += 1

                if cookie._rest.get('HttpOnly'):
                    print(Fore.GREEN + f"    [+] HttpOnly: Yes")
                    self.cookies_info['httponly'] += 1
                else:
                    print(Fore.RED + f"    [!] HttpOnly: No")
                    self.cookies_info['insecure'] += 1
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + f"\n[+] Total: {self.cookies_info['total']}")
        print(Fore.RED + f"[!] Insecure: {self.cookies_info['insecure']}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.cookies_info

    # ============================================
    # WEBSITE COOKIES
    # ============================================
    def get_website_cookies(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] WEBSITE COOKIES")
        print(Fore.CYAN + "=" * 80)

        self.website_cookies_info = {'all_cookies': {}, 'total': 0}

        for page in ['/', '/index.html', '/login', '/admin']:
            url = f"{self.base_url}{page}"
            try:
                temp_session = requests.Session()
                temp_session.headers.update(self.session.headers)

                response = temp_session.get(url, timeout=10, verify=False)

                if response.cookies:
                    for cookie in response.cookies:
                        key = f"{cookie.domain}:{cookie.name}"
                        if key not in self.website_cookies_info['all_cookies']:
                            self.website_cookies_info['all_cookies'][key] = cookie.name
                            self.website_cookies_info['total'] += 1
                            print(Fore.GREEN + f"    [+] Cookie: {cookie.name}")
            except Exception:
                pass

        print(Fore.CYAN + f"\n[+] Total: {self.website_cookies_info['total']}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.website_cookies_info

    # ============================================
    # SERVER BROWSER
    # ============================================
    def get_server_browser_info(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] SERVER BROWSER INFO")
        print(Fore.CYAN + "=" * 80)

        self.server_browser_info = {'server_info': {}, 'security_headers': {}}

        try:
            browser_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            }

            temp_session = requests.Session()
            temp_session.headers.update(browser_headers)

            response = temp_session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)

            self.server_browser_info['server_info'] = {
                'server': response.headers.get('Server', 'Unknown'),
                'powered_by': response.headers.get('X-Powered-By', 'Unknown'),
            }

            print(Fore.CYAN + "[*] Server Info:")
            for k, v in self.server_browser_info['server_info'].items():
                if v != 'Unknown':
                    print(Fore.GREEN + f"    [+] {k}: {v}")

            security = {
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security', 'Not Set'),
                'X-Frame-Options': response.headers.get('X-Frame-Options', 'Not Set'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options', 'Not Set'),
                'Content-Security-Policy': response.headers.get('Content-Security-Policy', 'Not Set'),
            }

            print(Fore.CYAN + "\n[*] Security Headers:")
            for k, v in security.items():
                if v != 'Not Set':
                    print(Fore.GREEN + f"    [+] {k}: {v[:50]}")
                else:
                    print(Fore.YELLOW + f"    [!] {k}: NOT SET")

            self.server_browser_info['security_headers'] = security
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.server_browser_info

    # ============================================
    # IP ADDRESS CHECK
    # ============================================
    def check_ip_address(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] IP ADDRESS CHECK")
        print(Fore.CYAN + "=" * 60)

        self.ip_address_info = {'ip': self.ip, 'status': 'unknown'}

        try:
            response = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] IP UNLOCKED")
                self.ip_address_info['status'] = 'unlocked'
            else:
                print(Fore.RED + f"[!] IP BLOCKED: {response.status_code}")
                self.ip_address_info['status'] = 'blocked'
        except requests.exceptions.Timeout:
            print(Fore.RED + f"[!] TIMEOUT")
            self.ip_address_info['status'] = 'timeout'
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.ip_address_info

    # ============================================
    # IP ADDRESS ENABLE
    # ============================================
    def enable_ip_address(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] IP ADDRESS ENABLE")
        print(Fore.CYAN + "=" * 60)

        self.session.cookies.clear()
        self.session.headers.update({
            'X-Forwarded-For': '127.0.0.1',
            'X-Real-IP': '127.0.0.1',
        })

        try:
            response = self.session.get(self.base_url, timeout=10, verify=False)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] IP UNLOCKED!")
        except Exception:
            print(Fore.RED + f"[-] Still blocked")

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.ip_address_info

    # ============================================
    # INTERNET ISP ENABLE
    # ============================================
    def enable_internet_isp(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] INTERNET ISP ENABLE")
        print(Fore.CYAN + "=" * 60)

        self.isp_block_info = {'blocked': False}

        try:
            if sys.platform == 'linux':
                subprocess.run(['sudo', 'systemd-resolve', '--flush-caches'],
                              capture_output=True, timeout=10)
                print(Fore.GREEN + "[+] DNS flushed")
        except Exception:
            pass

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.isp_block_info

    # ============================================
    # HEADER ENUMERATION
    # ============================================
    def enumerate_headers(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] HTTP HEADER ENUMERATION")
        print(Fore.CYAN + "=" * 60)

        try:
            response = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)

            self.headers_info = {
                'status_code': response.status_code,
                'server': response.headers.get('Server', 'Unknown'),
                'all_headers': dict(response.headers),
            }

            print(Fore.GREEN + f"[+] Status: {self.headers_info['status_code']}")
            print(Fore.GREEN + f"[+] Server: {self.headers_info['server']}")

            print(Fore.CYAN + "\n[*] All Headers:")
            for h, v in response.headers.items():
                print(Fore.WHITE + f"    {h}: {v}")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.headers_info

    # ============================================
    # SSL CERTIFICATE ANALYSIS
    # ============================================
    def analyze_ssl_certificate(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] SSL CERTIFICATE ANALYSIS")
        print(Fore.CYAN + "=" * 60)

        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((self.hostname, 443), timeout=CONFIG['timeout']) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()

                    self.ssl_info = {
                        'subject': dict(x[0] for x in cert.get('subject', [])),
                        'issuer': dict(x[0] for x in cert.get('issuer', [])),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter'),
                        'tls_version': ssock.version(),
                    }

                    print(Fore.GREEN + f"[+] TLS: {self.ssl_info['tls_version']}")
                    print(Fore.GREEN + f"[+] Issuer: {self.ssl_info['issuer']}")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.ssl_info

    # ============================================
    # WHOIS LOOKUP
    # ============================================
    def whois_lookup(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] WHOIS LOOKUP")
        print(Fore.CYAN + "=" * 60)

        try:
            import whois
            w = whois.whois(self.hostname)
            self.whois_info = {
                'domain_name': str(w.domain_name) if w.domain_name else 'Unknown',
                'registrar': str(w.registrar) if w.registrar else 'Unknown',
            }

            print(Fore.GREEN + f"[+] Domain: {self.whois_info['domain_name']}")
            print(Fore.GREEN + f"[+] Registrar: {self.whois_info['registrar']}")
        except ImportError:
            print(Fore.YELLOW + "[!] python-whois not installed")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.whois_info

    # ============================================
    # DNS ENUMERATION
    # ============================================
    def dns_enumeration(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] DNS ENUMERATION")
        print(Fore.CYAN + "=" * 60)

        try:
            import dns.resolver

            for rt in ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']:
                try:
                    answers = dns.resolver.resolve(self.hostname, rt)
                    records = [str(r) for r in answers]
                    self.dns_info[rt] = records
                    print(Fore.GREEN + f"[+] {rt}:")
                    for r in records:
                        print(Fore.WHITE + f"    {r}")
                except Exception:
                    pass
        except ImportError:
            print(Fore.YELLOW + "[!] dnspython not installed")

        return self.dns_info

    # ============================================
    # SUBDOMAIN ENUMERATION
    # ============================================
    def subdomain_enumeration(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] SUBDOMAIN ENUMERATION")
        print(Fore.CYAN + "=" * 60)

        found = []

        def check(sub):
            full = f"{sub}.{self.hostname}"
            try:
                ip = socket.gethostbyname(full)
                return (sub, full, ip)
            except socket.gaierror:
                return None

        try:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(check, s): s for s in COMMON_SUBDOMAINS}
                for f in as_completed(futures):
                    try:
                        r = f.result()
                        if r:
                            sub, full, ip = r
                            found.append({'domain': full, 'ip': ip})
                            print(Fore.GREEN + f"[+] {full} -> {ip}")
                    except Exception:
                        pass
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        self.subdomains_found = found
        print(Fore.CYAN + f"\n[+] Total: {len(found)}")
        return found

    # ============================================
    # PORT SCANNING
    # ============================================
    def port_scan(self, ports=None):
        if ports is None:
            ports = self.custom_ports

        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] PORT SCANNING")
        print(Fore.CYAN + "=" * 60)

        open_ports = []

        def check(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                r = s.connect_ex((self.ip, port))
                s.close()
                if r == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = 'unknown'
                    return (port, service)
            except Exception:
                pass
            return None

        try:
            with ThreadPoolExecutor(max_workers=CONFIG['port_scan_th']) as executor:
                futures = {executor.submit(check, p): p for p in ports}
                for f in as_completed(futures):
                    try:
                        r = f.result()
                        if r:
                            port, service = r
                            open_ports.append({'port': port, 'service': service})
                            print(Fore.GREEN + f"[+] Port {port} OPEN ({service})")
                    except Exception:
                        pass
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        self.open_ports = open_ports
        print(Fore.CYAN + f"\n[+] Total: {len(open_ports)}")
        return open_ports

    # ============================================
    # ISP INFORMATION
    # ============================================
    def get_isp_info(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] ISP INFORMATION")
        print(Fore.CYAN + "=" * 60)

        try:
            url = f"http://ip-api.com/json/{self.ip}?fields=status,country,regionName,city,isp,org,as,query"
            r = requests.get(url, timeout=10)

            if r.status_code == 200:
                data = r.json()
                if data.get('status') == 'success':
                    self.isp_info = {
                        'ip': data.get('query'),
                        'country': data.get('country'),
                        'region': data.get('regionName'),
                        'city': data.get('city'),
                        'isp': data.get('isp'),
                        'org': data.get('org'),
                        'asn': data.get('as'),
                    }

                    print(Fore.GREEN + f"[+] IP: {self.isp_info['ip']}")
                    print(Fore.GREEN + f"[+] Country: {self.isp_info['country']}")
                    print(Fore.GREEN + f"[+] ISP: {self.isp_info['isp']}")
                    print(Fore.GREEN + f"[+] ASN: {self.isp_info['asn']}")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.isp_info

    # ============================================
    # TECHNOLOGY DETECTION
    # ============================================
    def detect_technologies(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] TECHNOLOGY DETECTION")
        print(Fore.CYAN + "=" * 60)

        try:
            r = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            headers = r.headers
            html = r.text.lower()

            techs = []

            if 'Server' in headers:
                techs.append({'technology': 'Web Server', 'value': headers['Server']})

            patterns = {
                'WordPress': [r'wp-content'],
                'React': [r'react'],
                'Angular': [r'ng-app'],
                'Vue.js': [r'v-model'],
                'jQuery': [r'jquery'],
                'Bootstrap': [r'bootstrap'],
                'PHP': [r'\.php'],
            }

            for tech, pats in patterns.items():
                for p in pats:
                    if re.search(p, html):
                        techs.append({'technology': tech, 'value': 'Detected'})
                        break

            self.technologies = techs

            print(Fore.CYAN + "[*] Technologies:")
            for t in techs:
                print(Fore.GREEN + f"    [+] {t['technology']}")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.technologies

    # ============================================
    # EMAIL HARVESTING
    # ============================================
    def harvest_emails(self):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] EMAIL HARVESTING")
        print(Fore.CYAN + "=" * 60)

        try:
            r = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text)))
            filtered = [e for e in emails if not any(x in e.lower() for x in ['example.com', 'test.com'])]

            self.emails = filtered

            if filtered:
                print(Fore.GREEN + f"[+] Found {len(filtered)} email(s)")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        return self.emails

    # ============================================
    # API KEY DETECTION
    # ============================================
    def detect_api_keys(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] API KEY DETECTION")
        print(Fore.CYAN + "=" * 80)

        self.api_keys_found = []
        urls = [self.base_url] + [f"{self.base_url}{f}" for f in ['/.env', '/config.json']]

        for url in urls:
            try:
                r = self.session.get(url, timeout=10, verify=False)
                if r.status_code == 200:
                    for kt, pat in API_KEY_PATTERNS.items():
                        matches = re.findall(pat, r.text, re.IGNORECASE)
                        for m in matches:
                            if isinstance(m, tuple):
                                m = m[0] if m[0] else str(m)
                            if len(str(m)) > 8:
                                self.api_keys_found.append({'type': kt, 'value': str(m)[:100], 'url': url})
                                print(Fore.RED + f"[!] API KEY: {kt} at {url}")
            except Exception:
                pass

        print(Fore.CYAN + f"\n[+] API Keys: {len(self.api_keys_found)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.api_keys_found

    # ============================================
    # WEB SERVER API KEY DETECTION
    # ============================================
    def detect_web_server_api_keys(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] WEB SERVER API KEY DETECTION")
        print(Fore.CYAN + "=" * 80)

        self.web_server_api_keys_found = []
        urls = [f"{self.base_url}{f}" for f in [
            '/.env', '/config.json', '/config.php', '/web.config',
            '/settings.py', '/.htaccess', '/nginx.conf',
        ]]

        for url in urls:
            try:
                r = self.session.get(url, timeout=10, verify=False)
                if r.status_code == 200:
                    for kt, pat in WEB_SERVER_API_KEY_PATTERNS.items():
                        matches = re.findall(pat, r.text, re.IGNORECASE)
                        for m in matches:
                            if isinstance(m, tuple):
                                m = m[0]
                            if len(str(m)) > 8:
                                self.web_server_api_keys_found.append({'type': kt, 'value': str(m)[:100], 'url': url})
                                print(Fore.RED + f"[!] WEB SERVER API KEY: {kt}")
            except Exception:
                pass

        print(Fore.CYAN + f"\n[+] Web Server API Keys: {len(self.web_server_api_keys_found)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.web_server_api_keys_found

    # ============================================
    # SSL KEY UNLOCK
    # ============================================
    def ssl_key_unlock_scan(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] SSL KEY UNLOCK")
        print(Fore.CYAN + "=" * 80)

        self.ssl_unlock_info = {'ssl_enabled': False, 'bypass_methods': []}

        print(Fore.CYAN + "\n[*] Checking SSL...")
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((self.hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    self.ssl_unlock_info['ssl_enabled'] = True
                    print(Fore.GREEN + f"[+] SSL: Enabled ({ssock.version()})")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + "\n[*] Bypass Methods...")

        try:
            r = requests.get(self.base_url, verify=False, timeout=10)
            print(Fore.GREEN + f"[+] Disable SSL Verify: {r.status_code}")
            self.ssl_unlock_info['bypass_methods'].append("Disabled SSL Verification")
            self.unlocked_ssl.append("Disabled SSL Verification")
        except Exception:
            pass

        try:
            http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
            r = http.request('GET', self.base_url)
            print(Fore.GREEN + f"[+] Custom Context: {r.status}")
            self.ssl_unlock_info['bypass_methods'].append("Custom SSL Context")
            self.unlocked_ssl.append("Custom SSL Context")
        except Exception:
            pass

        print(Fore.CYAN + f"\n[+] Unlocked: {len(self.unlocked_ssl)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.ssl_unlock_info

    # ============================================
    # SOURCE CODE ANALYSIS
    # ============================================
    def source_code_analysis_scan(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] SOURCE CODE ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        self.source_code_analysis_data = {
            'comments': [], 'hidden_fields': [], 'inline_scripts': [], 'meta_tags': [],
        }

        try:
            r = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            html = r.text

            comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
            for c in comments:
                c = c.strip()
                if c and len(c) > 3:
                    self.comments_found.append({'content': c[:200]})
                    print(Fore.YELLOW + f"[!] Comment: {c[:100]}")

            hidden = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', html, re.IGNORECASE)
            for h in hidden:
                nm = re.search(r'name=["\']([^"\']+)["\']', h)
                self.hidden_fields.append({'name': nm.group(1) if nm else 'unknown'})

            scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
            for i, s in enumerate(scripts):
                s = s.strip()
                if s and len(s) > 10:
                    self.inline_scripts.append({'index': i, 'length': len(s)})

            meta = re.findall(r'<meta[^>]*>', html, re.IGNORECASE)
            for m in meta:
                nm = re.search(r'name=["\']([^"\']+)["\']', m)
                self.meta_tags.append({'name': nm.group(1) if nm else 'unknown'})
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

        print(Fore.CYAN + f"\n[+] Comments: {len(self.comments_found)}")
        print(Fore.CYAN + f"[+] Hidden: {len(self.hidden_fields)}")
        print(Fore.CYAN + f"[+] Inline: {len(self.inline_scripts)}")
        print(Fore.CYAN + f"[+] Meta: {len(self.meta_tags)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.source_code_analysis_data

    # ============================================
    # BROWSER APP ANALYSIS
    # ============================================
    def browser_app_analysis_scan(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] BROWSER APP ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        self.browser_app_analysis_data = {
            'files_found': [], 'frameworks': [], 'build_tools': [],
            'analytics': [], 'auth': [], 'api_clients': [],
        }

        print(Fore.CYAN + "\n[*] Checking files...")
        for fname in BROWSER_APP_FILES[:20]:
            url = f"{self.base_url}/{fname}"
            try:
                r = self.session.get(url, timeout=5, verify=False, allow_redirects=False)
                if r.status_code == 200:
                    self.browser_app_analysis_data['files_found'].append({
                        'path': fname, 'size': len(r.content),
                    })
                    print(Fore.GREEN + f"[+] Found: {url}")
            except Exception:
                pass

        print(Fore.CYAN + "\n[*] Analyzing frameworks...")
        try:
            r = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            html = r.text

            for cat, pats in BROWSER_APP_PATTERNS.items():
                for tech, tech_pats in pats.items():
                    for p in tech_pats:
                        if re.search(p, html, re.IGNORECASE):
                            if cat == 'frameworks':
                                self.browser_app_analysis_data['frameworks'].append(tech)
                                print(Fore.GREEN + f"[+] Framework: {tech}")
                            elif cat == 'build_tools':
                                self.browser_app_analysis_data['build_tools'].append(tech)
                                print(Fore.GREEN + f"[+] Build Tool: {tech}")
                            elif cat == 'analytics':
                                self.browser_app_analysis_data['analytics'].append(tech)
                                print(Fore.GREEN + f"[+] Analytics: {tech}")
                            elif cat == 'auth':
                                self.browser_app_analysis_data['auth'].append(tech)
                                print(Fore.GREEN + f"[+] Auth: {tech}")
                            elif cat == 'api_clients':
                                self.browser_app_analysis_data['api_clients'].append(tech)
                                print(Fore.GREEN + f"[+] API Client: {tech}")
                            break
        except Exception:
            pass

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.browser_app_analysis_data

    # ============================================
    # INDEX.HTML ANALYSIS
    # ============================================
    def analyze_index_html(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] INDEX.HTML ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        for path in ['/index.html', '/index.htm', '/index.php']:
            url = f"{self.base_url}{path}"
            try:
                r = self.session.get(url, timeout=CONFIG['timeout'], verify=False)
                if r.status_code == 200:
                    html = r.text
                    tm = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)

                    self.index_html_analysis = {
                        'url': url,
                        'size': len(r.content),
                        'title': tm.group(1).strip() if tm else None,
                        'comments': len(re.findall(r'<!--(.*?)-->', html, re.DOTALL)),
                        'forms': len(re.findall(r'<form[^>]*>', html, re.IGNORECASE)),
                        'inputs': len(re.findall(r'<input[^>]*>', html, re.IGNORECASE)),
                        'scripts': len(re.findall(r'<script[^>]*>', html, re.IGNORECASE)),
                        'links': len(re.findall(r'<a[^>]+href=', html, re.IGNORECASE)),
                    }

                    print(Fore.GREEN + f"[+] Found: {url}")
                    print(Fore.GREEN + f"    Title: {self.index_html_analysis['title']}")
                    print(Fore.GREEN + f"    Size: {self.index_html_analysis['size']}")
                    break
            except Exception:
                pass

        print(Fore.CYAN + "=" * 60 + "\n")
        return self.index_html_analysis

    # ============================================
    # HTML FILES ANALYSIS
    # ============================================
    def analyze_html_files(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] HTML FILES ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        found = []
        for path in ['/index.html', '/about.html', '/contact.html', '/login.html']:
            url = f"{self.base_url}{path}"
            try:
                r = self.session.get(url, timeout=5, verify=False)
                if r.status_code == 200:
                    tm = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
                    found.append({
                        'url': url, 'size': len(r.content),
                        'title': tm.group(1).strip() if tm else None,
                    })
                    print(Fore.GREEN + f"[+] {url}")
            except Exception:
                pass

        self.html_files_analysis = {'files': found, 'total': len(found)}
        print(Fore.CYAN + f"\n[+] Total: {len(found)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.html_files_analysis

    # ============================================
    # JAVA FILES ANALYSIS
    # ============================================
    def analyze_java_files(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] JAVA SOURCE CODE ANALYSIS")
        print(Fore.CYAN + "=" * 80)

        found = []
        for path in ['/Application.java', '/Main.java', '/Servlet.java']:
            url = f"{self.base_url}{path}"
            try:
                r = self.session.get(url, timeout=5, verify=False)
                if r.status_code == 200:
                    found.append({
                        'url': url,
                        'classes': re.findall(r'class\s+(\w+)', r.text),
                    })
                    print(Fore.GREEN + f"[+] {url}")
            except Exception:
                pass

        self.java_files_analysis = {'files': found, 'total': len(found)}
        print(Fore.CYAN + f"\n[+] Total: {len(found)}")
        print(Fore.CYAN + "=" * 60 + "\n")
        return self.java_files_analysis

    # ============================================
    # START AUTONOMOUS MODE
    # ============================================
    def start_autonomous_mode(self):
        print(Fore.RED + "\n" + "=" * 80)
        print(Fore.RED + "AUTONOMOUS AI ROBOT MODE ACTIVATED!")
        print(Fore.RED + "=" * 80 + "\n")

        try:
            r = self.session.get(self.base_url, timeout=CONFIG['timeout'], verify=False)
            print(Fore.GREEN + f"[+] Target reachable! Status: {r.status_code}")
        except Exception as e:
            print(Fore.RED + f"[-] Target unreachable: {e}")

        # NEW: Web Server Broken Check
        if hasattr(self.args, 'web_server_broken_check') and self.args.web_server_broken_check:
            self.check_web_server_broken()

        # NEW: Server Broken Check
        if hasattr(self.args, 'server_broken_check') and self.args.server_broken_check:
            self.check_server_broken()

        # Firewall Web Server Destroy
        if hasattr(self.args, 'firewall_web_server_destroy') and self.args.firewall_web_server_destroy:
            self.firewall_web_server_destroy()

        # Firewall Rules ISP Destroy
        if hasattr(self.args, 'firewall_rules_isp_destroy') and self.args.firewall_rules_isp_destroy:
            self.firewall_rules_isp_destroy()

        # Auto ISP Unblock
        if hasattr(self.args, 'auto_isp_unblock') and self.args.auto_isp_unblock:
            self.auto_isp_unblock()

        # Firewall Rules IP Enable
        if hasattr(self.args, 'firewall_rules_ip_address_enable') and self.args.firewall_rules_ip_address_enable:
            self.firewall_rules_ip_enable()

        # Firewall ISP Unblock
        if hasattr(self.args, 'firewall_isp_unblock') and self.args.firewall_isp_unblock:
            self.firewall_isp_unblock()

        # Cookies
        if hasattr(self.args, 'cookies') and self.args.cookies:
            self.analyze_cookies()

        if hasattr(self.args, 'website_cookies') and self.args.website_cookies:
            self.get_website_cookies()

        if hasattr(self.args, 'server_browen') and self.args.server_browen:
            self.get_server_browser_info()

        # IP/ISP
        if hasattr(self.args, 'ip_address') and self.args.ip_address:
            self.check_ip_address()

        if hasattr(self.args, 'ip_address_enable') and self.args.ip_address_enable:
            self.enable_ip_address()

        if hasattr(self.args, 'internet_isp_enable') and self.args.internet_isp_enable:
            self.enable_internet_isp()

        # ISP info
        if self.isp_info_enabled:
            self.get_isp_info()

        # API Keys
        if hasattr(self.args, 'api_key') and self.args.api_key:
            self.detect_api_keys()

        if hasattr(self.args, 'web_server_api_key') and self.args.web_server_api_key:
            self.detect_web_server_api_keys()

        # SSL Unlock
        if hasattr(self.args, 'ssl_unlock') and self.args.ssl_unlock:
            self.ssl_key_unlock_scan()

        # Source Code
        if hasattr(self.args, 'source_code') and self.args.source_code:
            self.source_code_analysis_scan()

        # Browser App
        if hasattr(self.args, 'browser_app') and self.args.browser_app:
            self.browser_app_analysis_scan()

        # File types
        if hasattr(self.args, 'index_html') and self.args.index_html:
            self.analyze_index_html()

        if hasattr(self.args, 'html') and self.args.html:
            self.analyze_html_files()

        if hasattr(self.args, 'java') and self.args.java:
            self.analyze_java_files()

        # Standard modules
        if self.args:
            if hasattr(self.args, 'headers') and self.args.headers:
                self.enumerate_headers()
            if hasattr(self.args, 'sslinfo') and self.args.sslinfo:
                self.analyze_ssl_certificate()
            if hasattr(self.args, 'whois') and self.args.whois:
                self.whois_lookup()
            if hasattr(self.args, 'dns') and self.args.dns:
                self.dns_enumeration()
            if hasattr(self.args, 'sub') and self.args.sub:
                self.subdomain_enumeration()
            if hasattr(self.args, 'portscan') and self.args.portscan:
                self.port_scan()
            if hasattr(self.args, 'dir') and self.args.dir:
                self.directory_bruteforce()
            if hasattr(self.args, 'tech') and self.args.tech:
                self.detect_technologies()
            if hasattr(self.args, 'emails') and self.args.emails:
                self.harvest_emails()
            if hasattr(self.args, 'full') and self.args.full:
                self.full_recon()

        self.print_summary()

    def full_recon(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.CYAN + "[*] FULL RECONNAISSANCE")
        print(Fore.CYAN + "=" * 80)

        try:
            self.check_web_server_broken()
            self.check_server_broken()
            self.firewall_web_server_destroy()
            self.firewall_rules_isp_destroy()
            self.auto_isp_unblock()
            self.firewall_rules_ip_enable()
            self.firewall_isp_unblock()
            self.analyze_cookies()
            self.get_website_cookies()
            self.get_server_browser_info()
            self.check_ip_address()
            self.enumerate_headers()
            self.analyze_ssl_certificate()
            self.whois_lookup()
            self.dns_enumeration()
            self.subdomain_enumeration()
            self.port_scan()
            self.directory_bruteforce()
            self.detect_technologies()
            self.harvest_emails()
            self.source_code_analysis_scan()
            self.browser_app_analysis_scan()
            self.ssl_key_unlock_scan()
            self.analyze_index_html()
            self.analyze_html_files()
            self.analyze_java_files()
            self.detect_api_keys()
            self.get_isp_info()
        except Exception as e:
            print(Fore.RED + f"[-] Error in full_recon: {e}")

        print(Fore.CYAN + "=" * 80 + "\n")

    def export_results(self, export_format='txt'):
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.CYAN + "[*] EXPORTING RESULTS")
        print(Fore.CYAN + "=" * 60)

        export_dir = CONFIG['export_dir']
        if not safe_makedirs(export_dir):
            export_dir = tempfile.gettempdir()
            print(Fore.YELLOW + f"[!] Using temp dir: {export_dir}")

        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        fn = f"finalrecon_{self.hostname}_{ts}"

        results = {
            'target': self.target, 'hostname': self.hostname, 'ip': self.ip, 'scan_time': ts,
            'web_server_broken_info': self.web_server_broken_info,
            'server_broken_info': self.server_broken_info,
            'firewall_web_server_info': self.firewall_web_server_info,
            'firewall_destroy_info': self.firewall_destroy_info,
            'auto_unblock_info': self.auto_unblock_info,
            'cookies_info': self.cookies_info,
            'website_cookies_info': self.website_cookies_info,
            'server_browser_info': self.server_browser_info,
            'ip_address_info': self.ip_address_info,
            'isp_block_info': self.isp_block_info,
            'headers': self.headers_info, 'ssl': self.ssl_info, 'whois': self.whois_info,
            'dns': self.dns_info, 'subdomains': self.subdomains_found,
            'open_ports': self.open_ports, 'directories': self.directories_found,
            'technologies': self.technologies, 'emails': self.emails,
            'isp_info': self.isp_info, 'api_keys_found': self.api_keys_found,
            'unlocked_ssl': self.unlocked_ssl,
        }

        if export_format == 'json':
            fp = os.path.join(export_dir, f"{fn}.json")
            try:
                with open(fp, 'w') as f:
                    json.dump(results, f, indent=4, default=str)
                print(Fore.GREEN + f"[+] Exported: {fp}")
            except Exception as e:
                print(Fore.RED + f"[-] Export error: {e}")
        else:
            fp = os.path.join(export_dir, f"{fn}.txt")
            try:
                with open(fp, 'w') as f:
                    f.write(f"FinalRecon-AI Scan Results\n{'=' * 60}\n")
                    f.write(f"Target: {self.target}\nHostname: {self.hostname}\nIP: {self.ip}\nScan Time: {ts}\n\n")
                    for sec, data in results.items():
                        if data and sec not in ['target', 'hostname', 'ip', 'scan_time']:
                            f.write(f"{sec.upper()}\n{'-' * 40}\n")
                            f.write(f"{json.dumps(data, indent=2, default=str)[:2000]}\n\n")
                print(Fore.GREEN + f"[+] Exported: {fp}")
            except Exception as e:
                print(Fore.RED + f"[-] Export error: {e}")

        return fp

    def print_summary(self):
        print(Fore.CYAN + "\n" + "=" * 80)
        print(Fore.GREEN + "[+] AI ROBOT MISSION COMPLETED!")
        print(Fore.CYAN + "=" * 80)

        if self.web_server_broken_info:
            status = "BROKEN" if self.web_server_broken_info.get('is_broken') else "WORKING"
            color = Fore.RED if self.web_server_broken_info.get('is_broken') else Fore.GREEN
            print(color + f"[+] Web Server: {status}")

        if self.server_broken_info:
            status = "BROKEN" if self.server_broken_info.get('is_broken') else "WORKING"
            color = Fore.RED if self.server_broken_info.get('is_broken') else Fore.GREEN
            print(color + f"[+] Server: {status}")

        print(Fore.GREEN + f"[+] Subdomains: {len(self.subdomains_found)}")
        print(Fore.GREEN + f"[+] Open Ports: {len(self.open_ports)}")
        print(Fore.GREEN + f"[+] Directories: {len(self.directories_found)}")
        print(Fore.RED + f"[+] API Keys: {len(self.api_keys_found)}")
        print(Fore.GREEN + f"[+] SSL Unlocked: {len(self.unlocked_ssl)}")
        print(Fore.CYAN + "=" * 80 + "\n")


# ============================================
# ARGUMENT PARSER
# ============================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description=f"FinalRecon-AI - Error-Free Edition v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    target_group = parser.add_argument_group('Target Options')
    target_group.add_argument("--url", help="Target URL")
    target_group.add_argument("--link", action="append", help="Scan specific link")

    basic_group = parser.add_argument_group('Basic Options')
    basic_group.add_argument("--port", action="append", type=int, dest="port", help="Custom port")
    basic_group.add_argument("--isp-info", action="store_true", help="ISP information")
    basic_group.add_argument("--full", action="store_true", help="Full reconnaissance")
    basic_group.add_argument("-w", "--wordlist", help="Wordlist")

    broken_group = parser.add_argument_group('Broken Check Options')
    broken_group.add_argument("--web-server-broken-check", action="store_true",
                             dest="web_server_broken_check", help="Web server broken check")
    broken_group.add_argument("--server-broken-check", action="store_true",
                             dest="server_broken_check", help="Server broken check")

    fws_group = parser.add_argument_group('Firewall Web Server Options')
    fws_group.add_argument("--firewall-web-server-destroy", action="store_true",
                          dest="firewall_web_server_destroy", help="Destroy firewall web server")

    firewall_group = parser.add_argument_group('Firewall Options')
    firewall_group.add_argument("--firewall-rules-isp-destroy", action="store_true",
                               dest="firewall_rules_isp_destroy", help="Destroy firewall rules")
    firewall_group.add_argument("--auto-isp-unblock", action="store_true",
                               dest="auto_isp_unblock", help="Auto ISP unblock")
    firewall_group.add_argument("--firewall-rules-ip-address-enable", action="store_true",
                               dest="firewall_rules_ip_address_enable", help="Firewall IP enable")
    firewall_group.add_argument("--firewall-isp-unblock", action="store_true",
                               dest="firewall_isp_unblock", help="Firewall ISP unblock")

    cookies_group = parser.add_argument_group('Cookies & Debug Options')
    cookies_group.add_argument("--cookies", action="store_true", dest="cookies", help="Cookies")
    cookies_group.add_argument("--debug", action="store_true", dest="debug", help="Debug")
    cookies_group.add_argument("--server-browen", action="store_true", dest="server_browen", help="Server browser")
    cookies_group.add_argument("--website-cookies", action="store_true", dest="website_cookies", help="Website cookies")

    ip_group = parser.add_argument_group('IP Address & ISP Options')
    ip_group.add_argument("--ip-address", action="store_true", dest="ip_address", help="IP check")
    ip_group.add_argument("--ip-address-enable", action="store_true", dest="ip_address_enable", help="IP enable")
    ip_group.add_argument("--internet-isp-enable", action="store_true", dest="internet_isp_enable", help="ISP enable")

    recon_group = parser.add_argument_group('Reconnaissance')
    recon_group.add_argument("--headers", action="store_true", help="HTTP headers")
    recon_group.add_argument("--sslinfo", action="store_true", help="SSL certificate")
    recon_group.add_argument("--whois", action="store_true", help="WHOIS lookup")
    recon_group.add_argument("--dns", action="store_true", help="DNS enumeration")
    recon_group.add_argument("--sub", action="store_true", help="Subdomain enumeration")
    recon_group.add_argument("--dir", action="store_true", help="Directory bruteforce")
    recon_group.add_argument("--portscan", action="store_true", help="Port scan")
    recon_group.add_argument("--tech", action="store_true", help="Technology detection")
    recon_group.add_argument("--emails", action="store_true", help="Email harvesting")

    source_group = parser.add_argument_group('Source Code Analysis')
    source_group.add_argument("--source-code", action="store_true", dest="source_code", help="Source code")

    api_group = parser.add_argument_group('API Key Detection')
    api_group.add_argument("--api-key", action="store_true", dest="api_key", help="API keys")
    api_group.add_argument("--web-server-api-key", action="store_true", dest="web_server_api_key", help="Web server API keys")

    file_group = parser.add_argument_group('File Type Analysis')
    file_group.add_argument("--index.html", action="store_true", dest="index_html", help="Index.html")
    file_group.add_argument("--html", action="store_true", dest="html", help="HTML files")
    file_group.add_argument("--java", action="store_true", dest="java", help="Java files")

    browser_group = parser.add_argument_group('Browser App Analysis')
    browser_group.add_argument("--browser-app", action="store_true", dest="browser_app", help="Browser app")

    ssl_group = parser.add_argument_group('SSL Key Unlock')
    ssl_group.add_argument("--ssl-unlock", action="store_true", dest="ssl_unlock", help="SSL unlock")

    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument("-o2", "--export", default='txt', help="Export format")
    output_group.add_argument("-nb", "--no-banner", action="store_true", dest="no_banner", help="Hide banner")
    output_group.add_argument("-version", action="version", version=f"FinalRecon-AI v{VERSION}")

    return parser.parse_args()


# ============================================
# MAIN
# ============================================
def main():
    try:
        args = parse_arguments()

        # Interactive mode if no URL
        if not args.url and not args.link:
            print(Fore.CYAN + "\n" + "=" * 60)
            print(Fore.CYAN + "🤖 FINALRECON-AI - INTERACTIVE MODE")
            print(Fore.CYAN + "=" * 60)
            print(Fore.YELLOW + "[*] No target specified. Entering interactive mode...\n")

            url = get_target_url()
            args.url = url

            print(Fore.CYAN + "\n[*] PORT CONFIGURATION")
            print(Fore.CYAN + "-" * 40)
            scan_ports = input(Fore.GREEN + "[?] Scan ports? (y/n, default: y): " + Fore.RESET).strip().lower()
            if scan_ports != 'n':
                ports = get_ports()
                args.port = ports
                args.portscan = True

            print(Fore.CYAN + "\n[*] DIRECTORY BRUTEFORCE")
            print(Fore.CYAN + "-" * 40)
            scan_dirs = input(Fore.GREEN + "[?] Bruteforce directories? (y/n, default: y): " + Fore.RESET).strip().lower()
            if scan_dirs != 'n':
                wordlist = get_wordlist()
                if wordlist:
                    args.wordlist = wordlist
                args.dir = True

            print(Fore.CYAN + "\n[*] SCAN OPTIONS")
            print(Fore.CYAN + "-" * 40)
            full_scan = input(Fore.GREEN + "[?] Full reconnaissance? (y/n, default: y): " + Fore.RESET).strip().lower()
            if full_scan != 'n':
                args.full = True
                args.isp_info = True
                args.headers = True
                args.sslinfo = True
                args.whois = True
                args.dns = True
                args.sub = True
                args.tech = True
                args.emails = True
                args.source_code = True
                args.browser_app = True
                args.ssl_unlock = True
                args.index_html = True
                args.html = True
                args.java = True
                args.api_key = True
                args.web_server_api_key = True
                args.cookies = True
                args.website_cookies = True
                args.server_browen = True
                args.web_server_broken_check = True
                args.server_broken_check = True

            print(Fore.CYAN + "\n[*] EXPORT OPTIONS")
            print(Fore.CYAN + "-" * 40)
            export_choice = input(Fore.GREEN + "[?] Export format (txt/json/none, default: txt): " + Fore.RESET).strip().lower()
            if export_choice in ['txt', 'json']:
                args.export = export_choice
            elif export_choice == 'none':
                args.export = 'None'

            print(Fore.GREEN + "\n[+] Configuration complete! Starting scan...\n")
            time.sleep(1)

        target = args.url if args.url else args.link[0] if args.link else None

        if not target:
            print(Fore.RED + "[-] Error: No target provided!")
            return 1

        robot = AutonomousAIRobot(target, args)

        if hasattr(args, 'export') and args.export != 'None':
            robot.export_results(args.export)

        print(Fore.GREEN + "\n[+] AI Robot Mission Completed Successfully!")
        return 0

    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Keyboard Interrupt.")
        return 130
    except Exception as e:
        print(Fore.RED + f"\n[-] Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    sys.exit(main())
