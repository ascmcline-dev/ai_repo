"""Prompt presets for Dataset Shot Planner v1.7.0."""

from __future__ import annotations

import json
from pathlib import Path

_VARIANTS_FILE = Path(__file__).resolve().parents[1] / "web" / "shot_variants.json"

with _VARIANTS_FILE.open("r", encoding="utf-8") as handle:
    SHOT_VARIANTS = json.load(handle)

if not isinstance(SHOT_VARIANTS, dict) or not SHOT_VARIANTS:
    raise ValueError("shot_variants.json must contain a non-empty object of shot-type lists")

for shot_type, variants in SHOT_VARIANTS.items():
    if not isinstance(shot_type, str) or not isinstance(variants, list):
        raise ValueError("Every shot type must map to a list of variant names")
    if not variants or not all(isinstance(item, str) and item.strip() for item in variants):
        raise ValueError(f"Shot type {shot_type!r} contains an invalid or empty variant list")

ALL_VARIANTS = list(
    dict.fromkeys(
        variant
        for variants in SHOT_VARIANTS.values()
        for variant in variants
    )
)

SHOT_BASE = {'Extreme Close-Up': 'extreme close-up detail photograph, tightly framed on the selected feature, precise anatomy '
                     'documentation, fine natural texture, controlled focus',
 'Close-Up Portrait': 'close-up portrait, full head visible with slight headroom, identity-preserving facial '
                      'documentation, realistic facial proportions',
 'Midshot': 'true waist-up midshot, camera zoomed out and framed from slightly above the top of the head to '
            'approximately the navel or lower mid-abdomen, small visible headroom, complete hair and full head visible, '
            'neck, both shoulders, chest, both upper arms, torso, natural waist and mid-abdomen all inside frame, '
            'clear upper-body pose, do not crop at the shoulders, collarbone, bust, ribs, or upper waist',
 'Full Body': 'full-body photograph, entire subject visible from head to feet, natural proportions, clear body pose, '
              'sufficient headroom and floor space',
 'Body Anatomy / Part Focus': 'anatomy and body-part documentation photograph, selected area clearly visible, accurate '
                              'proportions, natural texture, clean unobstructed framing'}

PHOTO_STYLES = {'Professional Photography Session': 'professional photography session, high-quality camera, controlled lighting, '
                                     'balanced exposure, clean composition, realistic depth of field, detailed natural '
                                     'texture',
 'Personal Cellphone Photo': 'casual personal cellphone photograph, natural everyday lighting, mild phone-camera '
                             'compression, slight lens softness, imperfect believable framing, candid unretouched '
                             'appearance',
 'Standard Consumer Camera': 'standard consumer-camera photograph, natural colors, moderate sharpness, realistic '
                             'exposure, casual composition, subtle lens softness',
 'DSLR Portrait': 'realistic DSLR portrait photography, optical depth of field, natural lens rendering, detailed '
                  'texture, controlled exposure',
 'Studio Photography': 'studio photography, controlled softbox lighting, neutral seamless background, clean exposure, '
                       'professional composition',
 'Natural Window-Light Portrait': 'natural window-light portrait, soft directional daylight, realistic shadows, gentle '
                                  'highlight rolloff, unretouched texture',
 'Lifestyle Photography': 'realistic lifestyle photography, natural environment, believable candid posture, available '
                          'light, relaxed composition',
 'Social Media Realism': 'authentic everyday social-media photograph, realistic smartphone or consumer-camera quality, '
                         'natural pores and skin variation, mild compression, slight lens softness, casual unretouched '
                         'appearance',
 'Candid Snapshot': 'unposed candid snapshot, spontaneous timing, natural available light, slightly imperfect framing, '
                    'realistic everyday camera rendering',
 'Polaroid / Instant Film': 'instant-film photograph, gentle softness, subtle grain, muted natural colors, mild '
                            'exposure variation, authentic printed-photo character',
 'Black and White Portrait': 'black-and-white portrait photography, natural grayscale tonal range, realistic texture, '
                             'controlled contrast, detailed highlights and shadows',
 'Black and White Documentary': 'black-and-white documentary photograph, available light, honest texture, restrained '
                                'contrast, candid realistic composition',
 'Editorial Fashion': 'editorial fashion photography, intentional composition, polished lighting, modern styling, '
                      'detailed fabric texture, realistic camera rendering',
 'Identity Documentation': 'identity documentation photograph, neutral accurate lighting, minimal stylization, precise '
                           'facial and anatomical detail, consistent camera perspective',
 'Clinical Anatomy Documentation': 'clinical anatomy documentation photograph, even neutral lighting, accurate '
                                   'proportions, clear unobstructed view, minimal artistic stylization'}

KREA2_STYLES = {'Professional Photography Session': 'professional real-life photograph, controlled natural-looking light, realistic '
                                     'camera depth, natural unretouched texture',
 'Personal Cellphone Photo': 'ordinary unretouched cellphone photo, slight lens softness, mild phone compression, '
                             'believable imperfect framing',
 'Standard Consumer Camera': 'ordinary consumer-camera photo, natural color, moderate sharpness, subtle lens softness',
 'DSLR Portrait': 'realistic DSLR portrait, natural optical depth of field, controlled exposure, unretouched texture',
 'Studio Photography': 'realistic studio photo, soft controlled light, clean exposure, natural texture',
 'Natural Window-Light Portrait': 'natural window-light photo, soft directional daylight, realistic shadows, '
                                  'unretouched texture',
 'Lifestyle Photography': 'ordinary lifestyle photo, natural environment, available light, relaxed realistic '
                          'composition',
 'Social Media Realism': 'ordinary unretouched social-media photo, natural skin texture, slight lens softness, mild '
                         'compression',
 'Candid Snapshot': 'unposed candid snapshot, available light, slightly imperfect framing, realistic everyday camera '
                    'rendering',
 'Polaroid / Instant Film': 'realistic instant-film photo, gentle softness, subtle grain, muted natural color, mild '
                            'exposure variation',
 'Black and White Portrait': 'natural black-and-white portrait, realistic grayscale tones, controlled contrast, '
                             'unretouched texture',
 'Black and White Documentary': 'black-and-white documentary snapshot, available light, honest texture, restrained '
                                'contrast',
 'Editorial Fashion': 'realistic editorial fashion photo, intentional composition, polished but natural lighting, '
                      'detailed fabric texture',
 'Identity Documentation': 'identity documentation photo, neutral accurate light, minimal stylization, precise facial '
                           'detail',
 'Clinical Anatomy Documentation': 'clinical anatomy documentation photo, even neutral light, accurate proportions, '
                                   'unobstructed view'}

EXPRESSIONS = {'Neutral': 'neutral relaxed expression',
 'Natural Smile': 'natural relaxed smile',
 'Broad Smile': 'broad genuine smile',
 'Serious': 'calm serious expression',
 'Confident': 'confident composed expression',
 'Soft / Approachable': 'soft approachable expression',
 'Laughing': 'natural candid laugh',
 'Focused': 'focused attentive expression',
 'No Expression Instruction': ''}

LIGHTING = {'Use Style Default': '',
 'Natural Daylight': 'natural daylight',
 'Soft Window Light': 'soft directional window light',
 'Overcast Daylight': 'soft overcast daylight with low contrast',
 'Warm Indoor Light': 'warm realistic indoor lighting',
 'Bright Indoor Light': 'bright neutral indoor lighting',
 'Soft Studio Light': 'soft controlled studio lighting',
 'High-Key Studio': 'high-key studio lighting with soft shadows',
 'Low-Key Dramatic': 'low-key dramatic lighting with controlled shadows',
 'Golden Hour': 'warm golden-hour sunlight',
 'Direct Flash': 'realistic direct on-camera flash'}

BACKGROUNDS = {'Unspecified': '',
 'Plain Neutral': 'plain neutral uncluttered background',
 'Studio Seamless': 'clean studio seamless backdrop',
 'Home Interior': 'ordinary realistic home interior',
 'Living Room': 'casual lived-in living room',
 'Bedroom': 'ordinary tidy bedroom',
 'Gym': 'realistic working gym environment',
 'Outdoor Urban': 'realistic outdoor urban environment',
 'Outdoor Natural': 'natural outdoor setting',
 'Office': 'realistic office environment',
 'Clinical Neutral': 'plain clinical documentation background'}

OUTFITS = {'Unspecified': '',
 'Varied Fitted Outfits': 'varied fitted outfits, tailored fit, form-following silhouette, clean lines, minimal '
                          'layering, no oversized garments, no bulky outerwear',
 'Fitted Casual': 'fitted casual clothing, streamlined silhouette, natural fabric tension, minimal layering',
 'Fitted Athletic': 'fitted athletic outfit, functional stretch fabric, streamlined silhouette, realistic fabric '
                    'texture',
 'Tailored Fashion': 'tailored modern outfit, precise fit, clean silhouette, realistic fabric structure',
 'Minimal Form-Fitting Outfit': 'minimal form-fitting outfit, simple clean silhouette, no bulky layers',
 'Fitted Top and Jeans': 'fitted top with well-fitted jeans, clean everyday silhouette',
 'Fitted Dress': 'well-fitted dress with a clean tailored silhouette',
 'Swimwear': 'properly fitted swimwear, clean anatomical silhouette',
 'Anatomy Documentation Clothing': 'simple fitted neutral clothing that keeps the selected anatomy clearly visible '
                                   'without bulky fabric'}

NEGATIVE_PRESETS = {'None': '',
 'Standard Dataset': 'cropped head, cropped feet, missing body parts, extra fingers, fused fingers, malformed hands, '
                     'distorted anatomy, duplicate limbs, text, watermark, logo, heavy beauty filter, plastic skin',
 'No Bulky Clothing': 'oversized clothing, baggy clothes, bulky jacket, puffy coat, heavy layering, loose hoodie, wide '
                      'pants, shapeless silhouette',
 'Maximum Anatomy Guard': 'extra limbs, missing limbs, malformed hands, fused fingers, extra fingers, deformed feet, '
                          'distorted joints, twisted anatomy, duplicated body parts, cropped anatomy, text, watermark'}

GENDERS = {'Unspecified': '',
 'Female': 'female subject',
 'Male': 'male subject',
 'Nonbinary / Androgynous': 'nonbinary androgynous subject'}

BODY_TYPES = {'Unspecified': '',
 'Petite': 'petite body type',
 'Slim': 'slim body type',
 'Lean / Athletic': 'lean athletic body type',
 'Athletic': 'athletic body type',
 'Average': 'average body type',
 'Curvy': 'curvy body type',
 'Hourglass': 'hourglass body shape',
 'Pear-Shaped': 'pear-shaped body type',
 'Broad / Muscular': 'broad muscular body type',
 'Plus Size': 'plus-size body type',
 'Tall': 'tall body type'}

FEMALE_CHEST_SIZES = ['Unspecified',
 '30 A Cup',
 '30 B Cup',
 '30 C Cup',
 '30 D Cup',
 '32 A Cup',
 '32 B Cup',
 '32 C Cup',
 '32 D Cup',
 '32 DD Cup',
 '34 A Cup',
 '34 B Cup',
 '34 C Cup',
 '34 D Cup',
 '34 DD Cup',
 '36 A Cup',
 '36 B Cup',
 '36 C Cup',
 '36 D Cup',
 '36 DD Cup',
 '38 B Cup',
 '38 C Cup',
 '38 D Cup',
 '38 DD Cup']

PROMPT_ORDERS = ['Krea2 Optimized', 'Qwen Image Edit', 'Traditional Photography', 'Legacy v1.1']

OUTFIT_PRIORITIES = ['Normal', 'High', 'Strict']

BODY_VISIBILITY_MODES = {'Use Selected Outfit': '',
 'Standard Form-Fitted Clothing': 'wearing fitted opaque non-bulky reference clothing that clearly shows the overall '
                                  'body silhouette and major proportions while smoothing intimate surface detail',
 'Anatomy Documentation — Ultra Form-Fitted': 'wearing a thin opaque neutral anatomical reference garment, '
                                              'ultra-form-fitted with no padding, shaping, or compression, closely '
                                              'following all external body contours including breast shape, nipple and '
                                              'areola-region contour, abdominal contours, groin contours and creases, '
                                              'gluteal cleft, buttock crease, and natural body folds, with nipples and '
                                              'genitals fully covered, neutral non-erotic anatomy documentation',
 'Medical Grade — Unclothed': 'adult subject with no clothing, neutral non-erotic medical documentation, unobstructed '
                              'external anatomy, natural skin folds and body creases visible, no jewelry, no '
                              'concealment pose, plain clinical presentation'}

ANATOMY_PART_FRAMING = {'Both Hands Front': 'camera centered on both hands, palms facing camera, both hands fill most of the frame, wrists '
                     'included, face and torso outside frame',
 'Both Hands Back': 'camera centered on the backs of both hands, both hands fill most of the frame, wrists included, '
                    'face and torso outside frame',
 'Left Hand': 'camera tightly framed on the left hand from wrist to fingertips, hand fills most of the image, face and '
              'torso outside frame',
 'Right Hand': 'camera tightly framed on the right hand from wrist to fingertips, hand fills most of the image, face '
               'and torso outside frame',
 'Fingers': 'macro-style crop from knuckles to fingertips, fingers fill most of the image, all digits fully visible '
            'and separated',
 'Both Feet Front': 'camera centered on both feet from ankles to toes, feet fill most of the frame, lower legs only, '
                    'upper body outside frame',
 'Both Feet Side': 'clean side-view crop of both feet from ankles to toes, feet fill most of the frame, upper body '
                   'outside frame',
 'Left Foot': 'camera tightly framed on the left foot from ankle to toes, foot fills most of the image, upper body '
              'outside frame',
 'Right Foot': 'camera tightly framed on the right foot from ankle to toes, foot fills most of the image, upper body '
               'outside frame',
 'Eyes': 'tight facial crop centered on both eyes from eyebrows to upper cheeks, eyes fill most of the image',
 'Mouth and Lips': 'tight facial crop centered on the mouth from below the nose to the chin, lips fill most of the '
                   'image',
 'Teeth': 'tight facial crop centered on the mouth and teeth, from below the nose to the chin',
 'Hair': 'head-and-hair documentation crop with the complete hairstyle and hairline visible, shoulders minimal',
 'Neck': 'camera cropped from the lower jaw to the upper chest, neck centered, most of the face outside frame',
 'Shoulders': 'camera cropped from the base of the neck to the upper arms and upper chest, both shoulders centered, '
              'face outside frame',
 'Upper Chest / Bust': 'front-facing camera crop from the base of the neck to the upper abdomen, upper chest and bust '
                       'centered and occupying most of the image, head and face completely outside frame',
 'Back': 'rear-view camera crop from the base of the neck to the hips, back centered and occupying most of the image, '
         'head and legs outside frame',
 'Waist': 'front-facing camera crop from the lower ribs to the upper hips, waist centered and occupying most of the '
          'image, chest, head, and legs outside frame',
 'Hips': 'front-facing camera crop from the lower abdomen to the upper thighs, hips and pelvis centered and occupying '
         'most of the image, head, face, chest, and lower legs completely outside frame',
 'Buttocks': 'rear-facing camera crop from the lower back to the mid-thighs, buttocks and gluteal region centered and '
             'occupying most of the image, head, face, upper torso, and lower legs completely outside frame',
 'Thighs': 'camera crop from the hips to just below the knees, both thighs centered and occupying most of the image, '
           'head and upper torso outside frame',
 'Knees': 'camera crop from the lower thighs to the upper calves, both knees centered and occupying most of the image, '
          'upper body outside frame',
 'Calves': 'camera crop from just below the knees to the ankles, both calves centered and occupying most of the image, '
           'upper body outside frame',
 'Arms': 'camera composed to show both complete arms from shoulders to fingertips, arms clearly separated from the '
         'torso, face outside frame when possible',
 'Elbows': 'tight crop from the mid-upper arms to the mid-forearms, both elbows centered and occupying most of the '
           'image'}

ANATOMY_PART_NEGATIVES = {'Upper Chest / Bust': 'face close-up, headshot, full face, shoulders-up portrait',
 'Back': 'face close-up, headshot, front-facing portrait',
 'Waist': 'face close-up, headshot, chest-up portrait',
 'Hips': 'face close-up, headshot, portrait framing, chest-up crop, shoulders-up crop',
 'Buttocks': 'face close-up, headshot, portrait framing, front-facing portrait',
 'Thighs': 'face close-up, headshot, portrait framing, chest-up crop',
 'Knees': 'face close-up, headshot, portrait framing, upper-body crop',
 'Calves': 'face close-up, headshot, portrait framing, upper-body crop'}

