from dataset_shot_planner.src.nodes import DatasetShotPlanner


PROFILE = {
    "schema": "CHARACTER_PROFILE",
    "schema_version": 2,
    "character_id": "adult_female_25_34_oval_brown_average",
    "identity": "adult subject, adult female, age range 25–34",
    "face": "oval face shape, hazel eyes",
    "hair": "medium brown shoulder-length hair",
    "body": "average height, average body type",
    "anatomy": (
        "proportionate 34 C cup bust, teardrop-shaped breasts with a gentle upper slope "
        "and natural lower fullness, high-set perky breast position"
    ),
    "anatomy_upper": (
        "proportionate 34 C cup bust, teardrop-shaped breasts with a gentle upper slope "
        "and natural lower fullness, high-set perky breast position"
    ),
    "anatomy_lower": "average buttocks",
    "tattoos": "",
    "piercings": "",
    "identity_lock": "adult female identity lock",
    "source_camera_view": "Three-Quarter Left",
}


def build(shot_type="Midshot", shot_variant="Standing Neutral", prompt_order="Qwen Image Edit"):
    return DatasetShotPlanner().build_prompt(
        prompt_order=prompt_order,
        shot_type=shot_type,
        shot_variant=shot_variant,
        photography_style="Personal Cellphone Photo",
        gender="Unspecified",
        body_type="Unspecified",
        female_chest_size="Unspecified",
        outfit_style="Fitted Casual",
        outfit_priority="High",
        expression="Neutral",
        lighting="Natural Daylight",
        background="Plain Neutral",
        negative_preset="Standard Dataset",
        randomize_variant=False,
        random_seed=1985,
        body_visibility="Use Selected Outfit",
        profile_usage="Shot-Aware Identity",
        clothing_source="Dataset Planner Clothing",
        camera_view="Use Character Profile View",
        character_profile=PROFILE,
    )


def test_midshot_is_true_waist_up_crop():
    result = build()
    framing = result[5].lower()
    prompt = result[0].lower()
    negative = result[10].lower()

    assert "slightly above the top of the head" in framing
    assert "navel or lower mid-abdomen" in framing
    assert "complete hair and full head visible" in framing
    assert "natural waist and mid-abdomen" in framing
    assert "do not crop at the shoulders" in framing

    assert "three-quarter-left camera view" in prompt
    assert "teardrop-shaped breasts" in prompt

    assert "head-and-shoulders crop" in negative
    assert "chest-up crop" in negative
    assert "cropped abdomen" in negative
    assert "camera too close" in negative


def test_full_body_behavior_remains_available():
    result = build("Full Body", "Standing Front", "Krea2 Optimized")
    assert "entire subject visible from head to feet" in result[5]
    assert "cropped abdomen" not in result[10]


def test_camera_view_still_inherits_profile():
    result = build()
    assert result[16] == "Three-Quarter Left"
    assert "three-quarter-left camera view" in result[15]
