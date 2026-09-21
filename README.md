# SmartNet Monitor

**Network and Application Service Monitoring System**

SmartNet Monitor is a Python/Flask-based academic project that demonstrates practical monitoring concepts from the **Transport Layer** and **Application Layer** of Computer Networks.

It provides a web dashboard for checking selected network/application services, measuring response time, recording monitoring results in SQLite, and displaying historical results.

> **Academic project:** Use this application only against systems and services you are authorized to monitor. Do not commit credentials, API keys, SNMP community strings, or private monitoring data.

## Features

- DNS resolution monitoring
- TCP connectivity monitoring
- UDP request/response monitoring
- TCP probe latency and service-level availability measurements
- HTTP/HTTPS monitoring
- SMTP service connectivity monitoring
- FTP service connectivity monitoring
- SNMP monitoring
- SQLite result history
- Dashboard summary statistics
- Response-time chart
- Browser-based periodic TCP monitoring
- Error handling for invalid input and unavailable services

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Network APIs | Python `socket`, `smtplib`/network libraries, `ftplib` |
| HTTP | `requests` |
| SNMP | `pysnmp` |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |

## Repository Structure

```text
SmartNet-Monitor/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── modules/
│   ├── __init__.py
│   ├── dns_monitor.py
│   ├── tcp_monitor.py
│   ├── udp_monitor.py
│   ├── qos_monitor.py
│   ├── http_monitor.py
│   ├── smtp_monitor.py
│   ├── ftp_monitor.py
│   └── snmp_monitor.py
│
├── database/
│   └── database.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── screenshots/
    └── .gitkeep
```

The SQLite database is created locally at runtime and is ignored by Git.

## Requirements

- Python 3.10 or newer recommended
- Internet/network access for tests against external services
- An authorized SMTP/FTP/SNMP service if those modules are tested

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SmartNet-Monitor.git
cd SmartNet-Monitor
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open the dashboard in a browser:

```text
http://127.0.0.1:5000
```

## Quick API Tests

After starting Flask, these endpoints can be tested from a browser or API client.

### Health

```text
http://127.0.0.1:5000/api/health
```

### DNS

```text
http://127.0.0.1:5000/api/dns?hostname=example.com
```

### TCP

```text
http://127.0.0.1:5000/api/tcp?host=HOST&port=PORT
```

### UDP

```text
http://127.0.0.1:5000/api/udp?host=HOST&port=PORT
```

### QoS / TCP probes

```text
http://127.0.0.1:5000/api/qos?host=HOST&port=PORT&count=5
```

### HTTP

```text
http://127.0.0.1:5000/api/http?url=https://example.com
```

### SMTP

```text
http://127.0.0.1:5000/api/smtp?host=HOST&port=587
```

### FTP

```text
http://127.0.0.1:5000/api/ftp?host=HOST&port=21
```

### SNMP

```text
http://127.0.0.1:5000/api/snmp?host=HOST&port=161&community=YOUR_COMMUNITY
```

### History

```text
http://127.0.0.1:5000/api/history
```

### Summary

```text
http://127.0.0.1:5000/api/summary
```

## Testing Notes

### DNS

A valid hostname should resolve to an IP address. An invalid hostname should return a controlled error.

### TCP

Use a TCP service that you are authorized to test. A successful connection indicates that the target TCP service accepted the connection.

### UDP

A UDP timeout only means that no response was received within the configured timeout. It does **not** by itself prove that the destination network is unavailable.

### QoS

The current QoS module uses repeated TCP connection probes. Its failure percentage should therefore be described as **TCP probe failure rate/service-level probe loss**, not raw IP packet loss.

### HTTP

An HTTP status such as 404 still demonstrates that an HTTP server responded. HTTP response status and network reachability are separate concepts.

### SMTP/FTP

These modules check service connectivity/greetings. They do not send email or modify FTP files.

### SNMP

SNMP requires an SNMP-enabled device or test agent. Use only authorized devices and never commit real community strings or credentials.

## Screenshots

Place project screenshots in `screenshots/`. Suggested files:

```text
screenshots/
├── dashboard.png
├── dns-success.png
├── tcp-success.png
├── qos-result.png
├── http-result.png
├── smtp-result.png
├── ftp-result.png
├── snmp-result.png
├── monitoring-history.png
└── response-chart.png
```

Do not commit screenshots containing private IP addresses, credentials, tokens, passwords, or other sensitive information.

## Testing Checklist

- [ ] Flask application starts successfully
- [ ] Dashboard loads
- [ ] `/api/health` returns OK
- [ ] DNS success and failure cases tested
- [ ] TCP success and failure cases tested
- [ ] UDP response/timeout behavior tested
- [ ] QoS/TCP probe statistics generated
- [ ] HTTP success/error cases tested
- [ ] SMTP service tested if authorized
- [ ] FTP service tested if authorized
- [ ] SNMP tested with an authorized SNMP agent, or limitation documented
- [ ] SQLite history verified
- [ ] Summary statistics verified
- [ ] Response-time chart verified
- [ ] Automatic monitoring verified

## Academic Project Documentation

The project can be documented using the following chapters:

1. Introduction
2. Literature Survey
3. System Analysis
4. Requirements Specification
5. System Design
6. Implementation
7. Testing and Results
8. Conclusion and Future Enhancements

All numerical results in the final report should come from actual tests performed on the final version of the application.

## Limitations

- Automatic monitoring is browser-based and stops when the page is closed.
- UDP results depend on whether the target service responds to the test datagram.
- SNMP testing requires a suitable SNMP agent/device.
- External service availability can depend on firewalls, NAT, DNS, provider policies, and local network configuration.

## Future Enhancements

- Server-side scheduled monitoring
- User authentication and role-based access
- SNMPv3 support with secure credentials
- Alerting by email/webhook
- More detailed QoS metrics
- Export reports to CSV/PDF
- Docker deployment
- Production WSGI server configuration

## Git Commands

After creating your GitHub repository:

```bash
git init
git add .
git commit -m "Initial SmartNet Monitor project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/SmartNet-Monitor.git
git push -u origin main
```

For later updates:

```bash
git add .
git commit -m "Update monitoring dashboard"
git push
```

## License

For an academic submission, add the license required by your institution. If you do not intend to grant reuse rights yet, you can omit a license file and retain the repository's copyright under your name/institution.
