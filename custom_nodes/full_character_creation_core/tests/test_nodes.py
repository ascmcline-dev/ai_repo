from full_character_creation_core.src.nodes import CharacterBlueprintCreator, CharacterShotPlanner


def make_profile(default_clothing="Clinical Unclothed Documentation", lower_body_notes="Full female pubic hair"):
    creator = CharacterBlueprintCreator()
    result = creator.build_blueprint(
        gender="Adult Female", age_range="25–34", heritage="Indigenous / Native American",
        skin_tone="Deep Tan", complexion="Natural Skin Texture", face_shape="Oval",
        jaw_shape="Defined", chin_shape="Rounded", eye_color="Gray", eye_shape="Almond",
        eyebrow_shape="Soft Arch", nose_shape="Straight", lip_shape="Balanced Medium",
        hair_color="Medium Brown", hair_length="Mid-Back", hair_texture="Slightly Wavy",
        hair_style="Loose Natural", height="Average", body_type="Average", bust_size="Medium-Full",
        bust_shape="Teardrop", bust_position="Natural Average-Set", bust_firmness="Balanced Natural",
        bust_augmentation="Natural / Unaugmented", buttocks="Average",
        default_clothing=default_clothing, jewelry_level="None", tattoo_status="None",
        piercing_status="One", piercing_descriptors="Left Eyebrow black curved barbell",
        lower_body_notes=lower_body_notes,
    )
    return result


def plan(profile, **overrides):
    values = dict(
        stage="Krea Identity Anchor", shot_type="Full Body", camera_view="Left Profile",
        pose="Arms Loosely Crossed", expression="Neutral", clothing_mode="Exact Outfit Override",
        body_region="Custom", background="Natural Home", lighting="Even Window Light",
        photo_style="Authentic Consumer Camera", character_blueprint=profile,
        exact_outfit="ultra micro bikini", body_detail_mode="Clothed Silhouette",
        outfit_coverage="Swimwear Set", clothing_priority="Maximum",
    )
    values.update(overrides)
    return CharacterShotPlanner().plan_shot(**values)


def test_blueprint_separates_clothed_and_anatomy_body():
    result = make_profile()
    blueprint = result[8]
    assert blueprint["schema_version"] == 2
    assert "pubic hair" in blueprint["anatomy_lower_body"].lower()
    assert "pubic hair" not in blueprint["clothed_lower_body"].lower()
    assert "natural unaugmented chest structure" in blueprint["anatomy_upper_body"].lower()
    assert "natural unaugmented chest structure" not in blueprint["clothed_upper_body"].lower()


def test_profile_tshirt_is_complete_outfit():
    result = make_profile(default_clothing="Simple Fitted T-Shirt", lower_body_notes="")
    prompt = result[14].lower()
    assert "fitted t-shirt" in prompt
    assert "jeans" in prompt
    assert "shoes" in prompt


def test_exact_swimwear_full_body_is_early_and_complete():
    profile = make_profile()[8]
    result = plan(profile)
    prompt = result[0].lower()
    assert "ultra micro bikini" in prompt
    assert "swimwear top" in prompt
    assert "swimwear bottoms" in prompt
    assert "pubic hair" not in prompt
    assert prompt.index("ultra micro bikini") < prompt.index("adult subject")
    assert "dominant wardrobe state" in prompt
    assert result[11] == "Clothed Silhouette"


def test_exact_swimwear_chest_up_requires_complete_top():
    profile = make_profile()[8]
    result = plan(profile, shot_type="Chest-Up")
    prompt = result[0].lower()
    assert "complete swimwear top" in prompt
    assert "both sides, straps, neckline" in prompt
    assert "pubic hair" not in prompt


def test_exact_swimwear_headshot_keeps_visible_straps():
    profile = make_profile()[8]
    result = plan(profile, shot_type="Head and Shoulders")
    prompt = result[0].lower()
    assert "swimwear top neckline and both straps" in prompt


def test_exact_clothing_override_ignores_clinical_profile():
    profile = make_profile()[8]
    result = plan(
        profile,
        shot_type="Waist-Up Midshot",
        exact_outfit="",
        exact_top="opaque fitted black tank top",
        exact_bottom="high-waisted black leggings",
        outfit_coverage="Complete Outfit",
    )
    prompt = result[0].lower()
    assert "opaque fitted black tank top" in prompt
    assert "high-waisted black leggings" in prompt
    assert "unclothed" not in prompt
    assert "pubic hair" not in prompt
    assert "natural unaugmented chest structure" not in prompt


def test_clinical_anatomy_retains_anatomy_notes():
    profile = make_profile()[8]
    result = plan(
        profile,
        stage="Qwen Anatomy Documentation",
        shot_type="Full Body",
        clothing_mode="Clinical Unclothed",
        body_detail_mode="Clinical Anatomy",
        exact_outfit="",
    )
    prompt = result[1].lower()
    assert "pubic hair" in prompt
    assert "natural unaugmented chest structure" in prompt
    assert result[11] == "Clinical Anatomy"


def test_krea_lora_expansion_does_not_duplicate_profile_clothing():
    profile = make_profile(default_clothing="Simple Fitted T-Shirt", lower_body_notes="")[8]
    result = plan(
        profile,
        stage="Krea Mini-LoRA Expansion",
        clothing_mode="Profile Default",
        exact_outfit="",
        outfit_coverage="Auto by Shot",
    )
    prompt = result[0].lower()
    assert prompt.count("fitted t-shirt") <= 2
    assert "pubic hair" not in prompt


def test_heritage_and_bust_descriptor_are_preserved():
    result = make_profile()
    assert "indigenous / native american heritage" in result[0].lower()
    assert "medium-full bust" in result[3].lower()
    assert "cup" not in result[3].lower()
