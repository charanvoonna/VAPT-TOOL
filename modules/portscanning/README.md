README.md
# Port Scanning Module - VAPT Tool

## Overview

This module is part of a Vulnerability Assessment and Penetration Testing (VAPT) tool.
It performs port scanning on specified targets using multiple techniques, including:

* TCP Connect Scan
* SYN Scan
* Slow Timing Scan (Evasion Technique)
* Decoy Scan (Evasion Technique)

The module supports scanning single ports, multiple ports, or port ranges with multi-threaded scanning for faster results. Colored terminal output is provided for better readability.

## Features

* Scan TCP ports on any target IP or domain
* Specify ports as individual numbers, comma-separated lists, or ranges (e.g., `22,80,443` or `20-50`)
* Multithreaded scanning (up to 10 threads) for efficiency
* Output results with clear color-coded status
* Easily extendable and modular OOP-based design

## Requirements

* Python 3.x
* napcap
* `colorama` Python package (for colored terminal output)

Install `colorama` with:

```bash
pip install colorama
```
