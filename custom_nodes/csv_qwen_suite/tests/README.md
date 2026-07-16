# CSV Qwen Suite (ComfyUI Custom Nodes)

A tiny node pack that solves the classic ComfyUI problem: **“I queued 120 runs but it keeps using row 1 forever.”**

This suite provides a single node:

**CSV Qwen Prompt + Seed Iterator**
- Loads `positive` / `negative` prompts from a CSV
- Repeats each row `batch_per_row` times
- Automatically advances **row_index** and **take_index** on every queued execution
- Outputs a deterministic changing seed per run:
  `seed = base_seed + row_index*row_stride + take_index*take_stride`

## Install

1. Copy this folder into:
   `ComfyUI/custom_nodes/csv_qwen_suite/`
2. Restart ComfyUI.

## CSV format

`example.csv`:

```csv
positive,negative
"a cozy sci‑fi portrait, soft rim light, high detail","text, watermark, blurry, lowres"
"industrial cyberpunk hallway, dramatic lighting, realistic","text, watermark, blurry, lowres"
```

Column names are auto-detected if you leave `positive_column` / `negative_column` empty.

## How to use

1. Add node: **prompt/csv_qwen → CSV Qwen Prompt + Seed Iterator**
2. Set:
   - `csv_path` to your CSV file
   - `batch_per_row` to your repeats per row (e.g. 4)
3. Queue runs:
   - If CSV has 30 rows and batch_per_row=4 → queue 120
4. Wire outputs:
   - `positive` → your Qwen (or text-encode) positive prompt input
   - `negative` → your negative prompt input
   - `seed` → your sampler / qwen seed input

## Notes on stability across queued runs

ComfyUI can re-instantiate nodes, so this node avoids relying on in-memory counters.
If ComfyUI does not expose a run index in the hidden context (it usually doesn’t),
the node uses a small **file-backed counter** stored in ComfyUI’s temp directory.

This is designed to be:
- Safe (no eval/exec, no pip installs)
- Deterministic and repeatable for a given run order

## Troubleshooting

- If you change your CSV content while a big queue is running, you can get mismatches.
  Best practice: keep CSV stable for the duration of a queue.
- Turn on `debug=true` to see exactly which row/take/run index is being selected.
