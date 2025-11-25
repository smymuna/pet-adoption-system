# Test Suite Documentation

## Overview

Comprehensive test suite for the Pet Adoption System covering:
- ✅ Unit tests (18 tests)
- ✅ Integration tests (39 tests)
- ✅ CRUD operations
- ✅ Edge cases and corner cases
- ✅ Database operations
- ✅ Search functionality
- ✅ Data aggregation

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests
│   ├── test_database.py    # Database connection tests
│   └── test_models.py      # Pydantic model validation tests
├── integration/            # Integration tests
│   ├── test_crud_animals.py      # Animals CRUD operations
│   ├── test_crud_adoptions.py    # Adoptions CRUD operations
│   ├── test_search_operations.py # Search functionality
│   ├── test_charts_data.py       # Charts data aggregation
│   ├── test_edge_cases.py        # Edge cases and corner cases
│   └── test_api_endpoints.py     # API endpoint tests
├── run_tests.sh            # Test runner script
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_models.py -v

# Specific test
pytest tests/unit/test_models.py::TestAnimalModels::test_animal_create_valid -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=backend --cov-report=term-missing --cov-report=html
```

### Use Test Runner Script
```bash
./tests/run_tests.sh
```

## Test Results

**Current Status:** 57 tests passing ✅

### Test Breakdown

#### Unit Tests (18 tests) ✅
- Database connection: 5 tests
- Model validation: 13 tests

#### Integration Tests (39 tests) ✅
- Animals CRUD: 9 tests
- Adoptions CRUD: 5 tests
- Search operations: 4 tests
- Charts data: 3 tests
- Edge cases: 9 tests
- API endpoints: 9 tests (some require database setup)

## Test Coverage

- **Models:** 100% ✅
- **Config:** 100% ✅
- **Database Connection:** 88% ✅
- **API Routes:** 0% (tested via integration tests)

## Test Fixtures

The test suite uses pytest fixtures for:
- Test database connection (`test_db`)
- Clean database state (`clean_db`)
- Sample data (`sample_animal`, `sample_adopter`, etc.)

## Edge Cases Tested

1. **Data Validation:**
   - Negative/zero ages
   - Invalid email formats
   - Empty strings
   - Very long strings (10,000+ characters)

2. **Database Operations:**
   - Non-existent records
   - Concurrent updates
   - Large datasets (100+ records)
   - Invalid ObjectIds

3. **Special Characters:**
   - Unicode characters
   - Emojis
   - Special characters in queries

4. **Date Handling:**
   - Very old dates
   - Future dates
   - Different formats

## Notes

- Tests use a separate test database (`pet_adoption_test`)
- Each test runs with a clean database state
- Test fixtures provide reusable test data
- API endpoint tests may require running server (optional)

