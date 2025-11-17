# processor.py
from datetime import datetime

def log_event(product, message):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] Product: {product}\nStatus: {message}\n")
