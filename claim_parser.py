print("claim_parser loaded")

def parse_claim(user_claim):
    claim = str(user_claim).lower()

    issue_type = "unknown"
    object_part = "unknown"

    # Damage types
    if "scratch" in claim:
        issue_type = "scratch"
    elif "dent" in claim:
        issue_type = "dent"
    elif "crack" in claim:
        issue_type = "crack"
    elif "broken" in claim:
        issue_type = "broken_part"
    elif "missing" in claim:
        issue_type = "missing_part"
    elif "water" in claim:
        issue_type = "water_damage"
    elif "stain" in claim:
        issue_type = "stain"

    # Object parts
    if "front bumper" in claim:
        object_part = "front_bumper"
    elif "rear bumper" in claim:
        object_part = "rear_bumper"
    elif "door" in claim:
        object_part = "door"
    elif "hood" in claim:
        object_part = "hood"
    elif "windshield" in claim:
        object_part = "windshield"
    elif "mirror" in claim:
        object_part = "side_mirror"
    elif "headlight" in claim:
        object_part = "headlight"
    elif "taillight" in claim:
        object_part = "taillight"
    elif "screen" in claim:
        object_part = "screen"
    elif "keyboard" in claim:
        object_part = "keyboard"
    elif "trackpad" in claim:
        object_part = "trackpad"
    elif "hinge" in claim:
        object_part = "hinge"
    elif "box" in claim:
        object_part = "box"
    elif "seal" in claim:
        object_part = "seal"
    elif "label" in claim:
        object_part = "label"

    return {
        "issue_type": issue_type,
        "object_part": object_part
    }