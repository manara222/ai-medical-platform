def get_clinical_recommendation(predicted_class: str):
    clinical_notes = {
        "akiec": "Possible actinic keratosis-type lesion. Dermatology review is recommended.",
        "bcc": "Possible basal cell carcinoma pattern. Specialist dermatology follow-up is advised.",
        "bkl": "Possible benign keratosis-like lesion. Clinical confirmation is recommended.",
        "df": "Possible dermatofibroma-like finding. A dermatologist can confirm the diagnosis.",
        "mel": "Possible melanoma-related pattern. Urgent dermatology consultation is recommended.",
        "nv": "Likely nevus-type lesion. Clinical review is still advised.",
        "vasc": "Possible vascular lesion pattern. Specialist evaluation is recommended.",

        "Cataract": "Possible cataract-related pattern. Ophthalmology examination is recommended.",
        "Diabetic_Retinopathy": "Possible diabetic retinopathy finding. Retina specialist follow-up is advised.",
        "Glaucoma": "Possible glaucoma-related retinal changes. Eye pressure and optic nerve evaluation are recommended.",
        "Normal": "No strong abnormal pattern detected, but medical review is still encouraged if symptoms exist.",

        "Covid": "Possible COVID-related chest X-ray pattern. Clinical review and further testing are recommended.",
        "Viral Pneumonia": "Possible viral pneumonia pattern. Physician consultation is advised.",

        "benign": "The lesion appears more likely benign, but specialist confirmation is recommended.",
        "malignant": "The lesion appears suspicious. Immediate specialist follow-up is strongly advised.",
        "normal": "No strong abnormal breast ultrasound pattern detected, but routine follow-up is still recommended."
    }

    next_steps = {
        "akiec": "Book a dermatology appointment and consider dermoscopic evaluation.",
        "bcc": "Consult a dermatologist for further assessment and possible biopsy.",
        "bkl": "Perform clinical skin examination to confirm the lesion type.",
        "df": "Dermatology review is recommended for confirmation.",
        "mel": "Seek urgent dermatology consultation as soon as possible.",
        "nv": "Monitor clinically and confirm with a dermatologist if needed.",
        "vasc": "Consult a specialist for vascular lesion assessment.",

        "Cataract": "Schedule an ophthalmology examination.",
        "Diabetic_Retinopathy": "Retina screening and diabetic eye follow-up are recommended.",
        "Glaucoma": "Perform glaucoma-focused ophthalmology evaluation.",
        "Normal": "Continue routine monitoring if symptoms are absent.",

        "Covid": "Correlate with clinical symptoms and seek physician review.",
        "Viral Pneumonia": "Visit a physician for chest evaluation and treatment guidance.",

        "benign": "Continue specialist follow-up to confirm the benign nature.",
        "malignant": "Immediate breast specialist consultation is recommended.",
        "normal": "Continue routine screening if needed."
    }

    return {
        "clinical_insight": clinical_notes.get(predicted_class, "Clinical review is recommended."),
        "next_step": next_steps.get(predicted_class, "Consult a medical specialist.")
    }