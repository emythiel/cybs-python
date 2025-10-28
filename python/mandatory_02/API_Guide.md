# Microsoft Defender XDR API - Student Guide 🎓

## 🌐 API Access Information

**Base URL:** [http://BASE-URL-IP](http://BASE-URL-IP)

This is an educational simulation of the Microsoft Defender XDR Incidents API designed for cybersecurity
learning exercises.

## 🔑 Getting Started

### Step 1: Get Your Access Token

Before using any API endpoints, you need to obtain an access token using your university email address.

**Endpoint:** POST /api/auth/token

**Request:**

```
curl -X POST http://BASE-URL-IP/api/auth/token \
-H "Content-Type: application/json" \
-d '{"email": "your-email@university.edu"}'
```
**Response:**

#### {

```
"message": "Token retrieved successfully",
"email": "your-email@university.edu",
"token": "student-Ab3dX9kL2mN8pQ5r",
"expires_at": "2025-10-20T16:30:00Z",
"expires_in_hours": 47.8,
"instructions": "Use this token in Authorization header: Bearer <token>",
"note": "Token will expire in 47.8 hours. Request a new token if it expires."
}
```
⚠ **Important:** Save your token! You'll need it for all API requests.

### Step 2: Use Your Token

Include your token in the Authorization header for all API requests:

```
Authorization: Bearer student-Ab3dX9kL2mN8pQ5r
```
## 📊 Available Endpoints


### 1. List Security Incidents

Get a list of security incidents for analysis.

**Endpoint:** GET /api/incidents

**Basic Request:**

```
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents"
```
**With Filters:**

```
# Get high severity incidents
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?severity=High"
```
```
# Get active incidents
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?status=Active"
```
```
# Get incidents from specific threat actor
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?threat_actor=APT29"
```
**Pagination (OData Style):**

```
# Get first 10 incidents
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?\$top=10"
```
```
# Skip first 10, get next 10
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?\$skip=10&\$top=10"
```
```
# Maximum 100 incidents per request
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents?\$top=100"
```
**Response Format:**

#### {

```
"@odata.context": "https://api.security.microsoft.com/api/$metadata#Incidents",
"@odata.count": 45 ,
"value": [
{
```

```
"incidentId": "INC1001",
"incidentName": "APT29 - Phishing Campaign",
"createdTime": "2025-10-15T10:30:00Z",
"severity": "High",
"status": "Active",
"classification": "TruePositive",
"determination": "Phishing",
"tags": ["APT29", "Emotet"],
"alerts": [...],
"summary": "Security incident involving APT29 with 3 alerts..."
}
],
"@odata.nextLink": "/api/incidents?$skip=10&$top=10",
"pagination": {
"skip": 0 ,
"top": 10 ,
"returned": 10 ,
"filtered_total": 45 ,
"unfiltered_total": 200
}
}
```
### 2. Get Specific Incident Details

Get detailed information about a specific incident.

**Endpoint:** GET /api/incidents/{incident-id}

**Request:**

```
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents/INC1001"
```
**Response:** Full incident details including all alerts, IOCs, and analysis information.

### 3. Get Incident Statistics

Get summary statistics for dashboard creation and analysis.

**Endpoint:** GET /api/incidents/summary

**Request:**

```
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/incidents/summary"
```
**Response:**


#### {

```
"total_incidents": 200 ,
"by_severity": {
"Critical": 15 ,
"High": 45 ,
"Medium": 89 ,
"Low": 51
},
"by_status": {
"Active": 67 ,
"InProgress": 45 ,
"Resolved": 88
},
"top_threat_actors": {
"APT29": 23 ,
"APT28": 18 ,
"Lazarus Group": 15
},
"recent_incidents": 34
}
```
### 4. Extract All IOCs (Indicators of Compromise)

Get all IOCs from incidents for threat intelligence analysis.

**Endpoint:** GET /api/iocs

**Request:**

```
curl -H "Authorization: Bearer your-token-here" \
"http://BASE-URL-IP/api/iocs"
```
**Response:**

#### {

```
"indicators_of_compromise": {
"ip_addresses": [
"192.168.1.100",
"203.0.113.45",
"185.220.100.240"
],
"domains": [
"malicious-domain.com",
"phishing-site.net",
"command-control.xyz"
],
"file_hashes": [
"d41d8cd98f00b204e9800998ecf8427e",
"5d41402abc4b2a76b9719d911017c592"
```

#### ],

```
"email_addresses": [
"suspicious@external.com",
"noreply@phishing.net"
],
"processes": [
"powershell.exe",
"cmd.exe",
"rundll32.exe"
]
},
"total_unique_iocs": 156
}
```
## ⚡ Rate Limits

To ensure fair usage for all students:

```
50 requests per minute per student
1500 requests per hour per student
Maximum 100 incidents per API call
```
If you exceed these limits, you'll receive a rate limit error. Wait a moment and try again.

## 🔒 Token Management

### Token Expiration

```
Tokens expire after 48 hours
You'll receive a new token automatically when requesting with an expired token
Always check the expires_in_hours field in responses
```
### Getting a New Token

If your token expires, simply request a new one using the same email:

```
curl -X POST http://BASE-URL-IP/api/auth/token \
-H "Content-Type: application/json" \
-d '{"email": "your-email@university.edu"}'
```
## 🎯 Learning Exercises

### Exercise 1: Incident Analysis Dashboard

Create a dashboard showing:

```
Total incidents by severity
Active vs resolved incidents
Top threat actors
```

```
Recent activity trends
```
### Exercise 2: IOC Extraction and Analysis

```
1. Extract all IOCs from the API
2. Categorize them by type (IPs, domains, hashes, etc.)
3. Create a threat intelligence report
4. Map IOCs to specific threat actors
```
### Exercise 3: Threat Actor Profiling

```
1. Filter incidents by specific threat actors
2. Analyze their tactics, techniques, and procedures (TTPs)
3. Identify common IOCs used by each group
4. Create threat actor profiles
```
### Exercise 4: Incident Response Workflow

```
1. List all active incidents
2. Prioritize by severity and impact
3. Extract relevant IOCs for blocking
4. Create incident response playbooks
```
## 💡 Best Practices

### 1. Efficient API Usage

```
# Good: Use pagination for large datasets
curl "http://BASE-URL-IP/api/incidents?\$top=50"
```
```
# Good: Use filters to get specific data
curl "http://BASE-URL-IP/api/incidents?severity=Critical&status=Active"
```
```
# Avoid: Requesting all data at once without filters
```
### 2. Token Security

```
Never share your token with other students
Don't include tokens in version control or public code
Store tokens securely in environment variables
```
### 3. Error Handling

Always check for errors in responses:

#### {

```
"error": "Invalid or expired token. Get your token at /api/auth/token"
}
```

### 4. Data Analysis Tips

```
Use the summary endpoint for overview statistics
Combine multiple API calls to build comprehensive analysis
Cache data locally to reduce API calls during development
```
## ❓ Common Issues & Solutions

### "Authorization header required"

**Problem:** Missing or incorrect Authorization header **Solution:** Include Authorization: Bearer your-
token-here in all requests

### "Invalid or expired token"

**Problem:** Token has expired (after 48 hours) **Solution:** Request a new token using your email

### "Rate limit exceeded"

**Problem:** Too many requests in a short time **Solution:** Wait 1 minute and try again, or reduce request
frequency

### "Email not found in course database"

**Problem:** Your email hasn't been added to the course **Solution:** Contact your instructor to be added to the
system

## 📱 Example: Python Script

Here's a simple Python example to get you started:

```
import requests
import json
```
```
# Configuration
API_BASE = "http://BASE-URL-IP"
EMAIL = "your-email@university.edu"
```
```
# Get token
def get_token():
response = requests.post(f"{API_BASE}/api/auth/token",
json={"email": EMAIL})
return response.json()["token"]
```
```
# Get incidents
def get_incidents(token, severity=None, limit= 10 ):
headers = {"Authorization": f"Bearer {token}"}
params = {"$top": limit}
if severity:
params["severity"] = severity
```

```
response = requests.get(f"{API_BASE}/api/incidents",
headers=headers, params=params)
return response.json()
```
```
# Main execution
if __name__ == "__main__":
# Get your token
token = get_token()
print(f"Token obtained: {token[: 20 ]}...")
```
```
# Get critical incidents
incidents = get_incidents(token, severity="Critical", limit= 5 )
print(f"Found {len(incidents['value'])} critical incidents")
```
```
# Print incident names
for incident in incidents['value']:
print(f"- {incident['incidentId']}: {incident['incidentName']}")
```
## 🏆 Assessment Tips

```
1. Document your API calls - Keep track of which endpoints you use
2. Show your analysis process - Explain how you filtered and processed data
3. Include visualizations - Charts and graphs help demonstrate understanding
4. Cite specific incidents - Use real incident IDs and data from the API
5. Demonstrate IOC extraction - Show you can identify and categorize threats
```
## 📞 Need Help?

```
Check this guide for common solutions
Review the error message in API responses
Contact your instructor if you can't access the system
Work with classmates to troubleshoot technical issues
```
**Happy threat hunting!** 🔍🛡
