https://console.runpod.io/hub/khs980714/Runpod-vLLM

---

## RunPod Hub Publish 체크리스트

### 1. `.runpod/hub.json` 생성
Hub 등록에 필수인 메타데이터 파일.

필수 필드:
- `title` — 표시 이름
- `description` — 기능 설명
- `type` — `"serverless"` 고정
- `category` — `"language"` (LLM이므로)
- `config.runsOn` — `"GPU"`
- `config.containerDiskInGb` — 디스크 크기 (정수)
- `config.gpuCount` — GPU 수
- `config.env` — 환경변수 목록 (MODEL_TYPE, MODEL_NAME, HF_TOKEN 등 RunPod UI에서 입력받을 항목)

참고 env 타입:
- `MODEL_NAME` → `input.type: "huggingface"` 또는 `"string"`
- `MODEL_TYPE` → `input.type: "options"` (public / gated / custom)
- `HF_TOKEN` → `input.type: "string"`
- `QUANTIZATION` → `input.type: "options"` (awq / gptq / "")
- `TENSOR_PARALLEL_SIZE`, `MAX_MODEL_LEN` → `input.type: "number"`
- `GPU_MEMORY_UTILIZATION`, `DTYPE` → `input.type: "string"` 또는 options

### 2. `.runpod/tests.json` 생성
Hub 자동 테스트용 파일.

필수 필드:
- `name` — 테스트 이름
- `input` — 요청 페이로드 (tests/payloads/ 참고)
- `gpuTypeId` — 테스트에 사용할 GPU 종류
- `gpuCount` — GPU 수
- `env` — 테스트용 환경변수 (MODEL_NAME 등)
- `allowedCudaVersions` — `["12.1"]`

### 3. GitHub Release 생성
Hub는 GitHub Release 기준으로 버전을 인덱싱함.
- 태그 예시: `v0.1.0`
- Release Notes 작성

### 4. GitHub 계정 연동 확인
RunPod 콘솔에서 GitHub 프로필이 계정에 연동되어 있는지 확인.
- 콘솔 → Settings → Integrations
