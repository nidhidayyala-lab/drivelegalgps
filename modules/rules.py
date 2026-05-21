from difflib import SequenceMatcher
import re

# Clean rule database (expandable)
VIOLATION_RULES = {
    "helmet": ("Helmet Not Worn", "MV Act 129", 1000),
    "seatbelt": ("Seatbelt Not Worn", "MV Act 138", 1000),
    "triple ride": ("Triple Riding", "MV Act 128", 1000),

    "speed": ("Over Speeding", "MV Act 183", 1500),
    "signal": ("Signal Jump", "MV Act 184", 1000),

    "license": ("No Driving License", "MV Act 181", 5000),
    "insurance": ("No Insurance", "MV Act 196", 2000),

    "no parking": ("No Parking", "MV Act 122", 500),

    "mobile": ("Mobile Phone While Driving", "MV Act 184", 1000),

    "drunk": ("Drunk Driving", "MV Act 185", 10000),

    "pollution": ("PUC Violation", "MV Act 190", 1000)
}

# -----------------------------
# MULTI-VIOLATION DETECTION
# -----------------------------
def detect_violations(text):

    found = []
    added = set()

    text = text.lower()
    words = text.split()

    for key, value in VIOLATION_RULES.items():

        matched = False

        # 1. Exact phrase match
        if key in text:
            matched = True

        # 2. Fuzzy match (OCR mistakes)
        else:
            for word in words:

                score = SequenceMatcher(None, key, word).ratio()

                if score >= 0.75:
                    matched = True
                    break

        if matched and value[0] not in added:

            found.append({
                "violation": value[0],
                "act": value[1],
                "fine": value[2],

                "english": f"{value[0]} is punishable under MV Act.",
                "hindi": "यह मोटर वाहन अधिनियम के तहत दंडनीय अपराध है।",
                "telugu": "ఇది మోటార్ వాహన చట్టం ప్రకారం శిక్షార్హమైన నేరం."
            })

            added.add(value[0])

    return found


# -----------------------------
# ACTUAL FINE EXTRACTION
# -----------------------------
def extract_actual_fine(text):

    numbers = re.findall(r'\d+', text)

    valid = []

    for n in numbers:

        val = int(n)

        # ignore years / small numbers
        if 100 <= val <= 100000:
            valid.append(val)

    return max(valid) if valid else 0