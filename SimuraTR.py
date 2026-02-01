#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMURAZXTR v1.0 - Advanced Intelligence Gathering System
Created by: Project Simura
Version: 1.0.0
"""

import os
import sys
import argparse
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.tracker import SimuraTracker
from utils.logger import SimuraLogger
from utils.visualizer import DataVisualizer

BANNER = f"""{Fore.CYAN}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  ███████╗██╗███╗   ███╗██╗   ██╗██████╗  █████╗ ███████╗║
║  ██╔════╝██║████╗ ████║██║   ██║██╔══██╗██╔══██╗╚══███╔╝║
║  ███████╗██║██╔████╔██║██║   ██║██████╔╝███████║  ███╔╝ ║
║  ╚════██║██║██║╚██╔╝██║██║   ██║██╔══██╗██╔══██║ ███╔╝  ║
║  ███████║██║██║ ╚═╝ ██║╚██████╔╝██║  ██║██║  ██║███████╗║
║  ╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝║
║                                                          ║
║  ╔════════════════════════════════════════════════════╗  ║
║  ║          T A R G E T   R E S O L V E R            ║  ║
║  ╚════════════════════════════════════════════════════╝  ║
║                                                          ║
║  Version: 1.0.0 | Mode: UNRESTRICTED                    ║
║  Created by: YANG | Project: SIMURA                     ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

class SimurazxTR:
    def __init__(self):
        self.logger = SimuraLogger()
        self.tracker = SimuraTracker()
        self.visualizer = DataVisualizer()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_banner(self):
        """Display customized banner"""
        print(BANNER)
        print(f"{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] Session ID: {self.session_id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[*] SIMURAZXTR initialized in UNRESTRICTED mode{Style.RESET_ALL}\n")
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='SIMURAZXTR - Advanced Intelligence Gathering System',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s -t target@email.com -m all
  %(prog)s -t 192.168.1.1 -m ip -o json
  %(prog)s -t "username" -m social -d 3
            """
        )
        
        parser.add_argument('-t', '--target', required=True, help='Target (IP, Email, Username, Phone)')
        parser.add_argument('-m', '--mode', required=True, 
                          choices=['all', 'ip', 'email', 'social', 'phone', 'darkweb'],
                          help='Investigation mode')
        parser.add_argument('-o', '--output', default='txt',
                          choices=['txt', 'json', 'html', 'pdf', 'csv'],
                          help='Output format')
        parser.add_argument('-d', '--depth', type=int, default=2,
                          help='Search depth (1-5, higher = more thorough)')
        parser.add_argument('-p', '--proxy', help='Proxy server (format: http://user:pass@host:port)')
        parser.add_argument('--stealth', action='store_true',
                          help='Enable stealth mode (slower, less detectable)')
        parser.add_argument('--no-cache', action='store_true',
                          help='Disable cache for fresh results')
        
        return parser.parse_args()
    
    def execute_module(self, target, mode, depth, proxy=None):
        """Execute the appropriate tracking module"""
        results = {}
        
        try:
            if mode == 'all' or mode == 'ip':
                print(f"{Fore.CYAN}[+] Gathering IP Intelligence...{Style.RESET_ALL}")
                ip_info = self.tracker.geolocate_ip(target)
                results['ip_info'] = ip_info
                
            if mode == 'all' or mode == 'email':
                print(f"{Fore.CYAN}[+] Analyzing Email Address...{Style.RESET_ALL}")
                email_info = self.tracker.analyze_email(target)
                results['email_info'] = email_info
                
            if mode == 'all' or mode == 'social':
                print(f"{Fore.CYAN}[+] Scanning Social Media Platforms...{Style.RESET_ALL}")
                social_info = self.tracker.scan_social_media(target, depth)
                results['social_info'] = social_info
                
            if mode == 'all' or mode == 'phone':
                print(f"{Fore.CYAN}[+] Resolving Phone Number...{Style.RESET_ALL}")
                phone_info = self.tracker.resolve_phone(target)
                results['phone_info'] = phone_info
                
            if mode == 'all' or mode == 'darkweb':
                print(f"{Fore.RED}[+] Monitoring Dark Web Mentions...{Style.RESET_ALL}")
                darkweb_info = self.tracker.check_darkweb(target)
                results['darkweb_info'] = darkweb_info
                
        except Exception as e:
            self.logger.error(f"Module execution failed: {str(e)}")
            return None
            
        return results
    
    def main(self):
        """Main execution flow"""
        self.print_banner()
        args = self.parse_arguments()
        
        # Log session start
        self.logger.info(f"Starting session {self.session_id}")
        self.logger.info(f"Target: {args.target}")
        self.logger.info(f"Mode: {args.mode}")
        
        # Execute intelligence gathering
        print(f"{Fore.YELLOW}[~] Initiating intelligence gathering on: {args.target}{Style.RESET_ALL}")
        
        results = self.execute_module(
            target=args.target,
            mode=args.mode,
            depth=args.depth,
            proxy=args.proxy
        )
        
        if results:
            # Generate visualization
            if args.mode == 'all':
                self.visualizer.generate_relationship_map(results, args.target)
            
            # Generate report
            report_path = self.tracker.generate_report(
                results=results,
                target=args.target,
                format=args.output,
                session_id=self.session_id
            )
            
            print(f"{Fore.GREEN}[✓] Operation completed successfully!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[✓] Report saved to: {report_path}{Style.RESET_ALL}")
            
            # Show summary
            self.display_summary(results)
        else:
            print(f"{Fore.RED}[✗] Intelligence gathering failed{Style.RESET_ALL}")
            sys.exit(1)
    
    def display_summary(self, results):
        """Display operation summary"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 OPERATION SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for category, data in results.items():
            if data:
                count = len(data) if isinstance(data, (list, dict)) else 1
                print(f"{Fore.GREEN}• {category.upper()}: {count} intelligence points collected{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        tool = SimurazxTR()
        tool.main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Operation interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[✗] Critical error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)