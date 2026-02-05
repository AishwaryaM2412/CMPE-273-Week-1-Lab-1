from flask import Flask, request, jsonify
import time
import logging

SERVICE_NAME = "service-a"
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

@app.get("/echo")
def echo():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
