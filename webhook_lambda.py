# webhook_lambda.py
import json
from processor import log_event

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    if "incident" in body:
        inc = body["incident"]
        product = inc.get("name", "Unknown Incident")
        updates = inc.get("incident_updates", [])
        message = updates[-1].get("body", "No message") if updates else "No message"
        log_event(product, message)
        return {"statusCode": 200}

    if "component" in body:
        comp = body["component"]
        product = comp.get("name", "Unknown Component")
        message = comp.get("status", "Updated")
        log_event(product, message)
        return {"statusCode": 200}

    # fallback
    log_event("Unknown", str(body))
    return {"statusCode": 200}
