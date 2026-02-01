import requests
import socket
import whois
import dns.resolver
import json
import time
from typing import Dict, List, Any
import concurrent.futures

class SimuraTracker:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.social_platforms = {
            'facebook': 'https://facebook.com/{}',
            'twitter': 'https://twitter.com/{}',
            'instagram': 'https://instagram.com/{}',
            'github': 'https://github.com/{}',
            'linkedin': 'https://linkedin.com/in/{}',
            'reddit': 'https://reddit.com/user/{}',
            'telegram': 'https://t.me/{}',
            'tiktok': 'https://tiktok.com/@{}',
            'youtube': 'https://youtube.com/@{}',
            'discord': 'https://discord.com/users/{}'
        }
    
    def geolocate_ip(self, ip_address: str) -> Dict[str, Any]:
        """Enhanced IP geolocation with multiple sources"""
        results = {}
        
        try:
            # Primary source: ipapi
            response = requests.get(f'https://ipapi.co/{ip_address}/json/', 
                                  headers={'User-Agent': 'SimurazxTR/1.0'})
            if response.status_code == 200:
                results['ipapi'] = response.json()
            
            # Secondary source: ipinfo
            response = requests.get(f'https://ipinfo.io/{ip_address}/json')
            if response.status_code == 200:
                results['ipinfo'] = response.json()
            
            # DNS resolution
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                results['dns'] = {'hostname': hostname}
            except:
                results['dns'] = {'hostname': 'Not resolved'}
            
            # WHOIS lookup
            try:
                whois_info = whois.whois(ip_address)
                results['whois'] = str(whois_info)
            except:
                results['whois'] = 'WHOIS lookup failed'
            
            # Port scanning (basic)
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389]
            results['open_ports'] = []
            
            for port in common_ports[:10]:  # Limit to 10 ports for speed
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    results['open_ports'].append(port)
                sock.close()
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def analyze_email(self, email: str) -> Dict[str, Any]:
        """Comprehensive email analysis"""
        results = {
            'email': email,
            'breaches': [],
            'social_profiles': [],
            'metadata': {}
        }
        
        try:
            # Check for breaches (using haveibeenpwned API)
            headers = {'User-Agent': 'SimurazxTR-Email-Checker'}
            response = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
                headers=headers
            )
            
            if response.status_code == 200:
                results['breaches'] = response.json()
            
            # Extract domain
            domain = email.split('@')[-1]
            results['domain_info'] = {
                'domain': domain,
                'mx_records': self.get_mx_records(domain)
            }
            
            # Check common social platforms
            username = email.split('@')[0]
            results['possible_usernames'] = [
                username,
                username.replace('.', ''),
                username.split('.')[0] if '.' in username else None
            ]
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def scan_social_media(self, username: str, depth: int = 2) -> Dict[str, Any]:
        """Scan multiple social media platforms for username"""
        results = {
            'username': username,
            'profiles_found': [],
            'profiles_checked': []
        }
        
        def check_platform(platform_name: str, url_template: str) -> Dict[str, Any]:
            """Check individual platform"""
            url = url_template.format(username)
            platform_result = {
                'platform': platform_name,
                'url': url,
                'exists': False,
                'status_code': None
            }
            
            try:
                headers = {'User-Agent': self.user_agents[0]}
                response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                platform_result['status_code'] = response.status_code
                
                # Platform-specific existence checks
                if response.status_code == 200:
                    if platform_name == 'github':
                        if f'/{username}"' in response.text.lower():
                            platform_result['exists'] = True
                    elif platform_name == 'twitter':
                        if 'twitter.com/' in response.url:
                            platform_result['exists'] = True
                    else:
                        # Generic check - if username appears in page
                        if username.lower() in response.text.lower():
                            platform_result['exists'] = True
                            
            except requests.RequestException:
                pass
            
            return platform_result
        
        # Use threading for faster scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_platform = {
                executor.submit(check_platform, name, url): name 
                for name, url in self.social_platforms.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_platform):
                result = future.result()
                results['profiles_checked'].append(result)
                if result['exists']:
                    results['profiles_found'].append(result)
        
        return results
    
    def get_mx_records(self, domain: str) -> List[str]:
        """Get MX records for domain"""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            return [str(record.exchange) for record in mx_records]
        except:
            return []
    
    def generate_report(self, results: Dict, target: str, format: str = 'txt', session_id: str = '') -> str:
        """Generate comprehensive report"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"reports/simuratrix_report_{target}_{timestamp}.{format}"
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        elif format == 'txt':
            with open(filename, 'w') as f:
                f.write(f"SIMURAZXTR Intelligence Report\n")
                f.write(f"{'='*50}\n")
                f.write(f"Target: {target}\n")
                f.write(f"Session: {session_id}\n")
                f.write(f"Generated: {time.ctime()}\n")
                f.write(f"{'='*50}\n\n")
                
                for category, data in results.items():
                    f.write(f"\n[{category.upper()}]\n")
                    f.write(f"{'-'*30}\n")
                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(f"{data}\n")
        
        return filename