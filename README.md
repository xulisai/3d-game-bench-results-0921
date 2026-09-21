# 3D Game Agent Bench — Completed Results (2026-09-21)

Each model is packaged as its own zip:

| File | Contents | Size |
|------|----------|------|
| [`Gemini-3.8-Flash_results_0921.zip`](./Gemini-3.8-Flash_results_0921.zip) | Gemini-3.8-Flash · **119** games | ~81 MB |
| [`GLM-5.3-Flash_results_0921.zip`](./GLM-5.3-Flash_results_0921.zip) | GLM-5.3-Flash · **109** games | ~41 MB |

## Preview after unzip

Do **not** open `index.html` via `file://`.

```bash
unzip Gemini-3.8-Flash_results_0921.zip
cd Gemini-3.8-Flash
python3 -m http.server 8123
# open http://127.0.0.1:8123/
```

Same for the GLM zip (serve from the `GLM-5.3-Flash` folder).
