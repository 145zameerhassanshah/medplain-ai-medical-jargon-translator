# MedPlain AI

## Medical Jargon Translator — Streamlit + LLM API

MedPlain AI is an AI-powered healthcare communication application built with Python and Streamlit.

The application accepts a clinical note, sends it to an LLM API using a carefully designed healthcare-specific system prompt, and converts complex medical terminology into clear, patient-friendly language.

The original clinical note and simplified explanation are displayed side-by-side for easy comparison.

---

## Project Objective

The objective of this project is to demonstrate how Large Language Models can be integrated securely into a Python application for healthcare communication.

The system focuses on transforming complex clinical terminology into understandable language while preserving the original medical meaning.

---

## Core Features

- Clinical note text input
- AI-powered medical jargon simplification
- Patient-friendly plain-language explanations
- Original and translated text displayed side-by-side
- Multilingual-ready architecture
- English output
- Urdu output
- Roman Urdu output
- Arabic output
- Multiple reading levels
- Simple, Standard and Detailed explanation modes
- Secure API authentication using environment variables
- Input validation
- API error handling
- Rate-limit handling
- Responsive Streamlit interface
- Medical safety boundaries
- Privacy reminder for clinical data

---

## Supported Languages

The current application architecture supports:

- English
- Urdu
- Roman Urdu
- Arabic

Additional languages can be added easily through the configuration file.

---

## Reading Levels

### Simple
Uses shorter sentences and easier everyday language.

### Standard
Provides a balanced patient-friendly explanation.

### Detailed
Explains important medical terminology in greater detail while remaining understandable.

---

## Medical Safety Design

The system prompt is designed to reduce unsafe or misleading output.

The model is instructed to:

- Preserve the meaning of the original clinical note
- Preserve medical uncertainty
- Avoid inventing information
- Avoid converting suspected conditions into confirmed diagnoses
- Avoid diagnosing patients
- Avoid prescribing medication or treatment
- Preserve important measurements and test results
- Explain medical abbreviations only when their meaning is reasonably clear
- Use respectful and non-judgmental language

---

## Example

### Original Clinical Note

```text
Pt presents with SOB x 2 days.
CXR shows RLL infiltrate.
BP 150/95 mmHg.
Possible lower respiratory tract infection.
