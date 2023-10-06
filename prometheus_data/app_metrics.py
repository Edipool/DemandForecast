from prometheus_client import Counter, Gauge, Histogram

predict_request_counter = Counter(
    "http_predict_request_total",
    "Total HTTP Predict Requests",
)
predict_request_latency = Histogram(
    "http_predict_request_latency_seconds",
    "HTTP Predict Request Latency",
)
predict_request_gauge = Gauge(
    "http_predict_request_gauge",
    "HTTP Predict Request Gauge",
)

how_much_to_order_request_count = Counter(
    "how_much_to_order_requests_total",
    "Total requests to /api/how_much_to_order",
)
how_much_to_order_successful_requests = Counter(
    "how_much_to_order_successful_requests_total",
    "Total successful requests to /api/how_much_to_order",
)
how_much_to_order_failed_requests = Counter(
    "how_much_to_order_failed_requests_total",
    "Total failed requests to /api/how_much_to_order",
)
how_much_to_order_response_time = Histogram(
    "how_much_to_order_response_seconds",
    "Histogram of response times for /api/how_much_to_order",
)
