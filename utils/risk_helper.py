def get_risk_info(disease_type: str, predicted_class: str, confidence: float):
    disease_type = disease_type.lower().strip()
    predicted_class = predicted_class.strip()

    # Default
    risk_level = "Moderate Risk"
    urgency = "Medical follow-up is recommended."
    color = "yellow"

    # Skin
    if disease_type == "skin disease":
        if predicted_class == "mel":
            risk_level = "High Risk"
            urgency = "Urgent dermatology consultation is recommended."
            color = "red"
        elif predicted_class in ["bcc", "akiec"]:
            risk_level = "Moderate Risk"
            urgency = "Specialist dermatology follow-up is advised."
            color = "yellow"
        elif predicted_class in ["nv", "bkl", "df", "vasc"]:
            risk_level = "Low Risk"
            urgency = "Clinical review is still recommended for confirmation."
            color = "green"

    # Eye
    elif disease_type == "eye disease":
        if predicted_class in ["Glaucoma", "Diabetic_Retinopathy"]:
            risk_level = "High Risk"
            urgency = "Prompt ophthalmology follow-up is recommended."
            color = "red"
        elif predicted_class == "Cataract":
            risk_level = "Moderate Risk"
            urgency = "Ophthalmology examination is recommended."
            color = "yellow"
        elif predicted_class == "Normal":
            risk_level = "Low Risk"
            urgency = "Routine monitoring is sufficient if no symptoms are present."
            color = "green"

    # COVID
    elif disease_type == "covid-19":
        if predicted_class == "Covid":
            risk_level = "High Risk"
            urgency = "Clinical correlation and physician review are strongly recommended."
            color = "red"
        elif predicted_class == "Viral Pneumonia":
            risk_level = "Moderate Risk"
            urgency = "Medical evaluation is recommended."
            color = "yellow"
        elif predicted_class == "Normal":
            risk_level = "Low Risk"
            urgency = "No strong abnormal pattern detected."
            color = "green"

    # Breast
    elif disease_type == "breast cancer":
        if predicted_class == "malignant":
            risk_level = "High Risk"
            urgency = "Immediate specialist breast consultation is recommended."
            color = "red"
        elif predicted_class == "benign":
            risk_level = "Moderate Risk"
            urgency = "Specialist follow-up is recommended for confirmation."
            color = "yellow"
        elif predicted_class == "normal":
            risk_level = "Low Risk"
            urgency = "Routine screening and monitoring are recommended."
            color = "green"

    # Confidence adjustment
    if confidence < 0.50 and risk_level == "High Risk":
        urgency += " Confidence is limited, so expert confirmation is essential."

    return {
        "risk_level": risk_level,
        "urgency": urgency,
        "color": color
    }