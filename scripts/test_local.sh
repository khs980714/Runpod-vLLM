#!/usr/bin/env bash
# Test the handler locally using RunPod's local_test utility.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PAYLOAD_DIR="${PROJECT_ROOT}/tests/payloads"

export MODEL_TYPE="${MODEL_TYPE:-public}"
export MODEL_NAME="${MODEL_NAME:-facebook/opt-125m}"
export TENSOR_PARALLEL_SIZE="${TENSOR_PARALLEL_SIZE:-1}"
export GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.90}"
export MAX_MODEL_LEN="${MAX_MODEL_LEN:-512}"

cd "${PROJECT_ROOT}"

echo "=== Chat Completions Test ==="
python -c "
import asyncio, json, sys
sys.path.insert(0, '.')
from src.handler import handler

payload = json.load(open('${PAYLOAD_DIR}/chat_completion.json'))
result = asyncio.run(handler({'id': 'test-001', 'input': payload}))
print(json.dumps(result, indent=2))
"

echo ""
echo "=== Text Completions Test ==="
python -c "
import asyncio, json, sys
sys.path.insert(0, '.')
from src.handler import handler

payload = json.load(open('${PAYLOAD_DIR}/completion.json'))
result = asyncio.run(handler({'id': 'test-002', 'input': payload}))
print(json.dumps(result, indent=2))
"
