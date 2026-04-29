#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-vllm-runpod-serverless}"
TAG="${TAG:-latest}"
FULL_IMAGE="${IMAGE_NAME}:${TAG}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "Building image: ${FULL_IMAGE}"
echo "Context:        ${PROJECT_ROOT}"

docker build \
  --file "${PROJECT_ROOT}/docker/Dockerfile" \
  --tag  "${FULL_IMAGE}" \
  "${PROJECT_ROOT}"

echo ""
echo "Build complete: ${FULL_IMAGE}"
echo "Run locally:  docker run --rm --gpus all -e MODEL_NAME=facebook/opt-125m ${FULL_IMAGE}"
