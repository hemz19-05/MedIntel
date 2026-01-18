def detect_intent(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["interaction", "combine", "together"]):
        return "interactions"

    if any(word in text for word in ["contraindication", "should not", "avoid", "issue", "problem"]):
        return "contraindications"

    if any(word in text for word in ["side effect", "adverse"]):
        return "side_effects"

    if any(word in text for word in ["pregnan", "conception", "conceiv", "breastfeeding", "lactati"]):
        return "pregnancy/breastfeeding"

    if any(word in text for word in ["dose", "dosage", "how much", "taken"]):
        return "dosage"

    return "general"


    
