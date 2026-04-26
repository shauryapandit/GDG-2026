"""
Bias Analyzer — wraps the Google Gemini API to perform structured bias detection.
Loads API key from the GEMINI_API_KEY environment variable.
"""

import json
import os
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT_TEMPLATE


class BiasAnalysisError(Exception):
    """Raised when bias analysis fails."""
    pass


class BiasAnalyzer:
    """Analyzes LLM-generated text for bias using the Gemini API."""

    MODEL = "gemini-2.5-flash"

    def __init__(self, api_key: str | None = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise BiasAnalysisError(
                "Please enter your Gemini API key in the sidebar."
            )
        self.client = genai.Client(api_key=api_key)

    def analyze(self, text: str) -> dict:
        """
        Send text to Gemini for bias analysis.

        Args:
            text: The LLM-generated text to analyze.

        Returns:
            A dict with keys: overall_bias_score, summary, biases (list).

        Raises:
            BiasAnalysisError: If the API call or parsing fails.
        """
        if not text or not text.strip():
            raise BiasAnalysisError("Please provide non-empty text to analyze.")

        prompt = ANALYSIS_PROMPT_TEMPLATE.format(text=text)

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,  # Low temperature for consistent, analytical output
                ),
            )
        except Exception as e:
            raise BiasAnalysisError(f"Gemini API call failed: {e}") from e

        # Parse the JSON response
        try:
            result = json.loads(response.text)
        except (json.JSONDecodeError, TypeError) as e:
            raise BiasAnalysisError(
                f"Failed to parse Gemini response as JSON: {e}\n"
                f"Raw response: {response.text[:500]}"
            ) from e

        # Validate required keys
        if "overall_bias_score" not in result:
            result["overall_bias_score"] = 0
        if "summary" not in result:
            result["summary"] = "Analysis complete."
        if "biases" not in result:
            result["biases"] = []

        return result
