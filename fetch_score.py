#!/usr/bin/env python3
"""
SecurityScorecard API Client - Fetch Company Security Rating

This script retrieves the security rating for a given company domain
using the SecurityScorecard API.

Requirements:
    pip install requests python-dotenv

Usage:
    1. Set your API key in a `.env` file:
       SSC_API_KEY=your_api_key_here

    2. Run:
       python fetch_score.py example.com
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_BASE_URL = "https://api.securityscorecard.io"
API_KEY = os.getenv("SSC_API_KEY")

if not API_KEY:
    print("Error: SSC_API_KEY not found in environment.", file=sys.stderr)
    print("Please set it in a .env file or as an environment variable.")
    sys.exit(1)

def get_company_score(domain: str):
    """Fetch security score for a given domain."""
    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
        "cache-control": "no-cache"
    }
    url = f"{API_BASE_URL}/companies/{domain}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        score = data.get("score", "N/A")
        grade = data.get("grade", "N/A")
        return score, grade
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Error: Domain '{domain}' not found in SecurityScorecard.", file=sys.stderr)
        else:
            print(f"HTTP Error: {e}", file=sys.stderr)
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None, None

def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch_score.py <company-domain>", file=sys.stderr)
        sys.exit(1)

    domain = sys.argv[1].lower().strip().rstrip('/')
    score, grade = get_company_score(domain)

    if score and grade:
        print(f"Domain: {domain}")
        print(f"Security Score: {score}")
        print(f"Grade: {grade}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
