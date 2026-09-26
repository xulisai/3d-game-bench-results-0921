# 3D Game Agent Bench — Completed Results (2026-09-24)

Both models are complete. Each is packaged as its own zip:

| File | Contents | Size |
|------|----------|------|
| [`Gemini-3.8-Flash_results_0924.zip`](./Gemini-3.8-Flash_results_0924.zip) | Gemini-3.8-Flash · **120 / 120** games (tasks 1–120) | ~82 MB |
| [`GLM-5.3-Flash_results_0924.zip`](./GLM-5.3-Flash_results_0924.zip) | GLM-5.3-Flash · **110 / 110** games (tasks 46–155) | ~41 MB |

## Preview after unzip

Do **not** open `index.html` via `file://`.

```bash
unzip Gemini-3.8-Flash_results_0924.zip
cd Gemini-3.8-Flash
python3 -m http.server 8123
# open http://127.0.0.1:8123/
```

Same for the GLM zip (serve from the `GLM-5.3-Flash` folder).
