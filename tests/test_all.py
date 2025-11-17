"""
Comprehensive Test Suite Runner
Run all tests with: pytest tests/ -v
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    # Run all tests with verbose output
    pytest.main(["-v", "--tb=short", "tests/"])

