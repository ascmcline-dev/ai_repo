"""Preset data for Standard Character Creator v1.5."""

from __future__ import annotations

import json
from pathlib import Path


_OPTIONS_FILE = Path(__file__).resolve().parents[1] / "web" / "character_options.json"
with _OPTIONS_FILE.open("r", encoding="utf-8") as handle:
    SHARED_OPTIONS = json.load(handle)

CLOTHING_BY_CATEGORY = SHARED_OPTIONS["clothing_by_category"]
PIERCING_TYPES_BY_LOCATION = SHARED_OPTIONS["piercing_types_by_location"]

CLOTHING_CATEGORIES = list(CLOTHING_BY_CATEGORY.keys())
ALL_CLOTHING_STYLES = list(
    dict.fromkeys(
        style
        for styles in CLOTHING_BY_CATEGORY.values()
        for style in styles
    )
)

PIERCING_LOCATIONS = list(PIERCING_TYPES_BY_LOCATION.keys())
ALL_PIERCING_TYPES = list(
    dict.fromkeys(
        style
        for styles in PIERCING_TYPES_BY_LOCATION.values()
        for style in styles
    )
)

GENDERS = [
    "Unspecified",
    "Adult Female",
    "Adult Male",
    "Androgynous / Nonbinary",
]

AGE_RANGES = [
    "18–24",
    "25–34",
    "35–44",
    "45–54",
    "55–64",
    "65+",
]

SKIN_TONES = [
    "Porcelain",
    "Fair",
    "Light",
    "Light-Medium",
    "Medium",
    "Olive",
    "Tan",
    "Deep Tan",
    "Brown",
    "Deep Brown",
    "Very Deep",
    "Custom / Unspecified",
]

COMPLEXIONS = [
    "Clear and Even",
    "Natural Skin Texture",
    "Freckled",
    "Beauty Marks",
    "Sun-Kissed",
    "Rosy",
    "Textured",
    "Acne-Prone",
    "Mature Fine Lines",
    "Weathered",
    "Vitiligo",
    "Unspecified",
]

FACE_SHAPES = [
    "Oval",
    "Round",
    "Square",
    "Heart-Shaped",
    "Diamond",
    "Oblong",
    "Rectangular",
    "Triangle",
    "Inverted Triangle",
    "Soft Angular",
    "Broad",
    "Narrow",
]

JAW_SHAPES = [
    "Soft Rounded",
    "Defined",
    "Sharp Angular",
    "Square",
    "Tapered",
    "Wide",
    "Narrow",
    "Strong",
    "Delicate",
    "Asymmetrical Natural",
]

CHIN_SHAPES = [
    "Rounded",
    "Pointed",
    "Square",
    "Broad",
    "Narrow",
    "Recessed",
    "Prominent",
    "Cleft",
    "Short",
    "Long",
]

EYE_COLORS = [
    "Dark Brown",
    "Brown",
    "Light Brown",
    "Amber",
    "Hazel",
    "Green",
    "Gray-Green",
    "Gray",
    "Blue-Gray",
    "Blue",
    "Light Blue",
    "Violet",
    "Heterochromia",
    "Very Dark / Near Black",
    "Custom / Unspecified",
]

EYE_SHAPES = [
    "Almond",
    "Round",
    "Hooded",
    "Monolid",
    "Deep-Set",
    "Upturned",
    "Downturned",
    "Wide-Set",
    "Close-Set",
    "Prominent",
    "Narrow",
    "Soft Average",
]

EYEBROW_SHAPES = [
    "Straight",
    "Soft Arch",
    "High Arch",
    "Rounded",
    "Angular",
    "Thick Natural",
    "Thin Defined",
    "Bushy",
    "Tapered",
    "Low-Set",
]

NOSE_SHAPES = [
    "Straight",
    "Button",
    "Upturned",
    "Downturned",
    "Aquiline",
    "Roman",
    "Broad",
    "Narrow",
    "Rounded Tip",
    "Pointed Tip",
    "Short",
    "Long",
]

LIP_SHAPES = [
    "Balanced Medium",
    "Full",
    "Thin",
    "Top-Heavy",
    "Bottom-Heavy",
    "Defined Cupid's Bow",
    "Soft Cupid's Bow",
    "Wide",
    "Narrow",
    "Downturned Corners",
]

HAIR_COLORS = [
    "Black",
    "Soft Black",
    "Dark Brown",
    "Medium Brown",
    "Light Brown",
    "Auburn",
    "Copper",
    "Strawberry Blonde",
    "Golden Blonde",
    "Platinum Blonde",
    "Silver",
    "Gray",
    "White",
    "Vivid / Fantasy Color",
    "Custom",
]

HAIR_LENGTHS = [
    "Buzzed",
    "Very Short",
    "Short",
    "Chin-Length",
    "Shoulder-Length",
    "Collarbone-Length",
    "Mid-Back",
    "Waist-Length",
    "Hip-Length",
    "Very Long",
]

HAIR_TEXTURES = [
    "Pin-Straight",
    "Straight",
    "Slightly Wavy",
    "Wavy",
    "Loose Curls",
    "Curly",
    "Tight Curls",
    "Coily",
    "Kinky-Coily",
    "Mixed Texture",
]

HAIR_STYLES = [
    "Loose Natural",
    "Center Part",
    "Side Part",
    "Slicked Back",
    "High Ponytail",
    "Low Ponytail",
    "Messy Bun",
    "Neat Bun",
    "Braids",
    "Box Braids",
    "Cornrows",
    "Bob",
    "Pixie Cut",
    "Shag / Layered",
    "Undercut",
]

HIGHLIGHT_STYLES = [
    "None",
    "Subtle Highlights",
    "Face-Framing Highlights",
    "Balayage",
    "Ombre",
    "Chunky Highlights",
    "Underlayer Color",
    "Full Multitone",
]

HIGHLIGHT_COLORS = HAIR_COLORS

HEIGHTS = [
    "Very Short",
    "Short",
    "Below Average",
    "Average",
    "Above Average",
    "Tall",
    "Very Tall",
    "Unspecified",
]

BODY_TYPES = [
    "Petite",
    "Slim",
    "Lean",
    "Lean Athletic",
    "Athletic",
    "Average",
    "Curvy",
    "Hourglass",
    "Pear-Shaped",
    "Broad",
    "Muscular",
    "Plus Size",
]

BRA_BANDS = [
    "Unspecified",
    "28",
    "30",
    "32",
    "34",
    "36",
    "38",
    "40",
    "42",
    "44",
]

CUP_SIZES = [
    "Unspecified",
    "AA",
    "A",
    "B",
    "C",
    "D",
    "DD / E",
    "DDD / F",
    "G",
    "H",
]


BREAST_SHAPES = [
    "Unspecified",
    "Bell Shape",
    "Teardrop",
    "Round",
    "Asymmetrical Natural",
    "East-West",
    "Side-Set",
    "Slender",
]

BREAST_SHAPE_PROMPTS = {
    "Bell Shape": (
        "bell-shaped breasts with a narrower upper pole and fuller rounded lower pole"
    ),
    "Teardrop": (
        "teardrop-shaped breasts with a gentle upper slope and natural lower fullness"
    ),
    "Round": (
        "round breasts with balanced upper-pole and lower-pole fullness"
    ),
    "Asymmetrical Natural": (
        "naturally asymmetrical breasts with subtle realistic left-right size or height variation"
    ),
    "East-West": (
        "east-west breast orientation with the breast projection angled slightly outward"
    ),
    "Side-Set": (
        "side-set breasts with a wider natural center gap and fuller outer chest"
    ),
    "Slender": (
        "slender elongated breast shape with a narrow base and gentle vertical contour"
    ),
}

BREAST_POSITIONS = [
    "Unspecified",
    "Natural Average-Set",
    "High-Set / Perky",
    "High and Tight",
    "Low-Set",
    "Downward-Sloping",
    "Pendulous Natural",
]

BREAST_POSITION_PROMPTS = {
    "Natural Average-Set": "natural average-set breast position",
    "High-Set / Perky": (
        "high-set perky breast position with a natural upward presentation"
    ),
    "High and Tight": (
        "high and tight breast position with compact chest attachment and minimal lower drop"
    ),
    "Low-Set": (
        "low-set breast position with lower chest attachment and realistic gravitational weight"
    ),
    "Downward-Sloping": (
        "natural downward-sloping breast position with visible lower-pole weight"
    ),
    "Pendulous Natural": (
        "naturally pendulous breast position with lower-set fullness and realistic gravitational drop"
    ),
}

BREAST_FIRMNESS = [
    "Unspecified",
    "Firm",
    "Naturally Firm",
    "Balanced Natural",
    "Soft",
    "Very Soft / Natural Movement",
]

BREAST_FIRMNESS_PROMPTS = {
    "Firm": "firm breast tissue with limited natural movement",
    "Naturally Firm": (
        "naturally firm breast tissue with stable shape and slight realistic movement"
    ),
    "Balanced Natural": (
        "balanced natural breast tissue with moderate softness and realistic weight"
    ),
    "Soft": (
        "soft natural breast tissue with gentle shape variation and realistic gravity"
    ),
    "Very Soft / Natural Movement": (
        "very soft natural breast tissue with pronounced settling, weight, and realistic movement"
    ),
}

BREAST_AUGMENTATION = [
    "Unspecified",
    "Natural / Unaugmented",
    "Subtle Natural-Looking Augmentation",
    "Round High-Profile Implants",
    "Teardrop / Anatomical Implants",
    "Very Firm Augmented Projection",
]

BREAST_AUGMENTATION_PROMPTS = {
    "Natural / Unaugmented": "natural unaugmented breast structure",
    "Subtle Natural-Looking Augmentation": (
        "subtle natural-looking breast augmentation with moderate projection and preserved natural slope"
    ),
    "Round High-Profile Implants": (
        "round high-profile breast implants with increased upper-pole fullness and forward projection"
    ),
    "Teardrop / Anatomical Implants": (
        "anatomical teardrop breast implants with a sloped upper pole and fuller lower pole"
    ),
    "Very Firm Augmented Projection": (
        "very firm augmented breasts with strong forward projection, high upper-pole fullness, "
        "and minimal natural drop"
    ),
}

MALE_GROIN_SIZES = [
    "Unspecified",
    "Small",
    "Average",
    "Large",
    "Extra Large",
]

FEMALE_GROIN_DESCRIPTIONS = [
    "Unspecified",
    "Shaved Vulva",
    "Closely Trimmed Pubic Hair",
    "Trimmed Pubic Hair",
    "Natural / Untrimmed Pubic Hair",
]

BUTTOCKS = [
    "Petite",
    "Small",
    "Average",
    "Rounded",
    "Full",
    "Large",
    "Very Large",
    "Athletic",
]

JEWELRY_LEVELS = [
    "None",
    "Minimal",
    "Everyday",
    "Layered",
    "Statement",
    "Luxury",
    "Alternative",
]

JEWELRY_ITEMS = [
    "None",
    "Stud Earrings",
    "Hoop Earrings",
    "Drop Earrings",
    "Pendant Necklace",
    "Chain Necklace",
    "Bracelet",
    "Watch",
    "Rings",
    "Nose Jewelry",
    "Body Chain",
    "Mixed Minimal Jewelry",
    "Statement Jewelry",
]

JEWELRY_MATERIALS = [
    "Unspecified",
    "Gold",
    "Silver",
    "Rose Gold",
    "Platinum",
    "Stainless Steel",
    "Black Metal",
    "Pearl",
    "Gemstone",
    "Mixed Materials",
]

TATTOO_STATUSES = [
    "None",
    "One Tattoo",
    "Multiple Tattoos",
]

TATTOO_LOCATIONS = [
    "Face",
    "Neck",
    "Collarbone / Chest",
    "Shoulder",
    "Upper Arm",
    "Forearm",
    "Hand / Fingers",
    "Upper Back",
    "Lower Back",
    "Ribcage / Side",
    "Abdomen",
    "Hip / Pelvis",
    "Buttock",
    "Thigh",
    "Calf / Ankle",
]

PIERCING_STATUSES = [
    "None",
    "One Piercing",
    "Multiple Piercings",
]

NEGATIVE_PRESETS = {
    "None": "",
    "Standard Character": (
        "child, teenager, underage, ambiguous age, malformed anatomy, distorted face, "
        "asymmetrical eyes, extra limbs, missing fingers, fused fingers, text, watermark, logo"
    ),
    "Realism": (
        "child, teenager, underage, ambiguous age, plastic skin, airbrushed skin, beauty filter, "
        "doll-like face, CGI, illustration, malformed anatomy, distorted proportions, text, watermark"
    ),
}

SHOT_TYPES = {
    "Close-Up Face Portrait": (
        "close-up face portrait, crop from the top of the head to the upper shoulders, "
        "full head visible with slight headroom, face occupying most of the frame, eye-level camera"
    ),
    "Head and Shoulders Portrait": (
        "head-and-shoulders portrait, crop from the top of the head to the upper chest, "
        "full head and both shoulders visible, face remains the dominant subject"
    ),
    "Chest-Up Portrait": (
        "chest-up portrait, crop from the top of the head to the lower chest, "
        "full head visible, upper torso and clothing clearly visible"
    ),
    "Waist-Up Midshot": (
        "waist-up midshot, crop from the top of the head to the waist, "
        "full head, arms, torso, and waist visible"
    ),
    "Three-Quarter Body": (
        "three-quarter body photograph, subject visible from the top of the head to below the knees, "
        "natural proportions, sufficient headroom, limbs clearly visible"
    ),
    "Full Body": (
        "full-body character photograph, entire adult subject visible from the top of the head to the feet, "
        "both feet fully inside frame, natural proportions, sufficient headroom and floor space"
    ),
    "Full Body Character Reference": (
        "full-body character reference photograph, entire adult subject visible head to toe, "
        "neutral balanced stance, arms and legs unobstructed, both feet fully visible, plain readable composition"
    ),
}

CAMERA_VIEWS = {
    "Front View": "front-facing view, camera centered",
    "Three-Quarter Left": (
        "body and face turned approximately 45 degrees toward the subject's left, "
        "both eyes visible when the face is included"
    ),
    "Three-Quarter Right": (
        "body and face turned approximately 45 degrees toward the subject's right, "
        "both eyes visible when the face is included"
    ),
    "Left Profile": "true left-side profile view, body and face aligned to the left",
    "Right Profile": "true right-side profile view, body and face aligned to the right",
    "Rear Three-Quarter Left": (
        "rear three-quarter view turned approximately 45 degrees toward the subject's left, "
        "back, side contour, and hairstyle visible"
    ),
    "Rear Three-Quarter Right": (
        "rear three-quarter view turned approximately 45 degrees toward the subject's right, "
        "back, side contour, and hairstyle visible"
    ),
    "Back View": "back-facing view with the rear of the body and hairstyle visible",
}

SHOT_NEGATIVES = {
    "Close-Up Face Portrait": "full-body shot, distant subject, tiny face, waist-up framing, cropped forehead, cropped chin",
    "Head and Shoulders Portrait": "full-body shot, distant subject, tiny face, waist-up framing, cropped forehead",
    "Chest-Up Portrait": "full-body shot, distant subject, tiny face, lower-body emphasis",
    "Waist-Up Midshot": "face-only close-up, full-body shot, cropped torso, missing arms",
    "Three-Quarter Body": "face-only close-up, headshot, cropped knees, cropped legs, missing limbs",
    "Full Body": "face-only close-up, headshot, chest-up crop, waist-up crop, cropped feet, feet outside frame, missing legs",
    "Full Body Character Reference": (
        "face-only close-up, headshot, chest-up crop, waist-up crop, cropped feet, feet outside frame, "
        "missing legs, crossed limbs, concealed hands"
    ),
}

