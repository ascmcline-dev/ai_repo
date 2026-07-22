# Dataset Shot Planner v1.7.0

## Improved Midshot framing

Midshot now explicitly requests:

- framing from slightly above the complete head
- small visible headroom
- complete hair and full head
- neck, both shoulders, chest, arms and torso
- natural waist and mid-abdomen
- lower edge around the navel or lower mid-abdomen

The negative output rejects shoulder-only, chest-up, bust-only,
cropped-hair, cropped-abdomen, cropped-waist and camera-too-close results.

Independent camera-view controls from v1.6 remain available.

## Installation

Replace the old `dataset_shot_planner` directory under
`ComfyUI/custom_nodes`, restart ComfyUI, and hard-refresh with `Ctrl+Shift+R`.
