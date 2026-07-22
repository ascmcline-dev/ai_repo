# Standard Character Creator v1.5

Creates a reusable adult `CHARACTER_PROFILE` with identity, body, anatomy,
camera-view and chest-conformation controls.

## Adult female chest controls

Cup size is now supplemented by independent visual controls:

- Breast Shape: Bell, Teardrop, Round, Asymmetrical, East-West, Side-Set, Slender
- Breast Position: Natural, High-Set / Perky, High and Tight, Low-Set,
  Downward-Sloping, Pendulous Natural
- Breast Firmness: Firm, Naturally Firm, Balanced Natural, Soft,
  Very Soft / Natural Movement
- Breast Augmentation: Natural / Unaugmented, Subtle Natural-Looking,
  Round High-Profile, Teardrop / Anatomical, Very Firm Augmented Projection

The values are stored in `CHARACTER_PROFILE` and included in upper-body,
midshot, full-body and relevant anatomy prompts. Face-only prompts omit them.

New outputs:

- `chest_prompt`
- `chest_warning`

The warning output reports obvious conflicting combinations.

## Installation

Replace the old `standard_character_creator` directory under
`ComfyUI/custom_nodes`, restart ComfyUI, and hard-refresh with `Ctrl+Shift+R`.
