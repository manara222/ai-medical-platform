def generate_chatbot_response(user_message: str, case_info: dict) -> str:
    disease_type = case_info.get("disease_type", "Unknown")
    predicted_class = case_info.get("predicted_class", "Unknown")
    clinical_insight = case_info.get("clinical_insight", "Clinical review is recommended.")
    next_step = case_info.get("next_step", "Consult a medical specialist.")
    risk_level = case_info.get("risk_level", "Moderate Risk")
    urgency = case_info.get("urgency", "Medical follow-up is recommended.")

    user_message = user_message.lower().strip()

    if any(word in user_message for word in ["what", "what does this mean", "meaning", "يعني", "ايه", "يعني ايه"]):
        return (
            f"The system predicted **{predicted_class}** under **{disease_type}**.\n\n"
            f"Clinical insight: {clinical_insight}\n\n"
            f"Risk level: {risk_level}\n\n"
            f"This means the uploaded image shows patterns most consistent with this category."
        )

    if any(word in user_message for word in ["next", "next step", "what should i do", "اعمل ايه", "الخطوة الجاية", "ماذا أفعل"]):
        return f"Recommended next step: {next_step}"

    if any(word in user_message for word in ["risk", "serious", "dangerous", "خطير", "هل ده خطر", "urgency"]):
        return (
            f"Risk level: {risk_level}\n\n"
            f"Urgency: {urgency}\n\n"
            f"Clinical insight: {clinical_insight}"
        )

    if any(word in user_message for word in ["confidence", "how sure", "الثقة", "هل النتيجة مؤكدة"]):
        return (
            "The confidence score reflects how strongly the AI model supports its selected class. "
            "A higher score means the model is more certain, but medical confirmation is still important."
        )

    if any(word in user_message for word in ["doctor", "specialist", "consult", "دكتور", "اكشف", "طبيب"]):
        return f"Yes, medical follow-up is recommended.\n\nSuggested next action: {next_step}"

    return (
        f"I am an AI medical assistant for this case.\n\n"
        f"Disease type: {disease_type}\n"
        f"Predicted class: {predicted_class}\n"
        f"Risk level: {risk_level}\n"
        f"Clinical insight: {clinical_insight}\n"
        f"Recommended next step: {next_step}\n\n"
        f"You can ask me:\n"
        f"- What does this result mean?\n"
        f"- What should I do next?\n"
        f"- Is this serious?\n"
        f"- How confident is the AI?"
    )