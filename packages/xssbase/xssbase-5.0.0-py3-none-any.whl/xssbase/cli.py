import argparse
import os
import sys
import platform
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from .main import test_xss_payloads, xss_payloads_default
from .utils import download_edgedriver

def main():
    if platform.system() != 'Windows':
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="XSSbase - A professional tool for scanning XSS vulnerabilities.",
        epilog="Author: Fidal\nGitHub: https://github.com/mr-fidal\n\n"
               "Copyright 2024 Fidal. All rights reserved. \n"
               "payload list : https://mrfidal.in/cyber-security/xssbase/payload-list.html"
               "Unauthorized copying of this tool, via any medium is strictly prohibited."
    )
    parser.add_argument('--url', required=True, help='URL to test for XSS vulnerability')
    parser.add_argument('--payload', help='File containing XSS payloads to use')
    args = parser.parse_args()

    if args.payload and not os.path.exists(args.payload):
        sys.exit(1)

    download_edgedriver()

    arch = platform.architecture()[0]
    edgedriver_path = 'edgedriver_win64/msedgedriver.exe' if arch == '64bit' else 'edgedriver_win32/msedgedriver.exe'

    service = EdgeService(edgedriver_path)
    driver = webdriver.Edge(service=service)

    if args.payload:
        with open(args.payload, 'r', encoding='utf-8') as f:
            payloads = [line.strip() for line in f.readlines()]
    else:
        payloads = xss_payloads_default

    try:
        test_xss_payloads(driver, args.url, payloads)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
