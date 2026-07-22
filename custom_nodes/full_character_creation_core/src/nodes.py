from __future__ import annotations

import hashlib
import re
from typing import Any


def _join(*parts: str) -> str:
    return ", ".join(str(p).strip(" ,") for p in parts if p and str(p).strip(" ,"))


def _slug(text: str) -> str:
    value = str(text).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


GENDERS = ["Adult Female", "Adult Male", "Adult Nonbinary"]
AGE_RANGES = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
HERITAGES = [
    "Unspecified",
    "Latin American / Hispanic",
    "Afro-Latino",
    "Caribbean",
    "White / European (Caucasian)",
    "Mediterranean / Southern European",
    "Black / African Descent",
    "Mixed Black / Multiracial",
    "East Asian",
    "Japanese",
    "Chinese",
    "Korean",
    "South Asian",
    "Southeast Asian",
    "Middle Eastern / North African",
    "Indigenous / Native American",
    "Pacific Islander",
    "Mixed Heritage",
    "Custom",
]
SKIN_TONES = [
    "Very Light", "Light", "Light-Medium", "Medium", "Olive", "Deep Tan",
    "Brown", "Deep Brown", "Very Deep", "Custom / Unspecified",
]
COMPLEXIONS = [
    "Natural Skin Texture", "Clear and Even", "Freckled", "Lightly Freckled",
    "Visible Pores", "Sun-Kissed", "Mature Natural Skin", "Unspecified",
]
FACE_SHAPES = ["Oval", "Round", "Heart-Shaped", "Soft Angular", "Square", "Long", "Diamond", "Unspecified"]
JAW_SHAPES = ["Delicate", "Soft", "Defined", "Strong", "Wide", "Tapered", "Unspecified"]
CHIN_SHAPES = ["Rounded", "Pointed", "Square", "Soft", "Prominent", "Unspecified"]
EYE_COLORS = ["Brown", "Dark Brown", "Hazel", "Green", "Blue", "Gray", "Amber", "Custom / Unspecified"]
EYE_SHAPES = ["Almond", "Round", "Prominent", "Deep-Set", "Hooded", "Upturned", "Downturned", "Unspecified"]
EYEBROWS = ["Soft Arch", "High Arch", "Straight", "Thick Natural", "Thin Natural", "Angular", "Unspecified"]
NOSES = ["Straight", "Narrow", "Button", "Wide", "Aquiline", "Rounded", "Upturned", "Unspecified"]
LIPS = ["Thin", "Balanced Medium", "Full", "Soft Cupid's Bow", "Wide", "Narrow", "Unspecified"]
HAIR_COLORS = ["Black", "Dark Brown", "Medium Brown", "Light Brown", "Strawberry Blonde", "Blonde", "Platinum", "Red", "Gray", "Silver", "Custom"]
HAIR_LENGTHS = ["Buzzed", "Very Short", "Chin-Length", "Shoulder-Length", "Mid-Back", "Waist-Length", "Custom"]
HAIR_TEXTURES = ["Pin-Straight", "Straight", "Slightly Wavy", "Wavy", "Curly", "Coily", "Custom"]
HAIR_STYLES = ["Loose Natural", "Center Part", "Side Part", "Braids", "Ponytail", "Bun", "Pixie", "Locs", "Afro", "Custom"]
HEIGHTS = ["Short", "Below Average", "Average", "Above Average", "Tall", "Very Tall", "Unspecified"]
BODY_TYPES = ["Very Slim", "Slim", "Average", "Athletic", "Curvy", "Full-Figured", "Muscular", "Heavyset", "Custom / Unspecified"]
BUST_SIZES = [
    "Unspecified", "Very Small", "Small", "Small-Medium", "Medium",
    "Medium-Full", "Full", "Large", "Very Large", "Overly Large",
]
BUST_SIZE_PROMPTS = {
    "Very Small": "very small bust with minimal projection and subtle chest volume",
    "Small": "small bust with gentle natural projection",
    "Small-Medium": "small-to-medium bust with modest natural projection",
    "Medium": "medium bust with balanced natural projection",
    "Medium-Full": "medium-full bust with noticeable but balanced projection",
    "Full": "full bust with pronounced natural volume and projection",
    "Large": "large bust with substantial natural volume and projection",
    "Very Large": "very large bust with heavy natural volume and strong projection",
    "Overly Large": "extremely large bust with exaggerated volume, very strong projection, and substantial natural weight",
}
BUST_SHAPES = ["Unspecified", "Bell Shape", "Teardrop", "Round", "Asymmetrical Natural", "East-West", "Side-Set", "Slender"]
BUST_SHAPE_PROMPTS = {
    "Bell Shape": "bell-shaped bust with a narrower upper pole and fuller rounded lower pole",
    "Teardrop": "teardrop-shaped bust with a gentle upper slope and natural lower fullness",
    "Round": "round bust with balanced upper-pole and lower-pole fullness",
    "Asymmetrical Natural": "naturally asymmetrical bust with subtle realistic left-right variation",
    "East-West": "east-west bust orientation with projection angled slightly outward",
    "Side-Set": "side-set bust with a wider natural center gap and fuller outer chest",
    "Slender": "slender elongated bust shape with a narrow base and gentle vertical contour",
}
BUST_POSITIONS = ["Unspecified", "Natural Average-Set", "High-Set / Perky", "High and Tight", "Low-Set", "Downward-Sloping", "Pendulous Natural"]
BUST_POSITION_PROMPTS = {
    "Natural Average-Set": "natural average-set chest position",
    "High-Set / Perky": "high-set perky chest position with a natural upward presentation",
    "High and Tight": "high and tight chest position with compact attachment and minimal lower drop",
    "Low-Set": "low-set chest position with realistic gravitational weight",
    "Downward-Sloping": "natural downward-sloping chest position with visible lower-pole weight",
    "Pendulous Natural": "naturally pendulous chest position with lower-set fullness and realistic gravitational drop",
}
BUST_FIRMNESS = ["Unspecified", "Firm", "Naturally Firm", "Balanced Natural", "Soft", "Very Soft / Natural Movement"]
BUST_FIRMNESS_PROMPTS = {
    "Firm": "firm chest tissue with limited natural movement",
    "Naturally Firm": "naturally firm chest tissue with stable shape and slight realistic movement",
    "Balanced Natural": "balanced natural chest tissue with moderate softness and realistic weight",
    "Soft": "soft natural chest tissue with gentle shape variation and realistic gravity",
    "Very Soft / Natural Movement": "very soft natural chest tissue with pronounced settling, weight, and realistic movement",
}
BUST_AUGMENTATION = ["Unspecified", "Natural / Unaugmented", "Subtle Natural-Looking Augmentation", "Round High-Profile Implants", "Teardrop / Anatomical Implants", "Very Firm Augmented Projection"]
BUST_AUGMENTATION_PROMPTS = {
    "Natural / Unaugmented": "natural unaugmented chest structure",
    "Subtle Natural-Looking Augmentation": "subtle natural-looking augmentation with moderate projection and preserved natural slope",
    "Round High-Profile Implants": "round high-profile implants with increased upper-pole fullness and forward projection",
    "Teardrop / Anatomical Implants": "anatomical teardrop implants with a sloped upper pole and fuller lower pole",
    "Very Firm Augmented Projection": "very firm augmented projection with high upper-pole fullness and minimal natural drop",
}
BUTTOCKS = ["Unspecified", "Small", "Average", "Rounded", "Full", "Wide", "Athletic", "Prominent"]
DEFAULT_CLOTHING = [
    "Simple Fitted T-Shirt", "Opaque Fitted Tank Top", "Casual Jeans and T-Shirt",
    "Fitted Athletic Outfit", "Simple Dress", "Business Casual", "Swimwear",
    "Clinical Unclothed Documentation", "Custom",
]
JEWELRY_LEVELS = ["None", "Minimal", "Everyday", "Statement", "Custom"]
MARK_STATUSES = ["None", "One", "Multiple"]

SHOT_TYPES = ["Face Close-Up", "Head and Shoulders", "Chest-Up", "Waist-Up Midshot", "Three-Quarter Body", "Full Body", "Body Close-Up"]
SHOT_PROMPTS = {
    "Face Close-Up": "close-up face portrait framed from slightly above the complete head to the upper shoulders, face occupying most of the image",
    "Head and Shoulders": "head-and-shoulders portrait with full head, hair, neck, shoulders, and upper chest visible",
    "Chest-Up": "true chest-up portrait with the camera pulled back, frame beginning slightly above the complete head and ending below the bust line, full neck, both shoulders, complete upper chest, both upper arms, and the full visible bust area inside the image",
    "Waist-Up Midshot": "true waist-up midshot framed from slightly above the complete head to the navel or lower mid-abdomen, full head, both shoulders, arms, torso, natural waist, and mid-abdomen visible",
    "Three-Quarter Body": "three-quarter-body photograph framed from slightly above the complete head to below the knees, arms and legs clearly visible",
    "Full Body": "full-body photograph with the entire subject visible from head to feet and balanced space around the body",
    "Body Close-Up": "focused body-documentation close-up of the selected region with that region fully visible and centered",
}
CAMERA_VIEWS = ["Front View", "Three-Quarter Left", "Three-Quarter Right", "Left Profile", "Right Profile", "Rear Three-Quarter Left", "Rear Three-Quarter Right", "Back View"]
CAMERA_PROMPTS = {
    "Front View": "front-facing camera view, camera centered",
    "Three-Quarter Left": "three-quarter-left camera view, body and face turned approximately 45 degrees left",
    "Three-Quarter Right": "three-quarter-right camera view, body and face turned approximately 45 degrees right",
    "Left Profile": "true left-profile camera view",
    "Right Profile": "true right-profile camera view",
    "Rear Three-Quarter Left": "rear three-quarter-left camera view",
    "Rear Three-Quarter Right": "rear three-quarter-right camera view",
    "Back View": "direct back-facing camera view",
}
POSES = ["Neutral Standing", "Relaxed Standing", "Seated", "Leaning", "Walking", "Arms Relaxed", "Arms Loosely Crossed", "One Hand at Waist", "Custom"]
EXPRESSIONS = ["Neutral", "Natural Closed-Mouth Smile", "Genuine Smile", "Serious", "Focused", "Thoughtful", "Custom"]
BODY_REGIONS = ["Upper Torso", "Chest and Ribcage", "Abdomen and Waist", "Upper Back and Shoulders", "Lower Back and Waist", "Hips Front", "Hips Rear", "Left Side Torso", "Right Side Torso", "Custom"]
STAGES = ["Krea Identity Anchor", "Qwen Face Documentation", "Qwen Upper-Body Anchor", "Qwen Anatomy Documentation", "Qwen Clothing Edit", "Qwen Body Close-Up", "Krea Mini-LoRA Expansion"]
CLOTHING_MODES = ["Profile Default", "Exact Outfit Override", "Clinical Unclothed", "Preserve Reference Clothing"]
BODY_DETAIL_MODES = ["Auto by Stage", "Clothed Silhouette", "Clinical Anatomy"]
OUTFIT_COVERAGE = ["Auto by Shot", "Complete Outfit", "Upper-Body Garment", "Lower-Body Garment", "One-Piece Garment", "Swimwear Set"]
CLOTHING_PRIORITIES = ["Standard", "Strong", "Maximum"]
BACKGROUNDS = ["Plain Neutral", "Simple Indoor", "Simple Outdoor", "Clinical Neutral", "Natural Home", "Gym", "Custom"]
LIGHTING = ["Soft Natural Daylight", "Even Window Light", "Clinical Even Light", "Warm Indoor Light", "Overcast Outdoor Light", "Custom"]
PHOTO_STYLES = ["Authentic Consumer Camera", "Personal Cellphone Photo", "Identity Documentation", "Clinical Documentation", "Standard Camera Photo"]


PRESET_OUTFITS: dict[str, dict[str, str]] = {
    "Simple Fitted T-Shirt": {
        "kind": "complete",
        "top": "simple fitted T-shirt",
        "bottom": "high-waisted fitted jeans",
        "footwear": "casual low-profile shoes",
    },
    "Opaque Fitted Tank Top": {
        "kind": "complete",
        "top": "opaque fitted tank top",
        "bottom": "high-waisted fitted jeans",
        "footwear": "casual low-profile shoes",
    },
    "Casual Jeans and T-Shirt": {
        "kind": "complete",
        "top": "casual fitted T-shirt",
        "bottom": "well-fitted jeans",
        "footwear": "casual sneakers",
    },
    "Fitted Athletic Outfit": {
        "kind": "complete",
        "top": "fitted opaque athletic top",
        "bottom": "high-waisted athletic leggings",
        "footwear": "training shoes",
    },
    "Simple Dress": {
        "kind": "one_piece",
        "one_piece": "simple fitted knee-length dress",
        "footwear": "simple low-profile shoes",
    },
    "Business Casual": {
        "kind": "complete",
        "top": "fitted business-casual blouse",
        "bottom": "tailored trousers",
        "footwear": "simple flats",
    },
    "Swimwear": {
        "kind": "swimwear",
        "swimwear_top": "matching fitted swimwear top",
        "swimwear_bottom": "matching fitted swimwear bottoms",
    },
    "Clinical Unclothed Documentation": {"kind": "clinical"},
    "Custom": {"kind": "custom"},
}


def _heritage_prompt(heritage: str, custom: str) -> str:
    if heritage == "Unspecified":
        return ""
    if heritage == "Custom":
        return custom.strip()
    return f"{heritage.lower()} heritage"


def _hair_value(value: str, custom: str, label: str) -> str:
    if value == "Custom":
        return custom.strip()
    return f"{value.lower()} {label}" if value else ""


def _bust_prompt(gender: str, size: str, shape: str, position: str, firmness: str, augmentation: str) -> str:
    if gender != "Adult Female":
        return ""
    return _join(
        BUST_SIZE_PROMPTS.get(size, ""),
        BUST_SHAPE_PROMPTS.get(shape, ""),
        BUST_POSITION_PROMPTS.get(position, ""),
        BUST_FIRMNESS_PROMPTS.get(firmness, ""),
        BUST_AUGMENTATION_PROMPTS.get(augmentation, ""),
    )


def _clothed_bust_prompt(gender: str, size: str, shape: str, position: str) -> str:
    if gender != "Adult Female":
        return ""
    size_text = BUST_SIZE_PROMPTS.get(size, "")
    shape_text = BUST_SHAPE_PROMPTS.get(shape, "")
    position_text = BUST_POSITION_PROMPTS.get(position, "")
    if size_text:
        size_text = size_text.replace("bust with", "bust shaping the garment with")
    return _join(size_text, shape_text, position_text)


def _split_lines(text: str) -> list[str]:
    values = []
    for block in re.split(r"[\r\n;]+", text or ""):
        cleaned = re.sub(r"^\s*(?:[-*•]+|\d+[.)])\s*", "", block).strip(" ,.;")
        if cleaned:
            values.append(cleaned)
    return values


def _marks_prompt(kind: str, status: str, description: str) -> tuple[str, list[str], str]:
    if status == "None":
        return "", [], ""
    entries = _split_lines(description)
    warnings = []
    if not entries:
        warnings.append(f"{kind} status is enabled but no descriptor was provided.")
    if status == "One" and len(entries) > 1:
        warnings.append(f"One {kind.lower()} is selected but multiple lines were supplied.")
    if status == "Multiple" and len(entries) < 2:
        warnings.append(f"Multiple {kind.lower()}s are selected but fewer than two lines were supplied.")
    if not entries:
        return "", [], " ".join(warnings)
    if len(entries) == 1:
        prompt = f"one permanent identity {kind.lower()} with exact placement: {entries[0]}"
    else:
        numbered = "; ".join(f"{kind.lower()} {i}: {entry}" for i, entry in enumerate(entries, 1))
        prompt = f"{len(entries)} separate permanent identity {kind.lower()}s with exact placements: {numbered}"
    return prompt, entries, " ".join(warnings)


def _infer_outfit_kind(text: str) -> str:
    lowered = (text or "").lower()
    if any(token in lowered for token in ("bikini", "swimwear", "swimsuit", "two-piece", "two piece")):
        return "swimwear"
    if any(token in lowered for token in ("dress", "bodysuit", "romper", "jumpsuit", "one-piece", "one piece")):
        return "one_piece"
    return "complete"


def _build_profile_outfit(
    default_clothing: str,
    exact_default_clothing: str,
    default_top: str,
    default_bottom: str,
    default_footwear: str,
    default_outerwear: str,
    default_one_piece: str,
    default_swimwear_top: str,
    default_swimwear_bottom: str,
    outfit_notes: str,
) -> tuple[str, dict[str, str]]:
    preset = dict(PRESET_OUTFITS.get(default_clothing, {"kind": "custom"}))

    components = {
        "kind": preset.get("kind", "custom"),
        "top": default_top.strip() or preset.get("top", ""),
        "bottom": default_bottom.strip() or preset.get("bottom", ""),
        "footwear": default_footwear.strip() or preset.get("footwear", ""),
        "outerwear": default_outerwear.strip() or preset.get("outerwear", ""),
        "one_piece": default_one_piece.strip() or preset.get("one_piece", ""),
        "swimwear_top": default_swimwear_top.strip() or preset.get("swimwear_top", ""),
        "swimwear_bottom": default_swimwear_bottom.strip() or preset.get("swimwear_bottom", ""),
        "raw": exact_default_clothing.strip(),
        "notes": outfit_notes.strip(),
    }

    if components["raw"]:
        components["kind"] = _infer_outfit_kind(components["raw"])

    kind = components["kind"]
    if kind == "clinical":
        return "unclothed adult subject in neutral clinical anatomy documentation", components

    if components["raw"]:
        if kind == "swimwear":
            prompt = _join(
                f"fully wearing a matching two-piece swimwear set described as {components['raw']}",
                "a fitted swimwear top and matching swimwear bottoms are both present",
                "realistic fabric edges, straps, seams, and tension",
                components["notes"],
            )
        elif kind == "one_piece":
            prompt = _join(
                f"fully wearing the one-piece garment described as {components['raw']}",
                components["footwear"] and f"with {components['footwear']}",
                components["notes"],
            )
        else:
            prompt = _join(
                f"fully dressed in the complete outfit described as {components['raw']}",
                components["notes"],
            )
        return prompt, components

    if kind == "swimwear":
        prompt = _join(
            "fully wearing a matching two-piece swimwear set",
            components["swimwear_top"],
            components["swimwear_bottom"],
            "realistic fabric edges, straps, seams, and tension",
            components["notes"],
        )
    elif kind == "one_piece":
        prompt = _join(
            "fully wearing a complete one-piece outfit",
            components["one_piece"],
            components["outerwear"],
            components["footwear"],
            components["notes"],
        )
    elif kind == "complete":
        prompt = _join(
            "fully dressed in a complete outfit consisting of",
            components["top"],
            components["bottom"],
            components["outerwear"],
            components["footwear"],
            components["notes"],
        )
    else:
        prompt = components["notes"]
    return prompt, components


def _override_components(
    exact_outfit: str,
    exact_top: str,
    exact_bottom: str,
    exact_footwear: str,
    exact_outerwear: str,
    outfit_coverage: str,
) -> dict[str, str]:
    raw = exact_outfit.strip()
    inferred_kind = _infer_outfit_kind(raw)
    if outfit_coverage == "Swimwear Set":
        kind = "swimwear"
    elif outfit_coverage == "One-Piece Garment":
        kind = "one_piece"
    elif outfit_coverage in {"Upper-Body Garment", "Lower-Body Garment", "Complete Outfit"}:
        kind = "complete"
    else:
        kind = inferred_kind

    return {
        "kind": kind,
        "top": exact_top.strip(),
        "bottom": exact_bottom.strip(),
        "footwear": exact_footwear.strip(),
        "outerwear": exact_outerwear.strip(),
        "one_piece": raw if kind == "one_piece" else "",
        "swimwear_top": exact_top.strip(),
        "swimwear_bottom": exact_bottom.strip(),
        "raw": raw,
        "notes": "",
    }


def _component_phrase(components: dict[str, str]) -> str:
    kind = components.get("kind", "complete")
    raw = components.get("raw", "")
    if raw:
        if kind == "swimwear":
            return _join(
                f"fully wearing a matching two-piece swimwear set described as {raw}",
                components.get("top") or "a fitted swimwear top",
                components.get("bottom") or "matching swimwear bottoms",
                "realistic fabric edges, straps, seams, and tension",
            )
        if kind == "one_piece":
            return _join(f"fully wearing the one-piece garment described as {raw}", components.get("footwear"))
        return _join(f"fully dressed in the complete outfit described as {raw}", components.get("top"), components.get("bottom"), components.get("outerwear"), components.get("footwear"))

    if kind == "swimwear":
        return _join(
            "fully wearing a matching two-piece swimwear set",
            components.get("swimwear_top") or components.get("top") or "fitted swimwear top",
            components.get("swimwear_bottom") or components.get("bottom") or "matching swimwear bottoms",
            "realistic fabric edges, straps, seams, and tension",
        )
    if kind == "one_piece":
        return _join("fully wearing a complete one-piece outfit", components.get("one_piece"), components.get("outerwear"), components.get("footwear"))
    return _join(
        "fully dressed in a complete outfit consisting of",
        components.get("top"), components.get("bottom"), components.get("outerwear"), components.get("footwear"),
    )


def _crop_outfit_prompt(
    base_prompt: str,
    components: dict[str, str],
    shot_type: str,
    body_region: str,
    priority: str,
) -> tuple[str, str]:
    if not base_prompt:
        return "", ""

    kind = components.get("kind", "complete")
    top = components.get("top") or components.get("swimwear_top") or (components.get("raw") if kind != "one_piece" else "")
    bottom = components.get("bottom") or components.get("swimwear_bottom")
    footwear = components.get("footwear")
    one_piece = components.get("one_piece") or (components.get("raw") if kind == "one_piece" else "")

    if shot_type == "Face Close-Up":
        if kind == "swimwear":
            crop = "the swimwear-top straps and neckline are clearly visible at the lower edge of the portrait"
        elif kind == "one_piece":
            crop = f"the neckline and shoulder area of {one_piece or 'the one-piece garment'} are clearly visible at the lower edge of the portrait"
        else:
            crop = f"the neckline and upper shoulder area of {top or 'the selected upper-body garment'} are clearly visible at the lower edge of the portrait"
    elif shot_type == "Head and Shoulders":
        if kind == "swimwear":
            crop = "the swimwear top neckline and both straps are clearly visible across the shoulders and upper chest"
        elif kind == "one_piece":
            crop = f"the upper portion, neckline, and shoulders of {one_piece or 'the one-piece garment'} are clearly visible"
        else:
            crop = f"the upper portion, neckline, shoulders, and sleeves or straps of {top or 'the selected upper-body garment'} are clearly visible"
    elif shot_type == "Chest-Up":
        if kind == "swimwear":
            crop = "the complete swimwear top is clearly visible across the chest with both sides, straps, neckline, and fabric edges present"
        elif kind == "one_piece":
            crop = f"the complete upper portion of {one_piece or 'the one-piece garment'} is clearly visible across the chest and upper torso"
        else:
            crop = f"the complete {top or 'upper-body garment'} is clearly visible across the chest and upper torso with neckline, seams, sleeves or straps, and fabric edges present"
    elif shot_type == "Waist-Up Midshot":
        if kind == "swimwear":
            crop = "the complete swimwear top and the upper edge of the matching swimwear bottoms are clearly visible"
        elif kind == "one_piece":
            crop = f"the upper and waist portions of {one_piece or 'the one-piece garment'} are clearly visible"
        else:
            crop = _join(
                f"the complete {top or 'upper-body garment'} is visible",
                f"the waistband or upper edge of {bottom or 'the matching lower-body garment'} is visible at the waist",
            )
    elif shot_type == "Three-Quarter Body":
        if kind == "swimwear":
            crop = "the complete matching swimwear top and swimwear bottoms are both clearly visible in the frame"
        elif kind == "one_piece":
            crop = f"the complete {one_piece or 'one-piece garment'} is clearly visible from shoulders through below the knees"
        else:
            crop = _join(
                f"the complete {top or 'upper-body garment'} and {bottom or 'lower-body garment'} are clearly visible",
                "the outfit remains continuous through the waist, hips, and legs",
            )
    elif shot_type == "Full Body":
        if kind == "swimwear":
            crop = "the complete matching swimwear top and swimwear bottoms are both clearly visible from head to feet"
        elif kind == "one_piece":
            crop = _join(
                f"the complete {one_piece or 'one-piece garment'} is clearly visible from head to feet",
                footwear and f"the {footwear} are visible",
            )
        else:
            crop = _join(
                f"the complete {top or 'upper-body garment'} and {bottom or 'lower-body garment'} are clearly visible",
                footwear and f"the {footwear} are visible",
                "the full outfit remains continuous from shoulders through the feet",
            )
    else:
        region = body_region.lower()
        if any(token in region for token in ("upper", "chest", "ribcage", "shoulder")):
            crop = f"the selected upper-body garment is clearly visible across the documented {region} region"
        elif any(token in region for token in ("abdomen", "waist", "hip", "lower")):
            crop = f"the waistband and lower-body garment are clearly visible across the documented {region} region"
        else:
            crop = "the requested garment remains clearly visible across the selected body-documentation region"

    final_lock = ""
    if priority in {"Strong", "Maximum"}:
        final_lock = "garment visibility confirmation: the requested outfit remains clearly visible in the selected crop"
    if priority == "Maximum":
        final_lock = _join(final_lock, "the selected clothing is the dominant wardrobe state in this image")
    return _join(base_prompt, crop), final_lock


def _resolve_body_mode(stage: str, clothing_mode: str, body_detail_mode: str) -> str:
    if clothing_mode == "Clinical Unclothed":
        return "Clinical Anatomy"
    if clothing_mode in {"Exact Outfit Override", "Preserve Reference Clothing"}:
        return "Clothed Silhouette"
    if body_detail_mode != "Auto by Stage":
        return body_detail_mode
    if stage in {"Qwen Anatomy Documentation", "Qwen Body Close-Up"}:
        return "Clinical Anatomy"
    return "Clothed Silhouette"


class CharacterBlueprintCreator:
    CATEGORY = "character creation/core"
    FUNCTION = "build_blueprint"
    DESCRIPTION = "Creates a reusable adult character blueprint with separate clothed-silhouette, clinical-anatomy, markings, and structured outfit prompts."

    RETURN_TYPES = (
        "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",
        "CHARACTER_BLUEPRINT", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",
    )
    RETURN_NAMES = (
        "face_identity", "upper_body_identity", "lower_body_identity", "bust_prompt", "marks_prompt",
        "default_clothing_prompt", "full_profile_prompt", "character_id", "character_blueprint", "warnings",
        "clothed_upper_body", "anatomy_upper_body", "clothed_lower_body", "anatomy_lower_body",
        "structured_outfit_prompt",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gender": (GENDERS, {"default": "Adult Female"}),
                "age_range": (AGE_RANGES, {"default": "25–34"}),
                "heritage": (HERITAGES, {"default": "Unspecified"}),
                "skin_tone": (SKIN_TONES, {"default": "Light"}),
                "complexion": (COMPLEXIONS, {"default": "Natural Skin Texture"}),
                "face_shape": (FACE_SHAPES, {"default": "Oval"}),
                "jaw_shape": (JAW_SHAPES, {"default": "Defined"}),
                "chin_shape": (CHIN_SHAPES, {"default": "Rounded"}),
                "eye_color": (EYE_COLORS, {"default": "Hazel"}),
                "eye_shape": (EYE_SHAPES, {"default": "Almond"}),
                "eyebrow_shape": (EYEBROWS, {"default": "Soft Arch"}),
                "nose_shape": (NOSES, {"default": "Straight"}),
                "lip_shape": (LIPS, {"default": "Balanced Medium"}),
                "hair_color": (HAIR_COLORS, {"default": "Medium Brown"}),
                "hair_length": (HAIR_LENGTHS, {"default": "Shoulder-Length"}),
                "hair_texture": (HAIR_TEXTURES, {"default": "Slightly Wavy"}),
                "hair_style": (HAIR_STYLES, {"default": "Loose Natural"}),
                "height": (HEIGHTS, {"default": "Average"}),
                "body_type": (BODY_TYPES, {"default": "Average"}),
                "bust_size": (BUST_SIZES, {"default": "Medium"}),
                "bust_shape": (BUST_SHAPES, {"default": "Teardrop"}),
                "bust_position": (BUST_POSITIONS, {"default": "Natural Average-Set"}),
                "bust_firmness": (BUST_FIRMNESS, {"default": "Balanced Natural"}),
                "bust_augmentation": (BUST_AUGMENTATION, {"default": "Natural / Unaugmented"}),
                "buttocks": (BUTTOCKS, {"default": "Average"}),
                "default_clothing": (DEFAULT_CLOTHING, {"default": "Simple Fitted T-Shirt"}),
                "jewelry_level": (JEWELRY_LEVELS, {"default": "Minimal"}),
                "tattoo_status": (MARK_STATUSES, {"default": "None"}),
                "piercing_status": (MARK_STATUSES, {"default": "None"}),
            },
            "optional": {
                "custom_heritage": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_color": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_length": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_texture": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_style": ("STRING", {"default": "", "multiline": False}),
                "exact_default_clothing": ("STRING", {"default": "", "multiline": True}),
                "jewelry_description": ("STRING", {"default": "", "multiline": True}),
                "tattoo_descriptors": ("STRING", {"default": "", "multiline": True, "placeholder": "One tattoo per line, including exact location"}),
                "piercing_descriptors": ("STRING", {"default": "", "multiline": True, "placeholder": "One piercing per line, including exact location and jewelry"}),
                "lower_body_notes": ("STRING", {"default": "", "multiline": True}),
                "custom_identity_notes": ("STRING", {"default": "", "multiline": True}),
                "default_top": ("STRING", {"default": "", "multiline": False, "placeholder": "Optional structured top override"}),
                "default_bottom": ("STRING", {"default": "", "multiline": False, "placeholder": "Optional structured bottom override"}),
                "default_footwear": ("STRING", {"default": "", "multiline": False, "placeholder": "Optional footwear override"}),
                "default_outerwear": ("STRING", {"default": "", "multiline": False, "placeholder": "Optional outerwear"}),
                "default_one_piece": ("STRING", {"default": "", "multiline": False, "placeholder": "Optional dress, bodysuit, romper, or jumpsuit"}),
                "default_swimwear_top": ("STRING", {"default": "", "multiline": False}),
                "default_swimwear_bottom": ("STRING", {"default": "", "multiline": False}),
                "outfit_notes": ("STRING", {"default": "", "multiline": True}),
            },
        }

    def build_blueprint(
        self, gender, age_range, heritage, skin_tone, complexion, face_shape, jaw_shape, chin_shape,
        eye_color, eye_shape, eyebrow_shape, nose_shape, lip_shape, hair_color, hair_length, hair_texture,
        hair_style, height, body_type, bust_size, bust_shape, bust_position, bust_firmness,
        bust_augmentation, buttocks, default_clothing, jewelry_level, tattoo_status, piercing_status,
        custom_heritage="", custom_hair_color="", custom_hair_length="", custom_hair_texture="",
        custom_hair_style="", exact_default_clothing="", jewelry_description="", tattoo_descriptors="",
        piercing_descriptors="", lower_body_notes="", custom_identity_notes="", default_top="",
        default_bottom="", default_footwear="", default_outerwear="", default_one_piece="",
        default_swimwear_top="", default_swimwear_bottom="", outfit_notes="",
    ):
        heritage_prompt = _heritage_prompt(heritage, custom_heritage)
        face_identity = _join(
            "adult subject", gender.lower(), f"age range {age_range}", heritage_prompt,
            f"{skin_tone.lower()} skin tone" if skin_tone != "Custom / Unspecified" else "",
            complexion.lower() if complexion != "Unspecified" else "",
            f"{face_shape.lower()} face", f"{jaw_shape.lower()} jaw", f"{chin_shape.lower()} chin",
            f"{eye_color.lower()} eyes" if eye_color != "Custom / Unspecified" else "",
            f"{eye_shape.lower()} eye shape", f"{eyebrow_shape.lower()} eyebrows",
            f"{nose_shape.lower()} nose", f"{lip_shape.lower()} lips",
            _hair_value(hair_color, custom_hair_color, "hair"),
            _hair_value(hair_length, custom_hair_length, "hair length"),
            _hair_value(hair_texture, custom_hair_texture, "hair texture"),
            _hair_value(hair_style, custom_hair_style, "hairstyle"),
            custom_identity_notes,
        )

        bust_prompt = _bust_prompt(gender, bust_size, bust_shape, bust_position, bust_firmness, bust_augmentation)
        clothed_bust = _clothed_bust_prompt(gender, bust_size, bust_shape, bust_position)

        anatomy_upper_body = _join(
            f"{height.lower()} height" if height != "Unspecified" else "",
            f"{body_type.lower()} body type" if body_type != "Custom / Unspecified" else "",
            bust_prompt,
        )
        clothed_upper_body = _join(
            f"{height.lower()} height" if height != "Unspecified" else "",
            f"{body_type.lower()} body type" if body_type != "Custom / Unspecified" else "",
            clothed_bust,
        )
        anatomy_lower_body = _join(
            f"{buttocks.lower()} buttocks" if buttocks != "Unspecified" else "",
            lower_body_notes,
        )
        clothed_lower_body = _join(
            f"{buttocks.lower()} lower-body and gluteal silhouette" if buttocks != "Unspecified" else "",
            "balanced hip, waist, and leg proportions",
        )

        tattoo_prompt, tattoo_entries, tattoo_warning = _marks_prompt("Tattoo", tattoo_status, tattoo_descriptors)
        piercing_prompt, piercing_entries, piercing_warning = _marks_prompt("Piercing", piercing_status, piercing_descriptors)
        marks_prompt = _join(tattoo_prompt, piercing_prompt)

        structured_outfit_prompt, outfit_components = _build_profile_outfit(
            default_clothing, exact_default_clothing, default_top, default_bottom,
            default_footwear, default_outerwear, default_one_piece,
            default_swimwear_top, default_swimwear_bottom, outfit_notes,
        )
        jewelry_prompt = "" if jewelry_level == "None" else _join(f"{jewelry_level.lower()} jewelry", jewelry_description)
        default_clothing_prompt = _join(structured_outfit_prompt, jewelry_prompt)

        upper_body_identity = anatomy_upper_body
        lower_body_identity = anatomy_lower_body
        full_profile_prompt = _join(face_identity, marks_prompt, anatomy_upper_body, anatomy_lower_body, default_clothing_prompt)
        base_id = _join(gender, age_range, heritage, face_shape, hair_color, body_type, bust_size)
        character_id = _slug(base_id) + "_" + hashlib.sha1(full_profile_prompt.encode("utf-8")).hexdigest()[:8]

        warnings = " ".join(x for x in [tattoo_warning, piercing_warning] if x)
        if bust_position == "High and Tight" and bust_firmness in {"Soft", "Very Soft / Natural Movement"}:
            warnings = _join(warnings, "High and Tight conflicts with the selected soft-tissue setting.")
        if outfit_components.get("kind") == "complete" and not outfit_components.get("raw"):
            if not outfit_components.get("top") or not outfit_components.get("bottom"):
                warnings = _join(warnings, "Complete outfit is missing a top or bottom component.")

        blueprint = {
            "schema": "CHARACTER_BLUEPRINT",
            "schema_version": 2,
            "character_id": character_id,
            "gender": gender,
            "age_range": age_range,
            "heritage": heritage,
            "heritage_prompt": heritage_prompt,
            "face_identity": face_identity,
            "upper_body_identity": anatomy_upper_body,
            "lower_body_identity": anatomy_lower_body,
            "anatomy_upper_body": anatomy_upper_body,
            "clothed_upper_body": clothed_upper_body,
            "anatomy_lower_body": anatomy_lower_body,
            "clothed_lower_body": clothed_lower_body,
            "bust_prompt": bust_prompt,
            "marks_prompt": marks_prompt,
            "tattoo_entries": tattoo_entries,
            "piercing_entries": piercing_entries,
            "default_clothing_prompt": default_clothing_prompt,
            "structured_outfit_prompt": structured_outfit_prompt,
            "outfit_components": outfit_components,
            "jewelry_prompt": jewelry_prompt,
            "full_profile_prompt": full_profile_prompt,
            "warnings": warnings,
        }

        return (
            face_identity, anatomy_upper_body, anatomy_lower_body, bust_prompt, marks_prompt,
            default_clothing_prompt, full_profile_prompt, character_id, blueprint, warnings,
            clothed_upper_body, anatomy_upper_body, clothed_lower_body, anatomy_lower_body,
            structured_outfit_prompt,
        )


class CharacterShotPlanner:
    CATEGORY = "character creation/core"
    FUNCTION = "plan_shot"
    DESCRIPTION = "Builds stage-specific Krea and Qwen prompts with authoritative crop-aware clothing or clinical anatomy routing."

    RETURN_TYPES = (
        "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",
        "INT", "INT", "STRING", "STRING", "STRING", "STRING", "STRING",
    )
    RETURN_NAMES = (
        "krea_prompt", "qwen_prompt", "shot_prompt", "clothing_prompt", "marks_prompt",
        "reference_required", "shot_id", "recommended_width", "recommended_height",
        "profile_character_id", "planner_notes", "effective_body_detail_mode",
        "outfit_visibility_lock", "outfit_components_prompt",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "stage": (STAGES, {"default": "Krea Identity Anchor"}),
                "shot_type": (SHOT_TYPES, {"default": "Face Close-Up"}),
                "camera_view": (CAMERA_VIEWS, {"default": "Front View"}),
                "pose": (POSES, {"default": "Neutral Standing"}),
                "expression": (EXPRESSIONS, {"default": "Neutral"}),
                "clothing_mode": (CLOTHING_MODES, {"default": "Profile Default"}),
                "body_region": (BODY_REGIONS, {"default": "Upper Torso"}),
                "background": (BACKGROUNDS, {"default": "Plain Neutral"}),
                "lighting": (LIGHTING, {"default": "Soft Natural Daylight"}),
                "photo_style": (PHOTO_STYLES, {"default": "Authentic Consumer Camera"}),
            },
            "optional": {
                "character_blueprint": ("CHARACTER_BLUEPRINT",),
                "exact_outfit": ("STRING", {"default": "", "multiline": True}),
                "custom_pose": ("STRING", {"default": "", "multiline": True}),
                "custom_expression": ("STRING", {"default": "", "multiline": False}),
                "custom_body_region": ("STRING", {"default": "", "multiline": True}),
                "custom_background": ("STRING", {"default": "", "multiline": True}),
                "custom_lighting": ("STRING", {"default": "", "multiline": True}),
                "trigger_word": ("STRING", {"default": "", "multiline": False}),
                "custom_suffix": ("STRING", {"default": "", "multiline": True}),
                "body_detail_mode": (BODY_DETAIL_MODES, {"default": "Auto by Stage"}),
                "outfit_coverage": (OUTFIT_COVERAGE, {"default": "Auto by Shot"}),
                "clothing_priority": (CLOTHING_PRIORITIES, {"default": "Strong"}),
                "exact_top": ("STRING", {"default": "", "multiline": False}),
                "exact_bottom": ("STRING", {"default": "", "multiline": False}),
                "exact_footwear": ("STRING", {"default": "", "multiline": False}),
                "exact_outerwear": ("STRING", {"default": "", "multiline": False}),
            },
        }

    def plan_shot(
        self, stage, shot_type, camera_view, pose, expression, clothing_mode, body_region,
        background, lighting, photo_style, character_blueprint=None, exact_outfit="",
        custom_pose="", custom_expression="", custom_body_region="", custom_background="",
        custom_lighting="", trigger_word="", custom_suffix="", body_detail_mode="Auto by Stage",
        outfit_coverage="Auto by Shot", clothing_priority="Strong", exact_top="",
        exact_bottom="", exact_footwear="", exact_outerwear="",
    ):
        profile = character_blueprint if isinstance(character_blueprint, dict) else {}
        face = profile.get("face_identity", "adult subject")
        marks = profile.get("marks_prompt", "")
        anatomy_upper = profile.get("anatomy_upper_body", profile.get("upper_body_identity", ""))
        clothed_upper = profile.get("clothed_upper_body", profile.get("upper_body_identity", ""))
        anatomy_lower = profile.get("anatomy_lower_body", profile.get("lower_body_identity", ""))
        clothed_lower = profile.get("clothed_lower_body", "")
        default_clothing = profile.get("default_clothing_prompt", "")
        default_components = profile.get("outfit_components", {}) if isinstance(profile.get("outfit_components"), dict) else {}
        character_id = profile.get("character_id", "character")

        shot_prompt = _join(SHOT_PROMPTS[shot_type], CAMERA_PROMPTS[camera_view])
        region = custom_body_region.strip() if body_region == "Custom" and custom_body_region.strip() else body_region
        if shot_type == "Body Close-Up":
            shot_prompt = _join(shot_prompt, f"focused on {region.lower()}")

        pose_prompt = custom_pose.strip() if pose == "Custom" and custom_pose.strip() else pose.lower()
        expression_prompt = custom_expression.strip() if expression == "Custom" and custom_expression.strip() else expression.lower() + " expression"
        background_prompt = custom_background.strip() if background == "Custom" and custom_background.strip() else background.lower() + " background"
        lighting_prompt = custom_lighting.strip() if lighting == "Custom" and custom_lighting.strip() else lighting.lower()
        style_prompt = photo_style.lower()

        effective_body_mode = _resolve_body_mode(stage, clothing_mode, body_detail_mode)

        if clothing_mode == "Clinical Unclothed":
            clothing_base = "unclothed adult subject in neutral clinical anatomy documentation"
            components = {"kind": "clinical"}
            clothing_prompt = clothing_base
            outfit_lock = ""
        elif clothing_mode == "Preserve Reference Clothing":
            clothing_base = "preserve the complete clothing already visible in Image 1"
            components = {"kind": "preserve"}
            clothing_prompt = clothing_base
            outfit_lock = "the same complete reference outfit remains visible in the selected crop"
        elif clothing_mode == "Exact Outfit Override":
            components = _override_components(
                exact_outfit, exact_top, exact_bottom, exact_footwear, exact_outerwear,
                outfit_coverage,
            )
            clothing_base = _component_phrase(components)
            clothing_prompt, outfit_lock = _crop_outfit_prompt(
                clothing_base, components, shot_type, region, clothing_priority,
            )
        else:
            components = default_components or {"kind": "complete", "raw": default_clothing}
            clothing_base = default_clothing or _component_phrase(components)
            clothing_prompt, outfit_lock = _crop_outfit_prompt(
                clothing_base, components, shot_type, region, clothing_priority,
            )

        face_only = shot_type in {"Face Close-Up", "Head and Shoulders"}
        upper_visible = shot_type in {"Chest-Up", "Waist-Up Midshot", "Three-Quarter Body", "Full Body", "Body Close-Up"}
        lower_visible = shot_type in {"Three-Quarter Body", "Full Body", "Body Close-Up"}

        upper = anatomy_upper if effective_body_mode == "Clinical Anatomy" else clothed_upper
        lower = anatomy_lower if effective_body_mode == "Clinical Anatomy" else clothed_lower

        visible_upper = "" if face_only else upper
        visible_lower = lower if lower_visible else ""

        # Clothing is deliberately placed immediately after framing so it is not buried after anatomy.
        krea_prompt = _join(
            trigger_word,
            shot_prompt,
            clothing_prompt,
            pose_prompt,
            expression_prompt,
            face,
            marks,
            visible_upper,
            visible_lower,
            background_prompt,
            lighting_prompt,
            style_prompt,
            outfit_lock,
            custom_suffix,
        )

        if stage == "Krea Identity Anchor":
            reference = "None — text-to-image"
            qwen_prompt = ""
            planner_notes = _join(
                "Krea identity anchor uses crop-relevant identity traits",
                f"body detail mode: {effective_body_mode}",
                "clothing is placed immediately after framing and is crop-aware",
            )
        elif stage == "Qwen Face Documentation":
            reference = "Portrait Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic photograph of the same adult person",
                "preserve the exact recognizable face, hair, skin characteristics, and permanent facial markings from Image 1",
                shot_prompt,
                clothing_prompt,
                pose_prompt,
                expression_prompt,
                face,
                marks,
                background_prompt,
                lighting_prompt,
                style_prompt,
                outfit_lock,
                "keep natural skin texture, realistic moist eyes, ordinary camera sharpness, and believable hair strands",
                custom_suffix,
            )
            planner_notes = "Uses only face, hair, expression, camera, visible clothing, and permanent markings."
        elif stage == "Qwen Upper-Body Anchor":
            reference = "Portrait Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic upper-body photograph of the same adult person",
                "preserve the exact recognizable face and hair from Image 1",
                shot_prompt,
                clothing_prompt,
                pose_prompt,
                expression_prompt,
                face,
                marks,
                upper,
                background_prompt,
                lighting_prompt,
                style_prompt,
                outfit_lock,
                "establish consistent shoulders, chest, torso, arms, and natural waist while preserving identity",
                custom_suffix,
            )
            planner_notes = _join("Introduces upper-body traits", f"body detail mode: {effective_body_mode}")
        elif stage == "Qwen Anatomy Documentation":
            reference = "Portrait or Anatomy Anchor"
            clinical_clothing = "unclothed adult subject in neutral clinical anatomy documentation"
            qwen_prompt = _join(
                "Edit Image 1 into neutral adult clinical anatomy documentation of the same person",
                "preserve exact face, hair, body proportions, tattoos, and piercings",
                shot_prompt,
                clinical_clothing,
                pose_prompt,
                face,
                marks,
                anatomy_upper,
                anatomy_lower if lower_visible else "",
                background_prompt,
                lighting_prompt,
                "clinical documentation photography",
                custom_suffix,
            )
            effective_body_mode = "Clinical Anatomy"
            planner_notes = "Clinical anatomy mode uses the full anatomy description and excludes clothing."
        elif stage == "Qwen Clothing Edit":
            reference = "Anatomy or Clothed Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic wardrobe photograph of the same adult person",
                "preserve the exact face, hair, body shape, chest proportions, waist, tattoos, and piercings from Image 1",
                shot_prompt,
                clothing_prompt,
                pose_prompt,
                expression_prompt,
                face,
                marks,
                clothed_upper,
                clothed_lower if lower_visible else "",
                background_prompt,
                lighting_prompt,
                style_prompt,
                outfit_lock,
                "render realistic fabric, seams, folds, edges, straps, waistbands, and garment tension",
                custom_suffix,
            )
            effective_body_mode = "Clothed Silhouette"
            planner_notes = "Wardrobe edit uses clothed silhouette only; anatomy-only lower-body notes are excluded."
        elif stage == "Qwen Body Close-Up":
            reference = "Anatomy Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into focused adult body-documentation photography of the same person",
                "preserve exact body proportions, skin characteristics, tattoos, and piercings",
                shot_prompt,
                clothing_prompt,
                pose_prompt,
                anatomy_upper if upper_visible else "",
                anatomy_lower if lower_visible else "",
                marks,
                background_prompt,
                lighting_prompt,
                "clinical documentation photography",
                custom_suffix,
            )
            planner_notes = "Body close-up uses anatomy details and the selected body region."
        else:
            reference = "Mini LoRA loaded in Krea model lane"
            qwen_prompt = ""
            planner_notes = _join(
                "Krea mini-LoRA expansion uses the targeted face and body profile",
                f"body detail mode: {effective_body_mode}",
                "clothing is authoritative and crop-aware",
            )

        if shot_type == "Face Close-Up":
            width, height = 1024, 1024
        elif shot_type in {"Head and Shoulders", "Chest-Up", "Waist-Up Midshot", "Body Close-Up"}:
            width, height = 1024, 1280
        else:
            width, height = 1024, 1536

        shot_id = _slug(_join(character_id, stage, shot_type, camera_view, pose, clothing_mode))
        return (
            krea_prompt, qwen_prompt, shot_prompt, clothing_prompt, marks, reference, shot_id,
            width, height, character_id, planner_notes, effective_body_mode, outfit_lock,
            _component_phrase(components) if components.get("kind") not in {"clinical", "preserve"} else clothing_base,
        )
