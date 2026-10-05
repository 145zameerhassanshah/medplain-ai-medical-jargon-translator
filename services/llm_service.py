import time

from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
)

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
)


def get_client():
    """
    Create and return an authenticated OpenRouter client.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is missing. "
            "Add it to the .env file."
        )

    return OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )


def translate_clinical_note(
    system_prompt: str,
    clinical_note: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 800,
    max_retries: int = 3,
) -> str:
    """
    Send a clinical note to OpenRouter and return
    a patient-friendly plain-language explanation.
    """

    if not clinical_note or not clinical_note.strip():
        return "Please enter a clinical note."

    client = get_client()

    for attempt in range(max_retries):
        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": clinical_note.strip(),
                    },
                ],
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                return (
                    "The AI returned an empty response. "
                    "Please try again."
                )

            return content.strip()

        except AuthenticationError as error:
            print(
                f"AuthenticationError: {error}"
            )

            return (
                "Authentication failed. "
                "Please check your OpenRouter API key."
            )

        except RateLimitError as error:
            print(
                f"RateLimitError: {error}"
            )

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue

            return (
                "The free AI service is temporarily busy "
                "or has reached its request limit. "
                "Please try again shortly."
            )

        except APITimeoutError as error:
            print(
                f"APITimeoutError: {error}"
            )

            return (
                "The AI service took too long to respond. "
                "Please try again."
            )

        except APIConnectionError as error:
            print(
                f"APIConnectionError: {error}"
            )

            return (
                "Unable to connect to the AI service. "
                "Please check your internet connection."
            )

        except BadRequestError as error:
            print(
                f"BadRequestError: {error}"
            )

            return (
                "The request could not be processed. "
                "Please review the clinical note and try again."
            )

        except Exception as error:
            print(
                f"Unexpected error: "
                f"{type(error).__name__}: {error}"
            )

            return (
                "Something went wrong while generating "
                "the translation. Please try again."
            )

    return (
        "The translation could not be generated. "
        "Please try again."
    )