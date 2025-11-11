# Exam Project Requirements - Programming

## Project Overview

Type: Individual or group (up to 4 students)

Submission Date: 5. December, 2025

Submission: ZIP file + report via WISEflow

Exam Format: 30 minutes:
- 5 minutes presentation
- 20 minutes live coding and Q&A
- 5 minutes evaluation


## Context

The security company SECO continues to face security challenges.  
Building on your work from Mandatory Task 1 and 2, you are now tasked with developing a comprehensive threat analysis system using the live event API.

Important: The API now generates events continuously. If accessed after one month, there could be around 2000+ events in the system.  
Your program must efficiently handle large datasets.


## Program Requirements

1. **API Integration**
    - Connect to the event API and retrieve authentication token
    - Implement proper token handling (storage/renewal)
    - Handle large datasets (2000+ events) efficiently via pagination
    - Use appropriate HTTP methods with correct headers
    - Implement retry logic for failed requests
2. **Data Processing**
    - Parse JSON event data into Python objects
    - Extract and categorize Indicators of Compromise (IOCs)
    - Handle missing or malformed data gracefully
3. **Database Storage**
    - Design and implement an SQLite database
    - Store events with proper relationships between tables
    - Minimum recommended schema:
        - Incidents table: `incidentId`, `incidentName`, `severity`, `status`, `createdTime`
        - Alerts table: `alertId`, `incidentId`, `machineId`, `detectionSource`, `firstActivity`
        - IOCs (entities) table: `incidentId`, `type` (e.g., `domains`, `emails`, `fileHashes`, `ips`,
       `processes`, etc.), `value`
    - Implement proper database connections and transactions
    - Handle duplicates correctly
4. **Error Handling**
    - Validate all API responses
    - Handle network errors and timeouts
    - Manage rate limiting (50 requests/min, 1500/hour)
    - Validate data before inserting into the database
    - Implement proper exception handling
    - Implement basic logging (write to file or use logging module)
    - Log errors, warnings, and important operations
5. **Code Quality**
    - Follow PEP8 conventions
    - Include comprehensive documentation:
        - Function docstrings
        - Inline comments for complex logic
        - Organize code into logical functions
        - Use meaningful variable and function names
        - If AI is used for documentation, it must be clearly marked


## Technical Requirements

Required Python modules:
- requests – API communication
- json – JSON parsing
- sqlite3 – Database operations
- datetime – Timestamp handling

Recommended additional modules:
- logging – Logging
- time – Rate limiting/delays

## Deliverables

1. **Source Code**
    - Well-organized Python files
    - Configuration file for API settings (no hardcoded tokens)
    - Script for creating the database
2. **Written Report (max. 5 pages)**
    - Problem analysis
    - Design decisions and justifications
    - Challenges and solutions
    - Future improvements

## Presentation (5 minutes)

Choose to present:
- System architecture and design
- Live demonstration of program functionality
- Technical challenges and solutions
- Data analysis and insights
- Review of critical code sections
- Suggestions for future improvements

Important: When fetching 2000 events with 100 per request:
- Requires 20 API calls
- Takes about 24–30 seconds (with rate limiting)
- Plan your implementation accordingly
- Remember: We do not want duplicates in the database

## Security Considerations
- Never hardcode API tokens in source code
- Use environment variables or configuration files
- Implement proper error messages without revealing sensitive information
- Handle API credentials securely

## Resources

- API Documentation: [API_GUIDE.md](./API_GUIDE.md)
- Python Documentation: https://docs.python.org/3/
- SQLite Documentation: https://docs.python.org/3/library/sqlite3.html
- Requests Library: https://requests.readthedocs.io/
- PEP8 Style Guide: https://pep8.org/
