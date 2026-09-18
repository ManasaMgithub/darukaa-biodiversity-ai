import re

REQUIRED_FACTORS = {
    "soil_organic_carbon": [
        "soil organic carbon",
        "soc",
        "organic carbon",
    ],
    "rainfall": [
        "rainfall",
        "rain",
        "precipitation",
    ],
    "land_use": [
        "land use",
        "land-use",
        "crop",
        "cropping",
        "monoculture",
        "forest",
        "agriculture",
        "urban",
        "farm",
        "farming",
        "wheat",
        "rice",
        "maize",
        "corn",
        "grassland",
    ],
}


def detect_factors(text):
    text_lower = text.lower()
    detected = {}

    # Soil Organic Carbon
    if any(
        keyword in text_lower
        for keyword in REQUIRED_FACTORS["soil_organic_carbon"]
    ):
        detected["soil_organic_carbon"] = extract_soc(text)

    # Rainfall
    if any(
        keyword in text_lower
        for keyword in REQUIRED_FACTORS["rainfall"]
    ):
        detected["rainfall"] = extract_rainfall(text)

    # Land use / crop system
    if any(
        keyword in text_lower
        for keyword in REQUIRED_FACTORS["land_use"]
    ):
        detected["land_use"] = extract_land_use(text)

    return detected


def extract_soc(text):
    """
    Extract SOC value when possible.
    Example:
    'SOC is 0.3%' -> '0.3%'
    """
    match = re.search(
        r"(?:soc|soil organic carbon|organic carbon)\s*(?:is|=|:)?\s*([\d.]+)\s*(%)?",
        text,
        re.IGNORECASE,
    )

    if match:
        value = match.group(1)
        unit = match.group(2) or ""
        return f"{value}{unit}"

    return text


def extract_rainfall(text):
    """
    Extract rainfall description.
    Example:
    'rainfall is low' -> 'low'
    """
    match = re.search(
        r"(?:rainfall|rain|precipitation)\s*(?:is|=|:)?\s*"
        r"(low|moderate|high|seasonal|irregular|heavy|limited|scarce)",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    return text


def extract_land_use(text):
    """
    Extract the crop/land-use description.
    """
    text_lower = text.lower()

    crop_keywords = [
        "wheat",
        "rice",
        "maize",
        "corn",
        "soybean",
        "cotton",
        "sugarcane",
    ]

    for crop in crop_keywords:
        if crop in text_lower:
            if "continuously" in text_lower or "continuous" in text_lower:
                return f"{crop} monoculture / continuous cropping"
            return crop

    if "monoculture" in text_lower:
        return "monoculture"

    if "forest" in text_lower:
        return "forest"

    if "grassland" in text_lower:
        return "grassland"

    if "urban" in text_lower:
        return "urban land"

    if "agriculture" in text_lower or "farm" in text_lower:
        return "agricultural land"

    return text


def get_missing_factors(environment_state):
    required = [
        "soil_organic_carbon",
        "rainfall",
        "land_use",
    ]

    return [
        factor
        for factor in required
        if factor not in environment_state
    ]


def build_clarification(missing_factors):
    questions = []

    if "soil_organic_carbon" in missing_factors:
        questions.append(
            "What is the approximate soil organic carbon (SOC) level?"
        )

    if "rainfall" in missing_factors:
        questions.append(
            "What is the rainfall pattern in the area "
            "(for example, low, moderate, high, seasonal, or irregular)?"
        )

    if "land_use" in missing_factors:
        questions.append(
            "What is the current land use or crop system "
            "(for example, wheat monoculture, mixed cropping, "
            "forest, grassland, or urban land)?"
        )

    return questions


def update_environment_state(environment_state, user_message):
    detected = detect_factors(user_message)

    for factor, value in detected.items():
        environment_state[factor] = value

    return environment_state


def conversation_status(environment_state):
    missing = get_missing_factors(environment_state)

    return {
        "complete": len(missing) == 0,
        "missing": missing,
        "questions": build_clarification(missing),
    }