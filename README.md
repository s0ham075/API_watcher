# Status Monitor — Serverless & Event-Driven (Webhooks + RSS)

This project monitors service incidents (including the OpenAI Status Page) using a hybrid event-driven architecture:

- **Webhooks** → real-time push updates
- **RSS feeds** → efficient event-like checks (every 5 minutes)
- **AWS Serverless** → Lambda + EventBridge for zero maintenance and near-zero cost

Your deployed webhook URL (Lambda via API Gateway) is included below for testing.

## Architecture Overview

### 1. Webhook Path (Push Model)
- Providers send POST requests to API Gateway
- API Gateway triggers the Webhook Lambda
- Lambda logs the incident message

### 2. RSS Path (Scheduled Event Model)
- EventBridge runs the RSS Lambda every 5 minutes
- Lambda fetches lightweight RSS feeds
- Only new incident entries are logged

### 3. Shared Processor
Both Lambda functions use the same processor, producing consistent output:
```
[2025-11-03 14:32:00] Product: X Status: Y
```

## Why This Solution Fits the Requirements

The assignment required avoiding manual refreshing and inefficient polling, and supporting 100+ providers.

This design satisfies that by:
- **Webhooks** → true real-time, no polling
- **RSS** → efficient, low-frequency checks built for event updates
- **Serverless** → auto-scaling, low cost, no servers
- **Extensible** → add any number of RSS URLs or webhook endpoints

## Cost Analysis (All Within AWS Free Tier)

| Component | Usage | Free Tier | Cost |
|-----------|-------|-----------|------|
| RSS Lambda | 8,640 runs/month | 1,000,000 free | $0.00 |
| Webhook Lambda | ~20–100 events | 1,000,000 free | $0.00 |
| API Gateway (HTTP API) | Very low | 1,000,000 free | $0.00 |
| EventBridge Rule | 8,640 triggers | 100,000 free | $0.00 |
| CloudWatch Logs | Few MB | 5 GB free | $0.00 |

💰 **Total Monthly Cost: $0.00**

- Even with 20–30 RSS feeds → still free
- Even with 100+ feeds → under $1/month

## Webhook Test Endpoint

Your webhook Lambda is live for testing for 1 week:

```bash
curl -X POST "https://ly6jh680tk.execute-api.ap-southeast-2.amazonaws.com/default/openAI_api_watcher" ^
  -H "Content-Type: application/json" ^
  -d "{\"incident\":{\"name\":\"Curl Test\",\"incident_updates\":[{\"body\":\"Webhook via curl!\"}]}}"
```
