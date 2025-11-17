#!/bin/bash
# Comprehensive Test Runner Script

echo "=========================================="
echo "Pet Adoption System - Test Suite"
echo "=========================================="
echo ""

echo "1. Running Unit Tests..."
pytest tests/unit/ -v
echo ""

echo "2. Running Integration Tests..."
pytest tests/integration/ -v
echo ""

echo "3. Running All Tests with Coverage..."
pytest tests/ -v --cov=backend --cov=ml --cov-report=term-missing --cov-report=html
echo ""

echo "4. Test Summary..."
pytest tests/ --co -q
echo ""

echo "=========================================="
echo "Tests Complete!"
echo "Coverage report: htmlcov/index.html"
echo "=========================================="

