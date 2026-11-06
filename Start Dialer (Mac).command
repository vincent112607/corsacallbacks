#!/bin/bash
cd "$(dirname "$0")"
python3 dialer_server.py || { echo "Python 3 is needed: install it free from python.org, then run this again."; read -n1; }
