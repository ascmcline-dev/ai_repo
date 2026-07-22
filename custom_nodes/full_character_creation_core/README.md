# Full Character Creation Core v1.1

Two simplified nodes:

- Character Blueprint Creator v1.1
- Character Shot Planner v1.1

## Clothing authority update

The Blueprint Creator now separates:

- clinical anatomy upper/lower body descriptions
- clothed upper/lower silhouette descriptions
- a structured default outfit

Default clothing presets are now complete outfits. A fitted T-shirt preset includes a top, bottom, and footwear instead of describing only a shirt.

Optional structured outfit fields are available for top, bottom, footwear, outerwear, one-piece garments, and swimwear top/bottom.

The Shot Planner adds:

- Body Detail Mode
- Outfit Coverage
- Clothing Priority
- Exact Top, Bottom, Footwear, and Outerwear fields

Clothing is placed immediately after framing in Krea and Qwen prompts. Exact Outfit Override excludes anatomy-only details such as pubic-hair notes and uses a clothed silhouette instead.

Outfit wording is crop-aware for face close-ups, chest-up, waist-up, three-quarter, full-body, and body-close-up shots. Swimwear is treated as a matching top-and-bottom set.
