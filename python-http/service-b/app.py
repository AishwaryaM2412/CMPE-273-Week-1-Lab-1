from flask import Flask, request, jsonify
import time
import logging
import requests

SERVICE_NAME = "service-b"
SERVICE_A_BASE = "http://127.0.0.1:8080"
SERVICE_A_TIMEOUT = (0.5, 1.0)  # (connect timeout, read timeout)

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

@app.before_request
def start_timer():
    request._start_time = time.perf_counter()

@app.after_request
def log_request(response):
    elapsed_ms = (time.perf_counter() - request._start_time) * 1000
    logging.info(
        "service=%s method=%s path=%s status=%s latency_ms=%.2f",
        SERVICE_NAME,
        request.method,
        request.path,
        response.status_code,
        elapsed_ms,
    )
    return response

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/call-echo")
def call_echo():
    msg = request.args.get("msg", "")
    try:
        r = requests.get(
            f"{SERVICE_A_BASE}/echo",
            params={"msg": msg},
            timeout=SERVICE_A_TIMEOUT
        )
        r.raise_for_status()
        return jsonify(service_b="ok", service_a=r.json()), 200

    except (requests.Timeout, requests.ConnectionError) as e:
        logging.error("service=%s error=service_a_unavailable detail=%s", SERVICE_NAME, str(e))
        return jsonify(error="Service A unavailable", detail=str(e)), 503

    except requests.HTTPError as e:
        logging.error("service=%s error=service_a_http_error detail=%s", SERVICE_NAME, str(e))
        return jsonify(error="Service A returned error", detail=str(e)), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=False)