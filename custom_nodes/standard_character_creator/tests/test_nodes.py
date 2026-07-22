from standard_character_creator.src.nodes import StandardCharacterCreator
from standard_character_creator.src.prompt_data import (
    BREAST_SHAPES,
    BREAST_POSITIONS,
    BREAST_FIRMNESS,
    BREAST_AUGMENTATION,
)


BASE = dict(
    shot_type="Waist-Up Midshot",
    camera_view="Front View",
    gender="Adult Female",
    age_range="25–34",
    skin_tone="Light",
    complexion="Natural Skin Texture",
    face_shape="Oval",
    jaw_shape="Defined",
    chin_shape="Rounded",
    eye_color="Hazel",
    eye_shape="Almond",
    eyebrow_shape="Soft Arch",
    nose_shape="Straight",
    lip_shape="Balanced Medium",
    hair_color="Medium Brown",
    hair_length="Shoulder-Length",
    hair_texture="Slightly Wavy",
    hair_style="Loose Natural",
    highlight_style="None",
    highlight_color="Golden Blonde",
    height="Average",
    body_type="Average",
    bra_band="34",
    cup_size="C",
    male_groin_size="Average",
    female_groin_description="Unspecified",
    buttocks="Average",
    clothing_category="Daily Outdoor",
    clothing_style="Casual Jeans and Tee",
    jewelry_level="Minimal",
    jewelry_item="Stud Earrings",
    jewelry_material="Silver",
    tattoo_status="None",
    tattoo_location="Upper Arm",
    piercing_status="None",
    piercing_location="Ear / Ears",
    piercing_type="Stud",
    negative_preset="Standard Character",
)


def build(**overrides):
    values = BASE.copy()
    values.update(overrides)
    return StandardCharacterCreator().build_character(**values)


def test_new_chest_option_lists():
    assert "Teardrop" in BREAST_SHAPES
    assert "High and Tight" in BREAST_POSITIONS
    assert "Very Soft / Natural Movement" in BREAST_FIRMNESS
    assert "Very Firm Augmented Projection" in BREAST_AUGMENTATION


def test_midshot_profile_contains_chest_conformation():
    result = build(
        breast_shape="Teardrop",
        breast_position="High-Set / Perky",
        breast_firmness="Naturally Firm",
        breast_augmentation="Natural / Unaugmented",
    )
    profile = result[15]
    chest_prompt = result[16]

    assert len(result) == 18
    assert "34 C cup" in chest_prompt
    assert "teardrop-shaped" in chest_prompt
    assert "high-set perky" in chest_prompt
    assert "naturally firm" in chest_prompt
    assert "unaugmented" in chest_prompt
    assert profile["schema_version"] == 2
    assert profile["breast_shape"] == "Teardrop"
    assert chest_prompt == profile["chest_prompt"]
    assert chest_prompt in profile["anatomy_upper"]


def test_face_only_prompt_hides_chest_details():
    result = build(
        shot_type="Close-Up Face Portrait",
        breast_shape="Round",
        breast_position="High and Tight",
        breast_firmness="Firm",
        breast_augmentation="Round High-Profile Implants",
    )
    assert result[7] == ""
    assert "round high-profile" not in result[0]


def test_conflicting_settings_return_warning():
    result = build(
        breast_position="High and Tight",
        breast_firmness="Very Soft / Natural Movement",
        breast_augmentation="Natural / Unaugmented",
    )
    assert "conflicts" in result[17].lower()


def test_nonfemale_profile_omits_chest_prompt():
    result = build(
        gender="Adult Male",
        breast_shape="Round",
        breast_position="High and Tight",
        breast_firmness="Firm",
        breast_augmentation="Round High-Profile Implants",
    )
    assert result[16] == ""
    assert result[17] == ""
