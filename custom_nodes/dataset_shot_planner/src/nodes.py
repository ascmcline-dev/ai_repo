
from __future__ import annotations

import hashlib
import random
import re
from typing import List

from .prompt_data import (
    SHOT_VARIANTS,
    ALL_VARIANTS,
    SHOT_BASE,
    PHOTO_STYLES,
    KREA2_STYLES,
    EXPRESSIONS,
    LIGHTING,
    BACKGROUNDS,
    OUTFITS,
    NEGATIVE_PRESETS,
    GENDERS,
    BODY_TYPES,
    FEMALE_CHEST_SIZES,
    PROMPT_ORDERS,
    OUTFIT_PRIORITIES,
    BODY_VISIBILITY_MODES,
    ANATOMY_PART_FRAMING,
    ANATOMY_PART_NEGATIVES,
)

SHOT_TYPES = list(SHOT_VARIANTS.keys())
PHOTO_STYLE_NAMES = list(PHOTO_STYLES.keys())
EXPRESSION_NAMES = list(EXPRESSIONS.keys())
LIGHTING_NAMES = list(LIGHTING.keys())
BACKGROUND_NAMES = list(BACKGROUNDS.keys())
OUTFIT_NAMES = list(OUTFITS.keys())
NEGATIVE_NAMES = list(NEGATIVE_PRESETS.keys())
GENDER_NAMES = list(GENDERS.keys())
BODY_TYPE_NAMES = list(BODY_TYPES.keys())
BODY_VISIBILITY_NAMES = list(BODY_VISIBILITY_MODES.keys())


PROFILE_USAGE_MODES = [
    "Ignore Profile",
    "Identity Only",
    "Shot-Aware Identity",
    "Full Character Profile",
]

CLOTHING_SOURCES = [
    "Dataset Planner Clothing",
    "Character Creator Clothing",
    "Merge Both",
    "No Clothing / Visibility Mode",
]


CAMERA_VIEW_OPTIONS = [
    "Use Shot Variant Only",
    "Use Character Profile View",
    "Front View",
    "Three-Quarter Left",
    "Three-Quarter Right",
    "Left Profile",
    "Right Profile",
    "Rear Three-Quarter Left",
    "Rear Three-Quarter Right",
    "Back View",
]

CAMERA_VIEW_PROMPTS = {
    "Front View": "front-facing camera view, body and face centered toward the camera",
    "Three-Quarter Left": (
        "three-quarter-left camera view, body and face turned approximately 45 degrees "
        "toward the subject's left, both eyes visible when the face is included"
    ),
    "Three-Quarter Right": (
        "three-quarter-right camera view, body and face turned approximately 45 degrees "
        "toward the subject's right, both eyes visible when the face is included"
    ),
    "Left Profile": "true left-profile camera view, body and face aligned to the left",
    "Right Profile": "true right-profile camera view, body and face aligned to the right",
    "Rear Three-Quarter Left": (
        "rear three-quarter-left camera view, body turned approximately 45 degrees left from the back, "
        "rear and side contours visible"
    ),
    "Rear Three-Quarter Right": (
        "rear three-quarter-right camera view, body turned approximately 45 degrees right from the back, "
        "rear and side contours visible"
    ),
    "Back View": "direct back-facing camera view, rear body proportions and hairstyle visible",
}

_DIRECTION_NEUTRAL_VARIANTS = {
    "Front Neutral": "neutral expression with the head naturally aligned to the body",
    "Front Smiling": "natural relaxed smile with the head naturally aligned to the body",
    "Front Serious": "calm serious expression with the head naturally aligned to the body",
    "45 Degree Left": "neutral portrait pose with the head aligned to the selected camera view",
    "45 Degree Right": "neutral portrait pose with the head aligned to the selected camera view",
    "Profile Left": "neutral portrait pose with the head aligned to the selected camera view",
    "Profile Right": "neutral portrait pose with the head aligned to the selected camera view",
    "Back View": "neutral body pose aligned to the selected camera view",
    "Back 45 Degree Left": "neutral body pose aligned to the selected camera view",
    "Back 45 Degree Right": "neutral body pose aligned to the selected camera view",
    "Standing Front": "standing naturally with relaxed shoulders and balanced posture",
    "Standing Back": "standing naturally with relaxed shoulders and balanced posture",
    "Standing Left Side": "standing naturally with relaxed shoulders and balanced posture",
    "Standing Right Side": "standing naturally with relaxed shoulders and balanced posture",
    "Walking Toward Camera": "walking naturally, mid-step, with the full body visible",
    "Walking Away": "walking naturally, mid-step, with the full body visible",
}


def _clean_join(parts: List[str]) -> str:
    return ", ".join(part.strip(" ,") for part in parts if part and part.strip(" ,"))


def _sentence_join(parts: List[str]) -> str:
    cleaned = [part.strip(" ,.;") for part in parts if part and part.strip(" ,.;")]
    return ". ".join(cleaned) + ("." if cleaned else "")


def _slug(text: str) -> str:
    value = text.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _stable_choice(options: List[str], random_seed: int, salt: str) -> str:
    digest = hashlib.sha256(f"{random_seed}|{salt}".encode("utf-8")).digest()
    picker = random.Random(int.from_bytes(digest[:8], "big"))
    return picker.choice(options)


def _variant_to_prompt(variant: str) -> str:
    direct = {
        "Both Eyes Centered": "camera centered directly on both eyes, both eyes fully visible, symmetrical eye-level view",
        "Left Eye": "extreme close-up of the left eye and surrounding eyelid and eyebrow anatomy",
        "Right Eye": "extreme close-up of the right eye and surrounding eyelid and eyebrow anatomy",
        "Eyebrows": "extreme close-up of both eyebrows and the brow ridge",
        "Forehead": "extreme close-up of the forehead and hairline transition",
        "Nose": "extreme close-up of the nose from a centered frontal view",
        "Mouth and Lips": "extreme close-up of the mouth and lips in a relaxed natural position",
        "Teeth and Smile": "extreme close-up of a natural smile with teeth clearly visible",
        "Teeth": "natural smile with teeth clearly visible",
        "Left Ear": "extreme close-up of the left ear from a clean side angle",
        "Right Ear": "extreme close-up of the right ear from a clean side angle",
        "Jawline": "extreme close-up of the jawline and chin contour",
        "Hairline": "extreme close-up of the front hairline and temple area",
        "Neck Front": "close documentation of the front of the neck and collarbone area",
        "Neck Side": "close documentation of the side of the neck from a three-quarter angle",
        "Toes": "extreme close-up anatomy documentation of the toes, all toes clearly visible, accurate joints and nails, natural proportions, clean unobstructed framing",
        "Front Neutral": "front-facing view, camera centered, neutral expression",
        "Front Smiling": "front-facing view, camera centered, natural relaxed smile",
        "Front Serious": "front-facing view, camera centered, calm serious expression",
        "45 Degree Left": "head turned approximately 45 degrees to the subject's left, both eyes still visible",
        "45 Degree Right": "head turned approximately 45 degrees to the subject's right, both eyes still visible",
        "Profile Left": "true left profile view, face turned 90 degrees",
        "Profile Right": "true right profile view, face turned 90 degrees",
        "Back View": "back of head and upper shoulders facing camera",
        "Back 45 Degree Left": "back three-quarter view turned approximately 45 degrees left",
        "Back 45 Degree Right": "back three-quarter view turned approximately 45 degrees right",
        "Looking Up": "chin raised slightly, looking upward while keeping facial structure visible",
        "Looking Down": "chin lowered slightly, looking downward while keeping facial structure visible",
        "Looking Left": "eyes and head directed to the left",
        "Looking Right": "eyes and head directed to the right",
        "Over Left Shoulder": "looking back over the left shoulder",
        "Over Right Shoulder": "looking back over the right shoulder",
        "Standing Neutral": "standing naturally with relaxed shoulders and balanced posture",
        "Hands on Hips": "standing with both hands resting naturally on the hips",
        "Arms Crossed": "standing with arms crossed comfortably across the torso",
        "Hands Relaxed": "hands relaxed naturally at the sides",
        "Leaning Against Wall": "leaning lightly against a wall in a relaxed pose",
        "Looking Over Shoulder": "torso angled away while looking back over one shoulder",
        "Walking Forward": "walking naturally toward the camera, mid-step",
        "Seated on Chair": "seated naturally on a chair with balanced posture",
        "Seated on Couch": "seated casually on a couch in a relaxed position",
        "Holding Coffee Mug": "holding a coffee mug naturally near the torso",
        "Holding Phone": "holding a phone casually in one hand",
        "Reading a Book": "holding and reading a book naturally",
        "Working on Laptop": "seated while naturally working on a laptop",
        "Casual Laugh": "caught during a relaxed natural laugh",
        "One Hand in Pocket": "standing with one hand casually placed in a pocket",
        "Adjusting Hair": "one hand naturally adjusting the hair",
        "Standing Front": "standing front-facing in a relaxed neutral stance",
        "Standing Back": "standing with the back facing the camera",
        "Standing Left Side": "standing in a true left-side view",
        "Standing Right Side": "standing in a true right-side view",
        "Walking Toward Camera": "walking naturally toward the camera, full body visible",
        "Walking Away": "walking naturally away from the camera, full body visible",
        "Seated on Floor": "seated naturally on the floor with the full body visible",
        "Cross-Legged": "seated cross-legged with balanced natural posture",
        "Kneeling": "kneeling naturally with full body and limbs visible",
        "Hands in Pockets": "standing casually with both hands in pockets",
        "One Leg Forward": "standing with one leg placed slightly forward",
        "Arms Raised": "standing with both arms raised naturally above shoulder level",
        "Turning Around": "captured while naturally turning around",
        "Relaxed Casual Stance": "relaxed casual full-body stance with natural weight distribution",
        "Both Hands Front": "both hands held forward with palms visible and fingers naturally separated",
        "Both Hands Back": "backs of both hands visible with fingers naturally separated",
        "Left Hand": "left hand isolated and clearly visible from a natural angle",
        "Right Hand": "right hand isolated and clearly visible from a natural angle",
        "Fingers": "close documentation of the fingers, joints, nails, and natural proportions",
        "Both Feet Front": "both feet visible from the front with natural spacing",
        "Both Feet Side": "both feet visible from a clean side angle",
        "Left Foot": "left foot isolated and clearly visible",
        "Right Foot": "right foot isolated and clearly visible",
        "Eyes": "both eyes and surrounding facial anatomy clearly visible",
        "Hair": "hair shape, texture, hairline, and overall arrangement clearly visible",
        "Neck": "neck and collarbone area clearly visible",
        "Shoulders": "both shoulders clearly visible with natural posture",
        "Upper Chest / Bust": "upper chest and bust anatomy clearly visible with accurate natural proportions and unobstructed contour reference",
        "Back": "back anatomy and shoulder-blade area clearly visible",
        "Waist": "waistline and torso silhouette clearly visible",
        "Hips": "hips and pelvic anatomy clearly visible with accurate natural proportions and contour definition",
        "Buttocks": "rear hip, gluteal, and buttocks anatomy clearly visible with accurate natural proportions and crease definition",
        "Thighs": "upper legs and thigh proportions clearly visible",
        "Knees": "both knees clearly visible from a natural angle",
        "Calves": "lower legs and calf proportions clearly visible",
        "Arms": "both arms clearly visible from shoulders to hands",
        "Elbows": "elbow joints and surrounding arm anatomy clearly visible",
    }
    return direct.get(variant, variant.lower())


def _subject_prompt(gender: str, body_type: str, female_chest_size: str) -> str:
    parts = [GENDERS.get(gender, ""), BODY_TYPES.get(body_type, "")]
    if gender == "Female" and female_chest_size != "Unspecified":
        parts.append(f"proportionate {female_chest_size} bust")
    return _clean_join(parts)


def _outfit_prompt(outfit_style: str, exact_outfit: str, priority: str) -> str:
    exact = exact_outfit.strip()
    base = exact if exact else OUTFITS.get(outfit_style, "")
    if not base:
        return ""

    if exact:
        base = f"wearing {base}" if not base.lower().startswith(("wearing ", "dressed in ")) else base

    if priority == "High":
        return _clean_join([base, "the outfit must remain clearly visible and match this description"])
    if priority == "Strict":
        return _clean_join([f"wearing exactly {base.removeprefix('wearing ').strip()}", "do not substitute, hide, cover, or alter the clothing"])
    return base



def _visibility_and_outfit_prompts(
    body_visibility: str,
    outfit_style: str,
    exact_outfit: str,
    priority: str,
) -> tuple[str, str]:
    visibility_prompt = BODY_VISIBILITY_MODES.get(body_visibility, "")
    if body_visibility == "Use Selected Outfit":
        return visibility_prompt, _outfit_prompt(outfit_style, exact_outfit, priority)
    return visibility_prompt, ""


def _build_qwen_instruction(
    subject_prompt: str,
    outfit_prompt: str,
    visibility_prompt: str,
    framing_prompt: str,
    camera_view_prompt: str,
    variant_prompt: str,
    expression_prompt: str,
    background_prompt: str,
    lighting_prompt: str,
    style_prompt: str,
    custom_prefix: str,
    custom_suffix: str,
) -> str:
    instructions = [
        custom_prefix,
        f"Edit Image 1 into a realistic camera photo of the same person",
        f"Keep the same facial identity, natural likeness, and overall person consistency from Image 1",
        subject_prompt,
        framing_prompt,
        camera_view_prompt,
        variant_prompt,
        outfit_prompt,
        visibility_prompt,
        expression_prompt,
        background_prompt,
        lighting_prompt,
        style_prompt,
        "Follow the requested framing, camera view, pose, body visibility, outfit when applicable, setting, and background exactly",
        "Keep the result grounded as an ordinary real-life photo, not a stylized portrait",
        custom_suffix,
    ]
    return _sentence_join(instructions)



def _framing_prompt(shot_type: str, variant: str) -> str:
    if shot_type == "Body Anatomy / Part Focus":
        specific = ANATOMY_PART_FRAMING.get(variant, "")
        return _clean_join([
            specific,
            "single targeted body-region composition",
            "the requested anatomy is the dominant subject of the image",
            "camera aimed directly at the requested body region",
        ])
    return SHOT_BASE.get(shot_type, "")


def _context_negative_prompt(shot_type: str, variant: str) -> str:
    if shot_type == "Body Anatomy / Part Focus":
        return ANATOMY_PART_NEGATIVES.get(variant, "")
    if shot_type == "Midshot":
        return _clean_join([
            "head-and-shoulders crop",
            "shoulders-only crop",
            "chest-up crop",
            "bust-only framing",
            "collarbone crop",
            "cropped top of head",
            "cropped hair",
            "cropped abdomen",
            "cropped waist",
            "camera too close",
            "portrait zoomed in too tightly",
        ])
    return ""


_FACE_DETAIL_VARIANTS = {
    "Both Eyes Centered",
    "Left Eye",
    "Right Eye",
    "Eyebrows",
    "Forehead",
    "Nose",
    "Mouth and Lips",
    "Teeth and Smile",
    "Teeth",
    "Left Ear",
    "Right Ear",
    "Jawline",
    "Hairline",
    "Neck Front",
    "Neck Side",
    "Eyes",
    "Hair",
    "Neck",
}

_UPPER_BODY_VARIANTS = {
    "Shoulders",
    "Upper Chest / Bust",
    "Back",
    "Arms",
    "Elbows",
    "Both Hands Front",
    "Both Hands Back",
    "Left Hand",
    "Right Hand",
    "Fingers",
}

_LOWER_BODY_VARIANTS = {
    "Waist",
    "Hips",
    "Buttocks",
    "Thighs",
    "Knees",
    "Calves",
    "Both Feet Front",
    "Both Feet Side",
    "Left Foot",
    "Right Foot",
    "Toes",
}


def _profile_value(profile: dict, key: str) -> str:
    value = profile.get(key, "")
    return value.strip() if isinstance(value, str) else ""


def _location_matches_variant(location: str, shot_type: str, variant: str) -> bool:
    location_l = location.lower().strip()
    if not location_l or location_l == "unspecified":
        return False

    if shot_type == "Full Body":
        return True

    if shot_type in {"Extreme Close-Up", "Close-Up Portrait"}:
        return any(token in location_l for token in (
            "face", "neck", "ear", "eyebrow", "nostril", "septum", "lip", "cheek",
        ))

    if shot_type == "Midshot":
        return any(token in location_l for token in (
            "face", "neck", "ear", "collarbone", "chest", "shoulder",
            "upper arm", "forearm", "hand", "ribcage", "navel", "nipple",
        ))

    if shot_type != "Body Anatomy / Part Focus":
        return True

    mapping = {
        "Both Hands Front": ("hand", "finger", "forearm"),
        "Both Hands Back": ("hand", "finger", "forearm"),
        "Left Hand": ("hand", "finger", "forearm"),
        "Right Hand": ("hand", "finger", "forearm"),
        "Fingers": ("hand", "finger"),
        "Both Feet Front": ("ankle", "calf", "foot"),
        "Both Feet Side": ("ankle", "calf", "foot"),
        "Left Foot": ("ankle", "calf", "foot"),
        "Right Foot": ("ankle", "calf", "foot"),
        "Toes": ("ankle", "foot"),
        "Eyes": ("face", "eyebrow"),
        "Both Eyes Centered": ("face", "eyebrow"),
        "Left Eye": ("face", "eyebrow"),
        "Right Eye": ("face", "eyebrow"),
        "Eyebrows": ("face", "eyebrow"),
        "Forehead": ("face",),
        "Nose": ("face", "nostril", "septum"),
        "Mouth and Lips": ("face", "lip"),
        "Teeth": ("face", "lip"),
        "Teeth and Smile": ("face", "lip"),
        "Left Ear": ("ear",),
        "Right Ear": ("ear",),
        "Jawline": ("face", "neck"),
        "Hairline": ("face",),
        "Hair": ("face", "neck"),
        "Neck": ("neck", "collarbone"),
        "Neck Front": ("neck", "collarbone"),
        "Neck Side": ("neck", "collarbone"),
        "Shoulders": ("shoulder", "upper arm", "collarbone"),
        "Upper Chest / Bust": ("chest", "collarbone", "ribcage", "nipple"),
        "Back": ("upper back", "lower back", "shoulder"),
        "Waist": ("abdomen", "ribcage", "hip", "navel"),
        "Hips": ("hip", "pelvis", "abdomen", "thigh"),
        "Buttocks": ("buttock", "lower back", "hip"),
        "Thighs": ("thigh", "hip"),
        "Knees": ("thigh", "calf", "knee"),
        "Calves": ("calf", "ankle"),
        "Arms": ("shoulder", "upper arm", "forearm", "hand"),
        "Elbows": ("upper arm", "forearm", "elbow"),
    }
    return any(token in location_l for token in mapping.get(variant, ()))


def _relevant_profile_detail(profile: dict, prompt_key: str, location_key: str, shot_type: str, variant: str) -> str:
    detail = _profile_value(profile, prompt_key)
    if not detail:
        return ""
    location = _profile_value(profile, location_key)
    if shot_type == "Full Body" or _location_matches_variant(location, shot_type, variant):
        return detail
    return ""


def _build_profile_prompt(profile: dict, usage: str, shot_type: str, variant: str) -> str:
    if not isinstance(profile, dict) or usage == "Ignore Profile":
        return ""

    identity = _profile_value(profile, "identity")
    face = _profile_value(profile, "face")
    hair = _profile_value(profile, "hair")
    body = _profile_value(profile, "body")
    anatomy = _profile_value(profile, "anatomy")
    anatomy_upper = _profile_value(profile, "anatomy_upper")
    anatomy_lower = _profile_value(profile, "anatomy_lower") or anatomy
    tattoos = _relevant_profile_detail(
        profile, "tattoos", "tattoo_location", shot_type, variant
    )
    piercings = _relevant_profile_detail(
        profile, "piercings", "piercing_location", shot_type, variant
    )

    if usage == "Identity Only":
        return _profile_value(profile, "identity_lock")

    if usage == "Full Character Profile":
        return _clean_join([
            _profile_value(profile, "identity_lock"),
            _profile_value(profile, "jewelry"),
        ])

    if shot_type in {"Extreme Close-Up", "Close-Up Portrait"}:
        return _clean_join([identity, face, hair, tattoos, piercings])

    if shot_type == "Midshot":
        return _clean_join([
            identity,
            face,
            hair,
            body,
            anatomy_upper,
            tattoos,
            piercings,
        ])

    if shot_type == "Full Body":
        return _clean_join([
            identity,
            face,
            hair,
            body,
            anatomy,
            _profile_value(profile, "tattoos"),
            _profile_value(profile, "piercings"),
        ])

    if shot_type == "Body Anatomy / Part Focus":
        if variant in _FACE_DETAIL_VARIANTS:
            return _clean_join([identity, face, hair, tattoos, piercings])
        if variant in _UPPER_BODY_VARIANTS:
            return _clean_join([
                identity,
                body,
                anatomy_upper,
                tattoos,
                piercings,
            ])
        if variant in _LOWER_BODY_VARIANTS:
            return _clean_join([
                identity,
                body,
                anatomy_lower,
                tattoos,
                piercings,
            ])

    return _clean_join([identity, face, hair, body, tattoos, piercings])


def _resolve_clothing_source(
    clothing_source: str,
    profile: dict,
    planner_outfit_prompt: str,
    planner_visibility_prompt: str,
) -> tuple[str, str]:
    profile_clothing = _profile_value(profile, "clothing") if isinstance(profile, dict) else ""

    if clothing_source == "Character Creator Clothing":
        return profile_clothing, ""

    if clothing_source == "Merge Both":
        return _clean_join([profile_clothing, planner_outfit_prompt]), planner_visibility_prompt

    if clothing_source == "No Clothing / Visibility Mode":
        visibility = planner_visibility_prompt or (
            "adult subject with no clothing for neutral non-erotic character documentation"
        )
        return "", visibility

    return planner_outfit_prompt, planner_visibility_prompt



def _resolve_camera_view(
    camera_view: str,
    profile: dict,
    shot_type: str,
) -> tuple[str, str]:
    if shot_type == "Body Anatomy / Part Focus":
        return "Anatomy Framing", ""

    effective_view = camera_view
    if camera_view == "Use Character Profile View":
        effective_view = _profile_value(profile, "source_camera_view") or "Front View"
    elif camera_view == "Use Shot Variant Only":
        return "Shot Variant Only", ""

    return effective_view, CAMERA_VIEW_PROMPTS.get(effective_view, "")


def _pose_prompt_with_camera_view(variant: str, camera_view_prompt: str) -> str:
    if camera_view_prompt and variant in _DIRECTION_NEUTRAL_VARIANTS:
        return _DIRECTION_NEUTRAL_VARIANTS[variant]
    return _variant_to_prompt(variant)


class DatasetShotPlanner:
    """Dataset Shot Planner v1.7.0."""
    CATEGORY = "prompt/dataset"
    FUNCTION = "build_prompt"
    DESCRIPTION = "Dataset Shot Planner v1.7.0 — strengthens true waist-up midshot framing and retains independent camera-view control."

    RETURN_TYPES = (
        "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",
        "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING",
        "STRING", "STRING", "STRING",
    )
    RETURN_NAMES = (
        "combined_prompt",
        "subject_prompt",
        "outfit_prompt",
        "visibility_prompt",
        "pose_variant_prompt",
        "framing_prompt",
        "expression_prompt",
        "background_prompt",
        "lighting_prompt",
        "style_prompt",
        "negative_prompt",
        "shot_variant",
        "shot_id",
        "profile_prompt",
        "profile_character_id",
        "camera_view_prompt",
        "effective_camera_view",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_order": (PROMPT_ORDERS, {"default": "Krea2 Optimized"}),
                "shot_type": (SHOT_TYPES, {"default": "Close-Up Portrait"}),
                "shot_variant": (ALL_VARIANTS, {"default": "Front Neutral"}),
                "photography_style": (PHOTO_STYLE_NAMES, {"default": "Personal Cellphone Photo"}),
                "gender": (GENDER_NAMES, {"default": "Unspecified"}),
                "body_type": (BODY_TYPE_NAMES, {"default": "Unspecified"}),
                "female_chest_size": (FEMALE_CHEST_SIZES, {"default": "Unspecified"}),
                "outfit_style": (OUTFIT_NAMES, {"default": "Varied Fitted Outfits"}),
                "outfit_priority": (OUTFIT_PRIORITIES, {"default": "High"}),
                "expression": (EXPRESSION_NAMES, {"default": "Neutral"}),
                "lighting": (LIGHTING_NAMES, {"default": "Use Style Default"}),
                "background": (BACKGROUND_NAMES, {"default": "Unspecified"}),
                "negative_preset": (NEGATIVE_NAMES, {"default": "Standard Dataset"}),
                "randomize_variant": ("BOOLEAN", {"default": False}),
                "random_seed": ("INT", {"default": 1985, "min": 0, "max": 9223372036854775807, "step": 1}),
                "body_visibility": (BODY_VISIBILITY_NAMES, {"default": "Use Selected Outfit"}),
                "profile_usage": (PROFILE_USAGE_MODES, {"default": "Shot-Aware Identity"}),
                "clothing_source": (CLOTHING_SOURCES, {"default": "Dataset Planner Clothing"}),
                "camera_view": (CAMERA_VIEW_OPTIONS, {"default": "Use Shot Variant Only"}),
            },
            "optional": {
                "exact_outfit": ("STRING", {"default": "", "multiline": True, "placeholder": "Example: fitted black ribbed crop top and high-waisted charcoal leggings"}),
                "custom_prefix": ("STRING", {"default": "", "multiline": True}),
                "custom_suffix": ("STRING", {"default": "", "multiline": True}),
                "custom_negative": ("STRING", {"default": "", "multiline": True}),
                "character_profile": ("CHARACTER_PROFILE", {"forceInput": True}),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(cls, shot_type, shot_variant, **kwargs):
        if shot_type not in SHOT_VARIANTS:
            return f"Unknown shot_type: {shot_type}"
        if shot_variant not in ALL_VARIANTS:
            return f"Unknown shot_variant: {shot_variant}"
        return True

    def build_prompt(
        self,
        prompt_order,
        shot_type,
        shot_variant,
        photography_style,
        gender,
        body_type,
        female_chest_size,
        outfit_style,
        outfit_priority,
        expression,
        lighting,
        background,
        negative_preset,
        randomize_variant,
        random_seed,
        body_visibility,
        profile_usage,
        clothing_source,
        camera_view,
        exact_outfit="",
        custom_prefix="",
        custom_suffix="",
        custom_negative="",
        character_profile=None,
    ):
        valid_variants = SHOT_VARIANTS.get(shot_type, SHOT_VARIANTS["Close-Up Portrait"])
        if randomize_variant:
            chosen_variant = _stable_choice(valid_variants, int(random_seed), shot_type)
        elif shot_variant in valid_variants:
            chosen_variant = shot_variant
        else:
            chosen_variant = valid_variants[0]

        subject_prompt = _subject_prompt(gender, body_type, female_chest_size)
        profile = character_profile if isinstance(character_profile, dict) else {}
        profile_prompt = _build_profile_prompt(
            profile,
            profile_usage,
            shot_type,
            chosen_variant,
        )
        effective_subject_prompt = profile_prompt or subject_prompt

        planner_visibility_prompt, planner_outfit_prompt = _visibility_and_outfit_prompts(
            body_visibility, outfit_style, exact_outfit, outfit_priority
        )
        outfit_prompt, visibility_prompt = _resolve_clothing_source(
            clothing_source,
            profile,
            planner_outfit_prompt,
            planner_visibility_prompt,
        )
        effective_camera_view, camera_view_prompt = _resolve_camera_view(
            camera_view,
            profile,
            shot_type,
        )
        pose_variant_prompt = _pose_prompt_with_camera_view(
            chosen_variant,
            camera_view_prompt,
        )
        framing_prompt = _framing_prompt(shot_type, chosen_variant)
        expression_prompt = EXPRESSIONS.get(expression, "")
        background_prompt = BACKGROUNDS.get(background, "")
        lighting_prompt = LIGHTING.get(lighting, "")
        style_prompt = (
            KREA2_STYLES.get(photography_style, "")
            if prompt_order == "Krea2 Optimized"
            else PHOTO_STYLES.get(photography_style, "")
        )

        if prompt_order == "Krea2 Optimized":
            if shot_type == "Body Anatomy / Part Focus":
                combined_prompt = _clean_join([
                    custom_prefix,
                    pose_variant_prompt,
                    framing_prompt,
                    effective_subject_prompt,
                    outfit_prompt,
                    visibility_prompt,
                    background_prompt,
                    lighting_prompt,
                    style_prompt,
                    expression_prompt,
                    custom_suffix,
                ])
            else:
                combined_prompt = _clean_join([
                    custom_prefix,
                    framing_prompt,
                    camera_view_prompt,
                    pose_variant_prompt,
                    effective_subject_prompt,
                    outfit_prompt,
                    visibility_prompt,
                    expression_prompt,
                    background_prompt,
                    lighting_prompt,
                    style_prompt,
                    custom_suffix,
                ])
        elif prompt_order == "Qwen Image Edit":
            combined_prompt = _build_qwen_instruction(
                effective_subject_prompt,
                outfit_prompt,
                visibility_prompt,
                framing_prompt,
                camera_view_prompt,
                pose_variant_prompt,
                expression_prompt,
                background_prompt,
                lighting_prompt,
                style_prompt,
                custom_prefix,
                custom_suffix,
            )
        elif prompt_order == "Traditional Photography":
            combined_prompt = _clean_join([
                custom_prefix,
                framing_prompt,
                camera_view_prompt,
                pose_variant_prompt,
                effective_subject_prompt,
                lighting_prompt,
                background_prompt,
                outfit_prompt,
                visibility_prompt,
                style_prompt,
                custom_suffix,
            ])
        else:
            combined_prompt = _clean_join([
                custom_prefix,
                effective_subject_prompt,
                framing_prompt,
                camera_view_prompt,
                pose_variant_prompt,
                expression_prompt,
                lighting_prompt,
                background_prompt,
                style_prompt,
                outfit_prompt,
                visibility_prompt,
                custom_suffix,
            ])

        negative_prompt = _clean_join([
            NEGATIVE_PRESETS.get(negative_preset, ""),
            _context_negative_prompt(shot_type, chosen_variant),
            custom_negative,
        ])

        profile_character_id = (
            _profile_value(profile, "character_id")
            if profile_usage != "Ignore Profile"
            else ""
        )

        shot_id_parts = [
            profile_character_id,
            _slug(shot_type),
            _slug(effective_camera_view),
            _slug(chosen_variant),
            _slug(photography_style),
        ]
        shot_id = "_".join(part for part in shot_id_parts if part)

        return (
            combined_prompt,
            subject_prompt,
            outfit_prompt,
            visibility_prompt,
            pose_variant_prompt,
            framing_prompt,
            expression_prompt,
            background_prompt,
            lighting_prompt,
            style_prompt,
            negative_prompt,
            chosen_variant,
            shot_id,
            profile_prompt,
            profile_character_id,
            camera_view_prompt,
            effective_camera_view,
        )
