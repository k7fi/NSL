import os
import sys
import re
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from typing import List, Dict, Optional
import random
import readline
import argparse
# try:
#     import readline  # For Unix-based systems
# except ImportError:
#     import pyreadline3 as readline  # type: ignore # For Windows

class NmapScriptLookup:
    def __init__(self):
        self.console = Console()
        self.script_dirs = [
            "/usr/share/nmap/scripts",
            "/usr/local/share/nmap/scripts",
            "/usr/share/nmap/nselib"
        ]
        self.search_results = []
        self.command_history = []
        self.history_index = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_welcome()

    def display_welcome(self):
        fonts = Figlet().getFonts()
        colors = ["bold red", "bold green", "bold yellow", "bold blue", "bold magenta","bold cyan", "bold white"]
        styles = ["bold", "italic", "underline","strike"]
        random_font = random.choice(fonts)
        random_color = random.choice(colors)
        random_style = random.choice(styles)
        f = Figlet(font=random_font)
        self.console.print(f.renderText('NSL'), style=f"{random_color} {random_style}")
        self.console.print("Nmap Script Lookup Tool", style="bold green")
        self.display_help()

    def display_help(self):
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="green")

        commands = {
            "-s <keyword>": "Search for scripts",
            "categories": "Display script categories",
            "-l <number/name>": "Display script description",
            "-a <number/name>": "Display script arguments",
            "-u <number/name>": "Display script usage",
            "info <number/name>": "Display detailed script information",
            "discovery": "Display discovery techniques",
            "firewall": "Display firewall evasion techniques",
            "clear": "Clear screen",
            "-q or 'exit'": "Quit program"
        }

        for cmd, desc in commands.items():
            help_table.add_row(cmd, desc)

        self.console.print(help_table)

    def check_script_arguments(self, script_path: str) -> bool:
        try:
            with open(script_path, 'r') as f:
                content = f.read()
                return '@args' in content
        except:
            return False

    def get_script_help(self, script_path: str) -> str:
        try:
            output = subprocess.check_output(['nmap', '--script-help', script_path], 
                                          stderr=subprocess.STDOUT, 
                                          text=True)
            # Remove "Starting Nmap" line and process output
            lines = output.split('\n')
            processed_lines = []
            for line in lines:
                if 'Starting Nmap' not in line:
                    # Colorize categories and script names
                    if 'Categories:' in line:
                        categories = line.split(':')[1].strip()
                        line = f"Categories: [cyan]{categories}[/cyan]"
                    elif script_path and os.path.basename(script_path) in line:
                        script_name = os.path.basename(script_path)
                        line = line.replace(script_name, f"[green]{script_name}[/green]")
                    processed_lines.append(line)
            return '\n'.join(processed_lines)
        except subprocess.CalledProcessError:
            return "Failed to get script help"

    def display_script_info(self, content: str, info_type: str, script_path: str = None):
        if info_type == '-l' and script_path:
            # Display both nmap help and description from file
            nmap_help = self.get_script_help(script_path)
            self.console.print(Panel(nmap_help, title="Script Help"))

            description = self.extract_info(content, r'description\s*=\s*\[\[(.*?)\]\]')
            if description != "Not found":
                self.console.print(Panel(description, title="Script Description"))

        elif info_type == '-a':
            args = self.extract_info(content, r'@args\s*(.*?)(?=@|\Z)')
            if args == "Not found":
                self.console.print("This script does not accept any arguments.", style="yellow")
                return
            self.console.print(Panel(args, title="Arguments"))

        elif info_type == 'info':
            patterns = {
                'Author': r'@author\s*(.*?)(?=@|\Z)',
                'License': r'@license\s*(.*?)(?=@|\Z)',
                'Categories': r'categories\s*=\s*{\s*(.*?)\s*}',
                'Dependencies': r'dependencies\s*=\s*{\s*(.*?)\s*}'
            }
            info_panel = ""
            for title, pattern in patterns.items():
                value = self.extract_info(content, pattern)
                if value != "Not found":
                    info_panel += f"[cyan]{title}:[/cyan] {value}\n"
            self.console.print(Panel(info_panel, title="Script Information"))

        elif info_type == '-u':
            usage = self.extract_info(content, r'@usage\s*(.*?)(?=@|\Z)')
            self.console.print(Panel(usage, title="Usage"))

    def process_command(self, command: str) -> bool:
        parts = command.strip().split()
        if not parts:
            return True

        cmd = parts[0].lower()
        arg = ' '.join(parts[1:]) if len(parts) > 1 else ''

        if cmd == '-q' or cmd == 'exit':
            return False
        elif cmd == 'clear':
            self.clear_screen()
        elif cmd == '-s' :
            self.search_scripts(arg)
        elif cmd == 'categories':
            self.display_categories()
        elif cmd == 'firewall':
            self.display_firewall_evasion()
        elif cmd == 'discovery':
            self.display_discovery_techniques()
        elif cmd in ['-l', '-a', '-u', 'info']:
            if not self.search_results:
                self.console.print("Please search for scripts first using -s <keyword>", style="red")
            elif content := self.get_script_content(arg):
                script_path = self.search_results[int(arg) - 1] if arg.isdigit() else next((s for s in self.search_results if arg in s), None)
                self.display_script_info(content, cmd, script_path)
        else:
            self.console.print("Invalid command.", style="red")
            self.display_help()

        return True

    def display_firewall_evasion(self):
        table = Table(title="Firewall Evasion Techniques")
        table.add_column("Technique", style="cyan")
        table.add_column("Description", style="yellow", width=40)
        table.add_column("Command", style="green")
        
        techniques = [
            ("Fragmentation", "Split packets into smaller fragments", "nmap -f [target]"),
            ("MTU Size", "Set custom MTU size to bypass firewall rules", "nmap --mtu <value> [target]"),
            ("Source Port", "Use trusted ports (e.g., 53 for DNS)", "nmap --source-port <port> [target]"),
            ("Data Length", "Add random data to packets", "nmap --data-length <size> [target]"),
            ("Random Hosts", "Randomize scan order to avoid detection", "nmap --randomize-hosts [target]"),
            ("MAC Spoof", "Disguise scanning machine identity", "nmap --spoof-mac <MAC> [target]"),
            ("Bad Checksum", "Send packets with incorrect checksums", "nmap --badsum [target]"),
            ("Idle Scan", "Use zombie host to hide true source", "nmap -sI <zombie> [target]"),
            ("Decoy Scan", "Use multiple fake IP addresses", "nmap -D <decoys> [target]")
        ]
        for technique, desc, command in techniques:
            # Split command into parts
            command_parts = command.split()

            # Create a Rich Text object
            formatted_command = Text()

            # Process and colorize each part
            for index, word in enumerate(command_parts):
                if index == 1:  # Second element (nmap option)
                    formatted_command.append(word, style="bold yellow")
                elif word == "[target]":  # Target indicator
                    formatted_command.append(" " + word, style="bold magenta")
                elif index == 2 and word != "[target]":  # Other elements (parameters like <value>)
                    formatted_command.append(" " + word, style="bold cyan")
                else:
                    formatted_command.append(" " + word,style="bold green")# First element (nmap)

            # Add row to table with properly formatted Rich Text
            table.add_row(technique, desc, formatted_command)
        # for technique, desc, command in techniques:
        #     table.add_row(technique, desc, command)
        
        self.console.print(table)

    def display_discovery_techniques(self):
        table = Table(title="Discovery Techniques")
        table.add_column("Scan Type", style="cyan")
        table.add_column("Command", style="green")
        
        techniques = {
            "SYN scan": "nmap -sS [target]",
            "TCP connect scan": "nmap -sT [target]",
            "UDP scan": "nmap -sU [target]",
            "FIN scan": "nmap -sF [target]",
            "Xmas scan": "nmap -sX [target]",
            "NULL scan": "nmap -sN [target]",
            "ACK scan": "nmap -sA [target]",
            "Window scan": "nmap -sW [target]",
            "Maimon scan": "nmap -sM [target]",
            "Idle scan": "nmap -sI [target]",
            "Ping scan": "nmap -sP [target]",
            "List scan": "nmap -sL [target]",
            "ARP scan": "nmap -PR [target]",
            "Traceroute": "nmap --traceroute [target]",
            "ICMP timeout scan": "nmap -PN [target]",
            "ICMP timestamp scan": "nmap -PO [target]",
            "ICMP address mask scan": "nmap -PM [target]",
            "ICMP echo scan": "nmap -PE [target]",
            "ICMP netmask scan": "nmap -PP [target]",
            "DNS server specification": "nmap --dns-servers [target]",
            "Alternative DNS lookup": "nmap --system-dns [target]"
        }
        
        for technique, command in techniques.items():
            table.add_row(technique, command)
        
        self.console.print(table)

    def display_categories(self):
        categories = {
            'auth': 'Authentication related scripts',
            'broadcast': 'Broadcast and network discovery scripts',
            'default': 'Default scripts run with -sC',
            'discovery': 'Host and service discovery scripts',
            'dos': 'Denial of Service scripts',
            'exploit': 'Exploit scripts',
            'external': 'Scripts that use external services',
            'fuzzer': 'Fuzzing scripts',
            'intrusive': 'Intrusive scripts',
            'malware': 'Malware detection scripts',
            'safe': 'Safe scripts',
            'vuln': 'Vulnerability detection scripts'
        }

        table = Table(title="Script Categories")
        table.add_column("Category", style="cyan")
        table.add_column("Description", style="green")
        
        for category, description in categories.items():
            table.add_row(category, description)
            
        self.console.print(table)

    def search_scripts(self, keyword: str) -> List[str]:
        self.search_results = []
        for script_dir in self.script_dirs:
            if os.path.exists(script_dir):
                for file in os.listdir(script_dir):
                    if file.endswith('.nse') and keyword.lower() in file.lower():
                        self.search_results.append(os.path.join(script_dir, file))
        
        if self.search_results:
            table = Table(title=f"Search Results for '{keyword}'")
            table.add_column("No.", style="cyan")
            table.add_column("Script Name", style="green")
            table.add_column("Path", style="yellow")
            table.add_column("Has Args", style="magenta")
            
            for i, script in enumerate(self.search_results, 1):
                has_args = "Yes" if self.check_script_arguments(script) else "No"
                table.add_row(str(i), os.path.basename(script), script, has_args)
            
            self.console.print(table)
        else:
            self.console.print(f"No scripts found matching '{keyword}'", style="red")
        
        return self.search_results

    def get_script_content(self, identifier: str) -> Optional[str]:
        try:
            idx = int(identifier) - 1
            script_path = self.search_results[idx]
        except (ValueError, IndexError):
            script_path = next((s for s in self.search_results if identifier in s), None)
        
        if script_path and os.path.exists(script_path):
            with open(script_path, 'r') as f:
                return f.read()
        return None

    def extract_info(self, content: str, pattern: str) -> str:
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        if matches:
            return '\n'.join(matches)
        return "Not found"

    def run(self):
        self.display_welcome()
        readline.parse_and_bind('tab: complete')
        while True:
            try:
                command = input("\nnsl> ").strip()
                if command:
                    if not self.process_command(command):
                        break
            except KeyboardInterrupt:
                print("\nUse 'quit' or '-q' to exit")
            except Exception as e:
                self.console.print(f"Error: {str(e)}", style="red")

def parse_arguments():
    """Handles command-line arguments."""
    parser = argparse.ArgumentParser(description="Nmap Script Lookup Tool")
    parser.add_argument("-s", "--search", help="Search for scripts by keyword", type=str)
    parser.add_argument("--discovery", action="store_true", help="Display discovery techniques")
    parser.add_argument("--firewall", action="store_true", help="Display firewall evasion techniques")
    return parser.parse_args()  # Return parsed arguments

def main():
    args = parse_arguments()  # Get command-line arguments
    nsl = NmapScriptLookup()

    if args.search:
        nsl.search_scripts(args.search)
    elif args.discovery:
        nsl.display_discovery_techniques()
    elif args.firewall:
        nsl.display_firewall_evasion()
    
    nsl.run()

# def main():
#     nsl = NmapScriptLookup()
#     nsl.run()

if __name__ == "__main__":
    main()