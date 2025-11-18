# Charts Parameters & Data Requirements

## Monthly Adoptions Chart

### Parameters
- **Endpoint**: `/api/charts/adoptions`
- **Method**: GET
- **Query Parameters**:
  - `start_date` (optional): Start date filter in `YYYY-MM-DD` format (e.g., `2024-01-01`)
  - `end_date` (optional): End date filter in `YYYY-MM-DD` format (e.g., `2024-12-31`)

### Data Requirements
- **Source Collection**: `adoptions`
- **Required Field**: `adoption_date` (must be in `YYYY-MM-DD` format)
- **Data Processing**:
  - Groups adoptions by year-month (format: `YYYY-MM`)
  - Counts adoptions per month
  - Applies date range filters if provided

### Response Format
```json
{
  "labels": ["2024-01", "2024-02", "2024-03"],
  "data": [5, 8, 12],
  "metadata": {
    "total_adoptions": 25,
    "valid_dates": 25,
    "invalid_dates": 0,
    "filtered_count": 25,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }
}
```

### Common Issues
1. **No data displayed**: 
   - Check if adoptions have `adoption_date` field
   - Verify date format is `YYYY-MM-DD`
   - Check for invalid date formats in database

2. **Empty chart**:
   - No adoption records exist
   - All dates are invalid format
   - Date filters exclude all records

---

## Medical Visits Over Time Chart

### Parameters
- **Endpoint**: `/api/charts/medical-visits`
- **Method**: GET
- **Query Parameters**:
  - `start_date` (optional): Start date filter in `YYYY-MM-DD` format (e.g., `2024-01-01`)
  - `end_date` (optional): End date filter in `YYYY-MM-DD` format (e.g., `2024-12-31`)

### Data Requirements
- **Source Collection**: `medical_records`
- **Required Field**: `visit_date` (must be in `YYYY-MM-DD` format)
- **Data Processing**:
  - Groups medical visits by year-month (format: `YYYY-MM`)
  - Counts visits per month
  - Applies date range filters if provided

### Response Format
```json
{
  "labels": ["2024-01", "2024-02", "2024-03"],
  "data": [3, 7, 5],
  "metadata": {
    "total_records": 15,
    "valid_dates": 15,
    "invalid_dates": 0,
    "filtered_count": 15,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }
}
```

### Common Issues
1. **No data displayed**:
   - Check if medical records have `visit_date` field
   - Verify date format is `YYYY-MM-DD`
   - Check for invalid date formats in database

2. **Empty chart**:
   - No medical records exist
   - All dates are invalid format
   - Date filters exclude all records

---

## Date Format Requirements

### Required Format
- **Format**: `YYYY-MM-DD`
- **Examples**:
  - ✅ Valid: `2024-01-15`
  - ✅ Valid: `2024-12-31`
  - ❌ Invalid: `01/15/2024`
  - ❌ Invalid: `15-01-2024`
  - ❌ Invalid: `2024/01/15`

### How Dates Are Processed
1. Dates are parsed using Python's `datetime.strptime(date_string, '%Y-%m-%d')`
2. Invalid dates are logged and skipped
3. Valid dates are grouped by year-month (`YYYY-MM` format)
4. Monthly counts are aggregated

---

## Troubleshooting

### Chart Shows "No Data Available"

**Check the metadata in the response:**
- `total_adoptions` / `total_records`: Total records in database
- `valid_dates`: Number of records with valid date format
- `invalid_dates`: Number of records with invalid date format

**Solutions:**
1. **If `total_adoptions`/`total_records` is 0**: No data exists - add adoption/medical records
2. **If `valid_dates` is 0**: All dates are invalid format - fix date formats in database
3. **If `filtered_count` is 0**: Date filters exclude all records - adjust filter dates

### Fixing Invalid Dates

**For Adoptions:**
```python
# Update adoption dates to correct format
db.adoptions.update_many(
    {},
    [{"$set": {"adoption_date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$adoption_date"}}}}]
)
```

**For Medical Records:**
```python
# Update visit dates to correct format
db.medical_records.update_many(
    {},
    [{"$set": {"visit_date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$visit_date"}}}}]
)
```

---

## Example API Calls

### Monthly Adoptions (All Time)
```
GET /api/charts/adoptions
```

### Monthly Adoptions (Date Range)
```
GET /api/charts/adoptions?start_date=2024-01-01&end_date=2024-12-31
```

### Medical Visits (All Time)
```
GET /api/charts/medical-visits
```

### Medical Visits (Date Range)
```
GET /api/charts/medical-visits?start_date=2024-01-01&end_date=2024-12-31
```

---

## Frontend Filtering

The charts page includes date filters that can be applied:
- **Start Date**: Filters data from this date onwards
- **End Date**: Filters data up to this date
- Both filters use `YYYY-MM-DD` format
- Filters are applied when clicking "Apply Filters" button

---

## Recent Fixes

1. ✅ Added error handling for empty data
2. ✅ Added metadata to API responses (total records, valid/invalid dates)
3. ✅ Added informative messages when no data is available
4. ✅ Improved date parsing with better error handling
5. ✅ Added debugging information (invalid dates are logged)
6. ✅ Charts now show helpful messages instead of blank canvas

