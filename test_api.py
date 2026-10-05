from prompts import build_system_prompt
from services.llm_service import translate_clinical_note


selected_language = "English"
reading_level = "Standard"

system_prompt = build_system_prompt(
    selected_language,
    reading_level,
)

clinical_note = """
Pt presents with SOB x 2 days.
CXR shows RLL infiltrate.
BP 150/95 mmHg.
Possible lower respiratory tract infection.
"""

result = translate_clinical_note(
    system_prompt=system_prompt,
    clinical_note=clinical_note,
)

print("\nORIGINAL CLINICAL NOTE:\n")
print(clinical_note)

print("\nPATIENT-FRIENDLY TRANSLATION:\n")
print(result)