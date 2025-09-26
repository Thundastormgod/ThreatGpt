# ThreatGPT API Usage Guide

This guide demonstrates how to use the ThreatGPT API for direct threat content generation and simulation management.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for local development. For production deployments, proper authentication should be implemented.

## Core Endpoints

### 1. Health Check

Check the API status and component health.

```bash
curl -X GET "http://localhost:8000/health"
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-26T10:30:00Z",
  "version": "0.1.0",
  "components": {
    "api": "healthy",
    "simulator": "healthy",
    "llm_manager": "healthy"
  }
}
```

### 2. Direct Content Generation

Generate threat simulation content directly using LLM providers.

```bash
curl -X POST "http://localhost:8000/llm/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Create a realistic phishing email targeting IT administrators",
       "scenario_type": "phishing",
       "max_tokens": 500,
       "temperature": 0.7
     }'
```

Response:
```json
{
  "content": "Generated phishing email content...",
  "provider_used": "openai",
  "tokens_used": 245,
  "generation_time_seconds": 2.3,
  "safety_score": 0.95,
  "metadata": {
    "scenario_type": "phishing",
    "validated": true
  }
}
```

### 3. Scenario Management

Create and manage threat scenarios.

#### Create Scenario
```bash
curl -X POST "http://localhost:8000/scenarios" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Advanced Phishing Campaign",
       "threat_type": "phishing",
       "description": "Sophisticated email-based attack targeting executives",
       "severity": "high",
       "target_systems": ["email", "workstation"],
       "attack_vectors": ["social_engineering", "credential_harvesting"]
     }'
```

Response:
```json
{
  "scenario_id": "abc123-def456-ghi789",
  "name": "Advanced Phishing Campaign",
  "threat_type": "phishing",
  "description": "Sophisticated email-based attack targeting executives",
  "severity": "high",
  "target_systems": ["email", "workstation"],
  "attack_vectors": ["social_engineering", "credential_harvesting"],
  "created_at": "2025-09-26T10:30:00Z",
  "metadata": {}
}
```

### 4. Simulation Execution

Execute threat simulations based on scenarios.

```bash
curl -X POST "http://localhost:8000/simulations" \
     -H "Content-Type: application/json" \
     -d '{
       "scenario_id": "abc123-def456-ghi789",
       "max_stages": 7
     }'
```

Response:
```json
{
  "message": "Simulation executed successfully",
  "result_id": "sim-xyz789-abc123",
  "status": "completed",
  "stages_completed": 7,
  "success_rate": 0.86,
  "duration_seconds": 12.5
}
```

### 5. LLM Provider Management

#### List Available Providers
```bash
curl -X GET "http://localhost:8000/llm/providers"
```

Response:
```json
{
  "providers": ["openai", "anthropic"],
  "default_provider": "openai",
  "total_providers": 2
}
```

#### Check LLM Status
```bash
curl -X GET "http://localhost:8000/llm/status"
```

Response:
```json
{
  "llm_manager": "operational",
  "available_providers": ["openai", "anthropic"],
  "status": "ready"
}
```

### 6. Active Simulations

Monitor currently running simulations.

```bash
curl -X GET "http://localhost:8000/simulations/active"
```

Response:
```json
{
  "active_simulations": 2,
  "simulations": [
    {
      "result_id": "sim-123",
      "status": "running",
      "scenario_id": "scenario-456",
      "stages_completed": 3,
      "start_time": "2025-09-26T10:25:00Z"
    }
  ]
}
```

## Content Generation Parameters

### Scenario Types
- `phishing` - Email-based phishing attacks
- `malware` - Malware-related threats
- `social_engineering` - Social engineering attacks
- `network_intrusion` - Network-based attacks
- `custom` - Custom threat scenarios

### Temperature Settings
- `0.1-0.3` - More focused, deterministic output
- `0.4-0.7` - Balanced creativity and consistency
- `0.8-1.0` - More creative, varied output

### Max Tokens
- `100-500` - Short content (SMS, brief emails)
- `500-1000` - Medium content (full emails, scripts)
- `1000-2000` - Long content (detailed scenarios)

## Error Handling

All endpoints return structured error responses:

```json
{
  "error": "Error description",
  "status_code": 400,
  "timestamp": "2025-09-26T10:30:00Z"
}
```

Common status codes:
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

Currently no rate limiting is implemented. For production use, implement appropriate rate limiting based on your requirements.

## Security Considerations

1. **Authentication**: Implement authentication for production use
2. **Input Validation**: All inputs are validated via Pydantic models
3. **Content Safety**: Generated content goes through safety validation
4. **Logging**: All API calls are logged for audit purposes

## Python Client Usage

```python
import requests

# Generate content
response = requests.post(
    "http://localhost:8000/llm/generate",
    json={
        "prompt": "Create a spear phishing email targeting finance team",
        "scenario_type": "phishing",
        "max_tokens": 800
    }
)

content = response.json()
print(content["content"])
```

## Starting the API Server

```bash
# Development server
uvicorn threatgpt.api.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn threatgpt.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Interactive API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc