https://console.runpod.io/hub/khs980714/Runpod-vLLM

---

## RunPod Hub Required 항목 처리

### [x] 3. Dockerfile (Required)
- 현재 `docker/Dockerfile`에 있어 RunPod이 감지 못함
- `Dockerfile`을 루트로 이동
- `docker/.dockerignore` → `.dockerignore`로 이동
- `.github/workflows/docker-build.yml`, `scripts/build.sh` 경로 수정

### [x] 4. Handler script (Required)
- 현재 `src/handler.py`에 있어 RunPod이 감지 못함
- 루트에 `handler.py` 생성 (src/handler.py로 위임)

### [x] 5. Badge
- README.md 상단에 배지 추가
- [![Runpod](https://api.runpod.io/badge/khs980714/Runpod-vLLM)](https://console.runpod.io/hub/khs980714/Runpod-vLLM)

### [ ] 6. Create a release (Required)
- 커밋/푸시 후 GitHub Release v0.1.1 생성 필요
- gh CLI 없어 수동 생성 필요: https://github.com/khs980714/Runpod-vLLM/releases/new
