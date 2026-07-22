from __future__ import annotations

import hashlib
import re
from typing import List

from .prompt_data import (
    GENDERS,
    AGE_RANGES,
    SKIN_TONES,
    COMPLEXIONS,
    FACE_SHAPES,
    JAW_SHAPES,
    CHIN_SHAPES,
    EYE_COLORS,
    EYE_SHAPES,
    EYEBROW_SHAPES,
    NOSE_SHAPES,
    LIP_SHAPES,
    HAIR_COLORS,
    HAIR_LENGTHS,
    HAIR_TEXTURES,
    HAIR_STYLES,
    HIGHLIGHT_STYLES,
    HIGHLIGHT_COLORS,
    HEIGHTS,
    BODY_TYPES,
    BRA_BANDS,
    CUP_SIZES,
    BREAST_SHAPES,
    BREAST_SHAPE_PROMPTS,
    BREAST_POSITIONS,
    BREAST_POSITION_PROMPTS,
    BREAST_FIRMNESS,
    BREAST_FIRMNESS_PROMPTS,
    BREAST_AUGMENTATION,
    BREAST_AUGMENTATION_PROMPTS,
    MALE_GROIN_SIZES,
    FEMALE_GROIN_DESCRIPTIONS,
    BUTTOCKS,
    CLOTHING_CATEGORIES,
    ALL_CLOTHING_STYLES,
    JEWELRY_LEVELS,
    JEWELRY_ITEMS,
    JEWELRY_MATERIALS,
    TATTOO_STATUSES,
    TATTOO_LOCATIONS,
    PIERCING_STATUSES,
    PIERCING_LOCATIONS,
    ALL_PIERCING_TYPES,
    NEGATIVE_PRESETS,
    SHOT_TYPES,
    CAMERA_VIEWS,
    SHOT_NEGATIVES,
)


def _clean_join(parts: List[str]) -> str:
    return ", ".join(part.strip(" ,") for part in parts if part and part.strip(" ,"))


def _slug(text: str) -> str:
    value = text.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _selected(label: str, value: str) -> str:
    if not value or value.lower().startswith(("unspecified", "custom / unspecified")):
        return ""
    return f"{value.lower()} {label}"


def _hair_color_prompt(hair_color: str, custom_hair_color: str) -> str:
    custom = custom_hair_color.strip()
    if hair_color in {"Custom", "Vivid / Fantasy Color"} and custom:
        return f"{custom} hair"
    if hair_color == "Custom":
        return ""
    return f"{hair_color.lower()} hair"


def _highlight_prompt(highlight_style: str, highlight_color: str, custom_highlight_color: str) -> str:
    if highlight_style == "None":
        return ""
    custom = custom_highlight_color.strip()
    color = custom if custom else highlight_color
    if color in {"Custom", "Custom / Unspecified"}:
        color = ""
    return _clean_join([
        highlight_style.lower(),
        f"{color.lower()} highlight color" if color else "",
    ])



def _breast_prompt(
    gender: str,
    bra_band: str,
    cup_size: str,
    breast_shape: str,
    breast_position: str,
    breast_firmness: str,
    breast_augmentation: str,
) -> str:
    if gender != "Adult Female":
        return ""

    size_prompt = ""
    if bra_band != "Unspecified" and cup_size != "Unspecified":
        size_prompt = f"proportionate {bra_band} {cup_size} cup bust"
    elif cup_size != "Unspecified":
        size_prompt = f"proportionate {cup_size} cup bust"

    return _clean_join([
        size_prompt,
        BREAST_SHAPE_PROMPTS.get(breast_shape, ""),
        BREAST_POSITION_PROMPTS.get(breast_position, ""),
        BREAST_FIRMNESS_PROMPTS.get(breast_firmness, ""),
        BREAST_AUGMENTATION_PROMPTS.get(breast_augmentation, ""),
        (
            "realistic adult breast anatomy with natural chest attachment, believable weight, "
            "and anatomically consistent left-right placement"
            if any(
                value != "Unspecified"
                for value in (
                    breast_shape,
                    breast_position,
                    breast_firmness,
                    breast_augmentation,
                )
            )
            else ""
        ),
    ])


def _breast_conflict_warning(
    gender: str,
    breast_position: str,
    breast_firmness: str,
    breast_augmentation: str,
) -> str:
    if gender != "Adult Female":
        return ""

    warnings = []

    if (
        breast_position == "High and Tight"
        and breast_firmness in {"Soft", "Very Soft / Natural Movement"}
    ):
        warnings.append(
            "High and Tight conflicts with a soft-tissue setting; expect weaker prompt adherence."
        )

    if (
        breast_position in {"Downward-Sloping", "Pendulous Natural"}
        and breast_augmentation in {
            "Round High-Profile Implants",
            "Very Firm Augmented Projection",
        }
    ):
        warnings.append(
            "Downward or pendulous positioning conflicts with high-profile very-firm augmentation."
        )

    if (
        breast_augmentation == "Very Firm Augmented Projection"
        and breast_firmness in {"Soft", "Very Soft / Natural Movement"}
    ):
        warnings.append(
            "Very Firm Augmented Projection conflicts with the selected soft-tissue setting."
        )

    return " ".join(warnings)


def _anatomy_prompt(
    gender: str,
    bra_band: str,
    cup_size: str,
    breast_shape: str,
    breast_position: str,
    breast_firmness: str,
    breast_augmentation: str,
    male_groin_size: str,
    female_groin_description: str,
    buttocks: str,
) -> str:
    parts = []

    if gender == "Adult Female":
        breast_prompt = _breast_prompt(
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
        )
        if breast_prompt:
            parts.append(breast_prompt)

        if female_groin_description != "Unspecified":
            parts.append(female_groin_description.lower())

    elif gender == "Adult Male":
        if male_groin_size != "Unspecified":
            parts.append(f"{male_groin_size.lower()} external genital profile")

    if buttocks:
        parts.append(f"{buttocks.lower()} buttocks")

    return _clean_join(parts)


def _clothing_prompt(clothing_category: str, clothing_style: str, exact_clothing: str) -> str:
    if clothing_category == "No Clothing / Tattoo Documentation":
        mode_prompts = {
            "Unclothed Tattoo Documentation": (
                "adult subject with no clothing for neutral non-erotic tattoo documentation, "
                "skin surface and tattoo locations unobstructed, no garments covering the body"
            ),
            "Unclothed Full-Body Character Reference": (
                "adult subject with no clothing for a neutral full-body character reference, "
                "entire body surface unobstructed, natural relaxed posture, non-erotic presentation"
            ),
            "Unclothed Neutral Anatomy Reference": (
                "adult subject with no clothing for neutral anatomy reference, "
                "unobstructed body contours and skin surface, non-erotic clinical presentation"
            ),
        }
        return mode_prompts.get(
            clothing_style,
            "adult subject with no clothing for neutral non-erotic character documentation",
        )

    exact = exact_clothing.strip()
    if exact:
        return f"wearing {exact}"
    if clothing_category == "Unspecified" or clothing_style == "Unspecified":
        return ""
    return f"wearing {clothing_style.lower()}, {clothing_category.lower()} clothing"


def _jewelry_prompt(jewelry_level: str, jewelry_item: str, jewelry_material: str, jewelry_notes: str) -> str:
    if jewelry_level == "None":
        return ""
    return _clean_join([
        f"{jewelry_level.lower()} jewelry",
        jewelry_item.lower() if jewelry_item != "None" else "",
        jewelry_material.lower() if jewelry_material != "Unspecified" else "",
        jewelry_notes,
    ])


def _tattoo_prompt(tattoo_status: str, tattoo_location: str, tattoo_description: str) -> str:
    if tattoo_status == "None":
        return ""
    return _clean_join([
        tattoo_status.lower(),
        f"located on the {tattoo_location.lower()}",
        tattoo_description,
    ])


def _piercing_prompt(
    piercing_status: str,
    piercing_location: str,
    piercing_type: str,
    piercing_notes: str,
) -> str:
    if piercing_status == "None":
        return ""
    return _clean_join([
        piercing_status.lower(),
        f"at the {piercing_location.lower()}" if piercing_location != "Unspecified" else "",
        piercing_type.lower() if piercing_type != "Unspecified" else "",
        piercing_notes,
    ])



FACE_ONLY_SHOTS = {
    "Close-Up Face Portrait",
    "Head and Shoulders Portrait",
}

UPPER_BODY_SHOTS = {
    "Chest-Up Portrait",
    "Waist-Up Midshot",
}


def _shot_prompt(shot_type: str, camera_view: str) -> str:
    return _clean_join([
        SHOT_TYPES.get(shot_type, ""),
        CAMERA_VIEWS.get(camera_view, ""),
    ])


def _visible_anatomy_prompt(
    shot_type: str,
    gender: str,
    bra_band: str,
    cup_size: str,
    breast_shape: str,
    breast_position: str,
    breast_firmness: str,
    breast_augmentation: str,
    male_groin_size: str,
    female_groin_description: str,
    buttocks: str,
) -> str:
    if shot_type in FACE_ONLY_SHOTS:
        return ""

    if shot_type in UPPER_BODY_SHOTS:
        return _breast_prompt(
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
        )

    return _anatomy_prompt(
        gender,
        bra_band,
        cup_size,
        breast_shape,
        breast_position,
        breast_firmness,
        breast_augmentation,
        male_groin_size,
        female_groin_description,
        buttocks,
    )


def _visible_identity_blocks(
    shot_type: str,
    body_prompt: str,
    full_anatomy_prompt: str,
    visible_anatomy_prompt: str,
) -> tuple[str, str]:
    if shot_type in FACE_ONLY_SHOTS:
        return "", ""
    return body_prompt, visible_anatomy_prompt



def _upper_anatomy_prompt(
    gender: str,
    bra_band: str,
    cup_size: str,
    breast_shape: str,
    breast_position: str,
    breast_firmness: str,
    breast_augmentation: str,
) -> str:
    return _breast_prompt(
        gender,
        bra_band,
        cup_size,
        breast_shape,
        breast_position,
        breast_firmness,
        breast_augmentation,
    )



def _lower_anatomy_prompt(
    gender: str,
    male_groin_size: str,
    female_groin_description: str,
    buttocks: str,
) -> str:
    parts = []

    if gender == "Adult Female" and female_groin_description != "Unspecified":
        parts.append(female_groin_description.lower())
    elif gender == "Adult Male" and male_groin_size != "Unspecified":
        parts.append(f"{male_groin_size.lower()} external genital profile")

    if buttocks:
        parts.append(f"{buttocks.lower()} buttocks")

    return _clean_join(parts)


class StandardCharacterCreator:
    """Standard Character Creator v1.5."""

    CATEGORY = "prompt/character"
    FUNCTION = "build_character"
    DESCRIPTION = "Creates an adult character identity and outputs a reusable CHARACTER_PROFILE with camera-view rotation and adult chest-shape controls."

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "CHARACTER_PROFILE",
        "STRING",
        "STRING",
    )

    RETURN_NAMES = (
        "combined_prompt",
        "shot_prompt",
        "identity_prompt",
        "face_prompt",
        "hair_prompt",
        "body_prompt",
        "anatomy_prompt",
        "visible_anatomy_prompt",
        "clothing_prompt",
        "jewelry_prompt",
        "tattoo_prompt",
        "piercing_prompt",
        "negative_prompt",
        "character_id",
        "identity_lock_prompt",
        "character_profile",
        "chest_prompt",
        "chest_warning",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shot_type": (list(SHOT_TYPES.keys()), {"default": "Close-Up Face Portrait"}),
                "camera_view": (list(CAMERA_VIEWS.keys()), {"default": "Front View"}),
                "gender": (GENDERS, {"default": "Adult Female"}),
                "age_range": (AGE_RANGES, {"default": "25–34"}),
                "skin_tone": (SKIN_TONES, {"default": "Light"}),
                "complexion": (COMPLEXIONS, {"default": "Natural Skin Texture"}),
                "face_shape": (FACE_SHAPES, {"default": "Oval"}),
                "jaw_shape": (JAW_SHAPES, {"default": "Defined"}),
                "chin_shape": (CHIN_SHAPES, {"default": "Rounded"}),
                "eye_color": (EYE_COLORS, {"default": "Hazel"}),
                "eye_shape": (EYE_SHAPES, {"default": "Almond"}),
                "eyebrow_shape": (EYEBROW_SHAPES, {"default": "Soft Arch"}),
                "nose_shape": (NOSE_SHAPES, {"default": "Straight"}),
                "lip_shape": (LIP_SHAPES, {"default": "Balanced Medium"}),
                "hair_color": (HAIR_COLORS, {"default": "Medium Brown"}),
                "hair_length": (HAIR_LENGTHS, {"default": "Shoulder-Length"}),
                "hair_texture": (HAIR_TEXTURES, {"default": "Slightly Wavy"}),
                "hair_style": (HAIR_STYLES, {"default": "Loose Natural"}),
                "highlight_style": (HIGHLIGHT_STYLES, {"default": "None"}),
                "highlight_color": (HIGHLIGHT_COLORS, {"default": "Golden Blonde"}),
                "height": (HEIGHTS, {"default": "Average"}),
                "body_type": (BODY_TYPES, {"default": "Average"}),
                "bra_band": (BRA_BANDS, {"default": "34"}),
                "cup_size": (CUP_SIZES, {"default": "C"}),
                "male_groin_size": (MALE_GROIN_SIZES, {"default": "Average"}),
                "female_groin_description": (
                    FEMALE_GROIN_DESCRIPTIONS,
                    {"default": "Unspecified"},
                ),
                "buttocks": (BUTTOCKS, {"default": "Average"}),
                "clothing_category": (CLOTHING_CATEGORIES, {"default": "Daily Outdoor"}),
                "clothing_style": (ALL_CLOTHING_STYLES, {"default": "Casual Jeans and Tee"}),
                "jewelry_level": (JEWELRY_LEVELS, {"default": "Minimal"}),
                "jewelry_item": (JEWELRY_ITEMS, {"default": "Stud Earrings"}),
                "jewelry_material": (JEWELRY_MATERIALS, {"default": "Silver"}),
                "tattoo_status": (TATTOO_STATUSES, {"default": "None"}),
                "tattoo_location": (TATTOO_LOCATIONS, {"default": "Upper Arm"}),
                "piercing_status": (PIERCING_STATUSES, {"default": "None"}),
                "piercing_location": (PIERCING_LOCATIONS, {"default": "Ear / Ears"}),
                "piercing_type": (ALL_PIERCING_TYPES, {"default": "Stud"}),
                "negative_preset": (list(NEGATIVE_PRESETS.keys()), {"default": "Standard Character"}),
            },
            "optional": {
                "breast_shape": (
                    BREAST_SHAPES,
                    {"default": "Unspecified"},
                ),
                "breast_position": (
                    BREAST_POSITIONS,
                    {"default": "Unspecified"},
                ),
                "breast_firmness": (
                    BREAST_FIRMNESS,
                    {"default": "Unspecified"},
                ),
                "breast_augmentation": (
                    BREAST_AUGMENTATION,
                    {"default": "Unspecified"},
                ),
                "custom_hair_color": (
                    "STRING",
                    {"default": "", "multiline": False, "placeholder": "Example: electric blue"},
                ),
                "custom_highlight_color": (
                    "STRING",
                    {"default": "", "multiline": False, "placeholder": "Example: silver"},
                ),
                "exact_clothing": (
                    "STRING",
                    {"default": "", "multiline": True, "placeholder": "Exact clothing description"},
                ),
                "jewelry_notes": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "tattoo_description": (
                    "STRING",
                    {"default": "", "multiline": True, "placeholder": "Tattoo design, color, size, style, and placement notes"},
                ),
                "piercing_notes": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "custom_identity_notes": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "custom_prefix": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "custom_suffix": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
                "custom_negative": (
                    "STRING",
                    {"default": "", "multiline": True},
                ),
            },
        }

    def build_character(
        self,
        shot_type,
        camera_view,
        gender,
        age_range,
        skin_tone,
        complexion,
        face_shape,
        jaw_shape,
        chin_shape,
        eye_color,
        eye_shape,
        eyebrow_shape,
        nose_shape,
        lip_shape,
        hair_color,
        hair_length,
        hair_texture,
        hair_style,
        highlight_style,
        highlight_color,
        height,
        body_type,
        bra_band,
        cup_size,
        male_groin_size,
        female_groin_description,
        buttocks,
        clothing_category,
        clothing_style,
        jewelry_level,
        jewelry_item,
        jewelry_material,
        tattoo_status,
        tattoo_location,
        piercing_status,
        piercing_location,
        piercing_type,
        negative_preset,
        breast_shape="Unspecified",
        breast_position="Unspecified",
        breast_firmness="Unspecified",
        breast_augmentation="Unspecified",
        custom_hair_color="",
        custom_highlight_color="",
        exact_clothing="",
        jewelry_notes="",
        tattoo_description="",
        piercing_notes="",
        custom_identity_notes="",
        custom_prefix="",
        custom_suffix="",
        custom_negative="",
    ):
        identity_prompt = _clean_join([
            "adult subject",
            gender.lower() if gender != "Unspecified" else "",
            f"age range {age_range}",
            f"{skin_tone.lower()} skin tone" if skin_tone != "Custom / Unspecified" else "",
            complexion.lower() if complexion != "Unspecified" else "",
            custom_identity_notes,
        ])

        face_prompt = _clean_join([
            f"{face_shape.lower()} face shape",
            f"{jaw_shape.lower()} jaw",
            f"{chin_shape.lower()} chin",
            f"{eye_color.lower()} eyes" if eye_color != "Custom / Unspecified" else "",
            f"{eye_shape.lower()} eye shape",
            f"{eyebrow_shape.lower()} eyebrows",
            f"{nose_shape.lower()} nose",
            f"{lip_shape.lower()} lips",
        ])

        hair_prompt = _clean_join([
            _hair_color_prompt(hair_color, custom_hair_color),
            f"{hair_length.lower()} hair length",
            f"{hair_texture.lower()} hair texture",
            f"{hair_style.lower()} hairstyle",
            _highlight_prompt(highlight_style, highlight_color, custom_highlight_color),
        ])

        body_prompt = _clean_join([
            f"{height.lower()} height" if height != "Unspecified" else "",
            f"{body_type.lower()} body type",
        ])

        full_anatomy_prompt = _anatomy_prompt(
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
            male_groin_size,
            female_groin_description,
            buttocks,
        )

        shot_prompt = _shot_prompt(shot_type, camera_view)

        visible_anatomy_prompt = _visible_anatomy_prompt(
            shot_type,
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
            male_groin_size,
            female_groin_description,
            buttocks,
        )

        visible_body_prompt, visible_anatomy_prompt = _visible_identity_blocks(
            shot_type,
            body_prompt,
            full_anatomy_prompt,
            visible_anatomy_prompt,
        )

        clothing_prompt = _clothing_prompt(
            clothing_category,
            clothing_style,
            exact_clothing,
        )

        jewelry_prompt = _jewelry_prompt(
            jewelry_level,
            jewelry_item,
            jewelry_material,
            jewelry_notes,
        )

        tattoo_prompt = _tattoo_prompt(
            tattoo_status,
            tattoo_location,
            tattoo_description,
        )

        piercing_prompt = _piercing_prompt(
            piercing_status,
            piercing_location,
            piercing_type,
            piercing_notes,
        )

        combined_prompt = _clean_join([
            custom_prefix,
            shot_prompt,
            identity_prompt,
            face_prompt,
            hair_prompt,
            visible_body_prompt,
            visible_anatomy_prompt,
            clothing_prompt,
            tattoo_prompt,
            piercing_prompt,
            jewelry_prompt,
            custom_suffix,
        ])

        unclothed_context_negative = (
            "sexualized pose, erotic framing, fetish presentation, explicit sexual activity"
            if clothing_category == "No Clothing / Tattoo Documentation"
            else ""
        )

        negative_prompt = _clean_join([
            NEGATIVE_PRESETS.get(negative_preset, ""),
            SHOT_NEGATIVES.get(shot_type, ""),
            unclothed_context_negative,
            custom_negative,
        ])

        character_id = "_".join([
            _slug(gender),
            _slug(age_range),
            _slug(face_shape),
            _slug(hair_color if hair_color != "Custom" else custom_hair_color),
            _slug(body_type),
        ])

        anatomy_upper_prompt = _upper_anatomy_prompt(
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
        )

        anatomy_lower_prompt = _lower_anatomy_prompt(
            gender,
            male_groin_size,
            female_groin_description,
            buttocks,
        )

        identity_lock_prompt = _clean_join([
            identity_prompt,
            face_prompt,
            hair_prompt,
            body_prompt,
            full_anatomy_prompt,
            tattoo_prompt,
            piercing_prompt,
        ])

        chest_prompt = _breast_prompt(
            gender,
            bra_band,
            cup_size,
            breast_shape,
            breast_position,
            breast_firmness,
            breast_augmentation,
        )
        chest_warning = _breast_conflict_warning(
            gender,
            breast_position,
            breast_firmness,
            breast_augmentation,
        )

        character_profile = {
            "schema": "CHARACTER_PROFILE",
            "schema_version": 2,
            "character_id": character_id,
            "identity_lock": identity_lock_prompt,
            "identity": identity_prompt,
            "face": face_prompt,
            "hair": hair_prompt,
            "body": body_prompt,
            "anatomy": full_anatomy_prompt,
            "anatomy_upper": anatomy_upper_prompt,
            "anatomy_lower": anatomy_lower_prompt,
            "tattoos": tattoo_prompt,
            "tattoo_status": tattoo_status,
            "tattoo_location": tattoo_location,
            "tattoo_description": tattoo_description.strip(),
            "piercings": piercing_prompt,
            "piercing_status": piercing_status,
            "piercing_location": piercing_location,
            "piercing_type": piercing_type,
            "jewelry": jewelry_prompt,
            "clothing": clothing_prompt,
            "clothing_category": clothing_category,
            "clothing_style": clothing_style,
            "gender": gender,
            "age_range": age_range,
            "skin_tone": skin_tone,
            "complexion": complexion,
            "face_shape": face_shape,
            "jaw_shape": jaw_shape,
            "chin_shape": chin_shape,
            "eye_color": eye_color,
            "eye_shape": eye_shape,
            "hair_color": custom_hair_color.strip() if hair_color == "Custom" else hair_color,
            "hair_length": hair_length,
            "hair_texture": hair_texture,
            "hair_style": hair_style,
            "height": height,
            "body_type": body_type,
            "bra_band": bra_band,
            "cup_size": cup_size,
            "breast_shape": breast_shape,
            "breast_position": breast_position,
            "breast_firmness": breast_firmness,
            "breast_augmentation": breast_augmentation,
            "chest_prompt": chest_prompt,
            "chest_warning": chest_warning,
            "male_groin_size": male_groin_size,
            "female_groin_description": female_groin_description,
            "buttocks": buttocks,
            "source_shot_type": shot_type,
            "source_camera_view": camera_view,
        }

        return (
            combined_prompt,
            shot_prompt,
            identity_prompt,
            face_prompt,
            hair_prompt,
            body_prompt,
            full_anatomy_prompt,
            visible_anatomy_prompt,
            clothing_prompt,
            jewelry_prompt,
            tattoo_prompt,
            piercing_prompt,
            negative_prompt,
            character_id,
            identity_lock_prompt,
            character_profile,
            chest_prompt,
            chest_warning,
        )
