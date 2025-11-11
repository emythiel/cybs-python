# Microsoft Defender XDR API - Student Guide V2


## Continuous Incident Generation Version
Welcome to the Educational Cybersecurity API V2! This guide will help you connect to and use the API for
your course exam.


## API Information

**Base URL:** `http://BASE-URL-IP` (Replace with actual address)  
**API Version:** 2.0 (Continuous Generation)  
**Special Feature**: New security incidents are automatically generated every 2-60 minutes, simulating a real-world Security Operations Center (SOC) environment where threats are continuously detected.


## Getting Started

### Step 1: Get Your Access Token
Before you can access the API, you need to obtain your personal access token.

**curl Example:**
```bash
curl -X POST http://BASE-URL-IP/api/auth/token \ 
  -H "Content-Type: application/json" \ 
  -d '{"email":"your.email@student.edu"}'
```

**PowerShell Example:**
```powershell
$headers = @{"Content-Type"="application/json"}
$body = @{"email"="your.email@student.edu"} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://BASE-URL-IP/api/auth/token" -Method
POST -Headers $headers -Body $body
Write-Host "Your token: $($response.token)"
Write-Host "Expires in: $($response.expires_in_hours) hours"
```

**Response:**
```json
{
  "message": "Token retrieved successfully",
  "email": "your.email@student.edu",
  "token": "student-xxxxxxxxxxxxx",
  "expires_at": "2025-11-12T20:00:00+00:00",
  "expires_in_hours": 48.0,
  "instructions": "Use this token in Authorization header: Bearer <token>"
}
```

**Important:**
- Your token expires after **48 hours**
- Save your token securely
- If your token expires, simply request a new one using the same email


## Authentication

All API requests (except getting your token) require authentication using your token in the *Authorization*
header.

**Format:**
```
Authorization: Bearer your-token-here
```

**curl Example:**
```bash
curl -H "Authorization: Bearer student-xxxxxxxxxxxxx" \
  http://BASE-URL-IP/api/incidents
```

**PowerShell Example:**
```powershell
$headers = @{"Authorization"="Bearer student-xxxxxxxxxxxxx"}
$response = Invoke-RestMethod -Uri "http://BASE-URL-IP/api/incidents" -Headers
$headers
$response
```

## Available Endpoints

### 1. Get All Incidents
Retrieve a list of security incidents with optional pagination.

**Endpoint:** `GET /api/incidents`  
**Query Parameters:**
- `$top`
  - Number of results to return (max 100, default 10)
- `$skip`
  - Number of results to skip (for pagination)

**curl Examples:**
```bash
# Get first 10 incidents (default)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://BASE-URL-IP/api/incidents

# Get first 50 incidents
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://BASE-URL-IP/api/incidents?\$top=50"

# Pagination - skip first 20, get next 10
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://BASE-URL-IP/api/incidents?\$skip=20&\$top=10"
```

**PowerShell Examples:**
```powershell
$headers = @{"Authorization"="Bearer YOUR_TOKEN"}
$baseUrl = "http://BASE-URL-IP"

# Get first 10 incidents (default)
$response = Invoke-RestMethod -Uri "$baseUrl/api/incidents" -Headers $headers

# Get first 50 incidents
$response = Invoke-RestMethod -Uri "$baseUrl/api/incidents?`$top=50" -Headers $headers
Write-Host "Total incidents: $($response.'@odata.count')"
Write-Host "Returned: $($response.value.Count) incidents"

# Display incidents
foreach($incident in $response.value) {
    Write-Host "$($incident.incidentId): $($incident.incidentName)"
}

# Pagination - skip first 20, get next 10
$response = Invoke-RestMethod -Uri "$baseUrl/api/incidents?`$skip=20&`$top=10" -
Headers $headers
```

**Response Structure:**
```json
{
  "@odata.context": "https://api.security.microsoft.com/api/$metadata#Incidents",
  "@odata.count": 127,
  "value": [
    {
      "incidentId": "INC1001",
      "incidentName": "APT29 - Phishing Campaign",
      "createdTime": "2025-11-10T20:30:00Z",
      "lastUpdateTime": "2025-11-10T22:15:00Z",
      "status": "Active",
      "severity": "High",
      "classification": "TruePositive",
      "determination": "Phishing",
      "tags": ["APT29", "Emotet"],
      "alerts": [...],
      "impactedEntities": {
        "users": 5,
        "machines": 2,
        "mailboxes": 1
      },
      "threatFamily": "Emotet",
      "mitreTechniques": ["T1566.001", "T1204.002"],
      "summary": "Security incident involving APT29..."
    }
  ],
  "pagination": {
    "skip": 0,
    "top": 10,
    "returned": 10,
    "filtered_total": 127,
    "unfiltered_total": 127
  },
  "api_version": "2.0"
}
```
---
### 2. Get Specific Incident
Retrieve detailed information about a single incident.  
**Endpoint:** `GET /api/incidents/{incident_id}

**curl Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://BASE-URL-IP/api/incidents/INC1001
```

**PowerShell Example:**
```powershell
$headers = @{"Authorization"="Bearer YOUR_TOKEN"}
$incidentId = "INC1001"
$response = Invoke-RestMethod -Uri
"http://BASE-URL-IP/api/incidents/$incidentId" -Headers $headers

Write-Host "Incident: $($response.incidentName)"
Write-Host "Severity: $($response.severity)"
Write-Host "Status: $($response.status)"
Write-Host "Threat Actor: $($response.tags[0])"
Write-Host "Number of alerts: $($response.alerts.Count)"

# Examine alerts
foreach($alert in $response.alerts) {
    Write-Host "`nAlert: $($alert.title)"
    Write-Host " Severity: $($alert.severity)"
    Write-Host " Machine: $($alert.computerDnsName)"
    Write-Host " IPs: $($alert.entities.ips -join ', ')"
    Write-Host " Domains: $($alert.entities.domains -join ', ')"
}
```

**Response Structure:**
```json
{
  "incidentId": "INC1001",
  "incidentName": "APT29 - Phishing Campaign",
  "createdTime": "2025-11-10T20:30:00Z",
  "severity": "High",
  "status": "Active",
  "tags": ["APT29", "Emotet"],
  "alerts": [
    {
      "alertId": "ALT1001-0",
      "title": "Suspicious PowerShell execution detected",
      "category": "Malware",
      "severity": "High",
      "detectionSource": "Microsoft Defender for Endpoint",
      "machineId": "machine-42",
      "computerDnsName": "WORKSTATION-42.contoso.com",
      "entities": {
        "ips": ["192.168.1.100", "203.0.113.45"],
        "domains": ["malicious-domain.com"],
        "fileHashes": ["d41d8cd98f00b204e9800998ecf8427e"],
        "emails": ["user1@contoso.com"],
        "processes": ["powershell.exe"]
      }
    }
  ],
  "mitreTechniques": ["T1566.001", "T1204.002"]
}
```
---
## Rate Limits
The API enforces rate limits:
- **50 requests per minute**
- **1500 requests per hour**  
If you exceed these limits, you'll receive a `401 Unauthorized` response.

**Best Practice - Add delays:**
```python
# Wait 5 minutes between requests
time.sleep(300)
```

## Understanding the Data

### Incident Structure
Each incident contains:
- **incidentId**: Unique identifier (e.g., "INC1001")
- **incidentName**: Descriptive name combining threat actor and attack type
- **createdTime**: When the incident was first detected (ISO 8601 format)
- **lastUpdateTime**: When the incident was last updated
- **severity**: Low, Medium, High, or Critical
- **status**: Active, InProgress, or Resolved
- **classification**: TruePositive, FalsePositive, or InformationalExpectedActivity
- **determination**: Type of threat (e.g., Malware, Phishing, MultiStagedAttack)
- **tags**: Array containing threat actor and malware family names
- **alerts**: Array of related security alerts (see Alert Structure below)
- **impactedEntities**: Count of affected users, machines, and mailboxes
- **threatFamily**: Name of the malware family involved
- **mitreTechniques**: Array of MITRE ATT&CK technique IDs
- **summary**: Text description of the incident

### Alert Structure
Each alert within an incident contains:
- **alertId**: Unique alert identifier
- **title**: Descriptive alert title
- **category**: Type of threat (Malware, Phishing, Lateral Movement, etc.)
- **severity**: Alert severity level (Low, Medium, High, Critical)
- **detectionSource**: Microsoft product that detected the alert
- **machineId**: Identifier of the affected machine
- **computerDnsName**: DNS name of the affected machine
- **entities**: Object containing Indicators of Compromise (IOCs):
  - **ips**: Array of IP addresses
  - **domains**: Array of domain names
  - **fileHashes**: Array of file hash values
  - **emails**: Array of email addresses
  - **processes**: Array of process names
- **firstActivity**: Timestamp of first observed activity
- **lastActivity**: Timestamp of last observed activity


## What's New in V2?

### Continuous Incident Generation
Unlike V1 which had a fixed set of 200 incidents, V2 continuously generates new incidents:
- **Startup**: Begins with 25 initial incidents
- **Background Generation**: 1-3 new incidents created every 2-60 minutes
- **Growth Rate**: Approximately 40-60 new incidents per day
- **Course Duration**: Expected to reach 2,600-2,800 incidents over 4 weeks

**Why is this important?**
- Simulates a real Security Operations Center where threats appear continuously
- Allows you to practice monitoring for new threats over time
- Enables time-based analysis and trending
- More realistic incident response scenarios


## Common Issues

- ### Issue: "Invalid or expired token"
  - **Solution:** Request a new token using your email address.
- ### Issue: "Rate limit exceeded"
  - **Solution:** Add delays between requests
- ### Issue: "No new incidents appearing
  - **Solution:** V2 generates incidents every 2-60 minutes randomly. The background generation is automatic. Check back later or use the summary endpoint to see current total.
