# Python HTTP Track

# CMPE 273 – Week 1 Lab 1
## Tiny Distributed System (Python – Flask)

This project demonstrates a simple locally distributed system with two independent services communicating over HTTP.

---

## Services

### Service A (Echo API)
- Runs on: `http://127.0.0.1:8080`
- Endpoints:
  - `GET /health` → `{ "status": "ok" }`
  - `GET /echo?msg=hello` → `{ "echo": "hello" }`

### Service B (Client)
- Runs on: `http://127.0.0.1:8081`
- Endpoints:
  - `GET /health` → `{ "status": "ok" }`
  - `GET /call-echo?msg=hello`
    - Calls Service A `/echo`
    - Returns combined response
    - Uses timeout and handles failure

---

## How to Run Locally

### Prerequisites
- Python 3.10+
- Git

### Setup
```bash
git clone <your-repo-url>
cd python-http
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Run Service A
```bash
cd service-a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Run Service B (new terminal)
```bash
cd service-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Test
```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```

Stop Service A and rerun the curl command to observe failure handling.


