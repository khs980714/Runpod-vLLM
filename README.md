# vllm-runpod-serverless

RunPod Serverless worker that exposes a **vLLM AsyncEngine** as an OpenAI-compatible API.

## Features

| Feature | Detail |
|---------|--------|
| Base image | `runpod/base` (CUDA 12.1) |
| Inference backend | vLLM `AsyncLLMEngine` |
| API compatibility | OpenAI `/chat/completions`, `/completions`, `/models` |
| Model types | `public`, `gated`, `custom` |

---

## Model Types

| `MODEL_TYPE` | Description |
|---|---|
| `public` | Any HuggingFace public model (e.g. `facebook/opt-125m`) |
| `gated` | HF gated / private model — requires `HF_TOKEN` |
| `custom` | Fine-tuned model stored on the pod volume (e.g. `/runpod-volume/my-model`) |

---

## Environment Variables

Copy `.env.example` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `MODEL_TYPE` | `public` | `public` \| `gated` \| `custom` |
| `MODEL_NAME` | `facebook/opt-125m` | HF repo-id or local path |
| `HF_TOKEN` | — | Required for `gated` models |
| `TENSOR_PARALLEL_SIZE` | `1` | Number of GPUs for tensor parallelism |
| `GPU_MEMORY_UTILIZATION` | `0.90` | Fraction of GPU VRAM to use |
| `MAX_MODEL_LEN` | `4096` | Maximum sequence length |
| `DTYPE` | `auto` | `auto` \| `float16` \| `bfloat16` |
| `QUANTIZATION` | — | `awq` \| `gptq` \| `squeezellm` |
| `LOG_LEVEL` | `INFO` | `DEBUG` \| `INFO` \| `WARNING` |

---

## Request Format

All requests go to a single RunPod endpoint. The `endpoint` field in the payload determines routing.

### Chat Completions

```json
{
  "endpoint": "chat/completions",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 256
}
```

### Text Completions

```json
{
  "endpoint": "completions",
  "prompt": "Once upon a time",
  "temperature": 0.8,
  "max_tokens": 128
}
```

### List Models

```json
{
  "endpoint": "models"
}
```

---

## Local Development

### Build Docker image

```bash
bash scripts/build.sh
```

### Run tests

```bash
pip install -r requirements.txt pytest
pytest tests/ -v
```

### Smoke-test the handler (no Docker)

```bash
MODEL_NAME=facebook/opt-125m bash scripts/test_local.sh
```

---

## Project Structure

```
vllm-runpod-serverless/
├── .github/workflows/docker-build.yml   # CI: build & push on push/tag
├── docker/
│   ├── Dockerfile                        # runpod/base + vLLM
│   └── .dockerignore
├── src/
│   ├── handler.py                        # RunPod entrypoint & router
│   ├── engine.py                         # vLLM AsyncLLMEngine wrapper
│   ├── model_loader.py                   # public / gated / custom loading
│   ├── api/
│   │   ├── chat.py                       # /chat/completions
│   │   ├── completions.py                # /completions
│   │   └── models.py                     # /models
│   └── utils/
│       ├── config.py                     # env-var config
│       └── logger.py                     # structured logging
├── scripts/
│   ├── build.sh
│   └── test_local.sh
├── tests/
│   ├── test_handler.py
│   ├── test_model_loader.py
│   └── payloads/
│       ├── chat_completion.json
│       └── completion.json
├── .env.example
├── requirements.txt
└── README.md
```

---

## CI / CD

Push to `main` or create a version tag (`v*`) to trigger the GitHub Actions workflow.  
Set `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` as repository secrets.
