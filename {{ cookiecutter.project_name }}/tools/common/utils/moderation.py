import openai
import logging
import os
from openai import OpenAI

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Use shared logging config (configured in graph_builder.py)
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI()

# Helper function for moderation check
def check_moderation(text: str) -> dict:
    """Check if the input text violates OpenAI's content policy using the Moderation API."""
    try:
        # Use the omni-moderation-latest model for moderation check
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=text
        )

        # Correctly access moderation results
        flagged = response.results[0].flagged
        categories = response.results[0].categories
        category_scores = response.results[0].category_scores

        # Log the moderation results
        logger.info(f"Moderation result: Flagged={flagged}, Categories={categories}, Scores={category_scores}")

        return {
            "flagged": flagged,
            "categories": categories,
            "category_scores": category_scores
        }
    except Exception as e:
        logger.error(f"Error during moderation check: {e}")
        return {"flagged": False, "categories": {}, "category_scores": {}}

if __name__ == "__main__":
    test_text = "This is a test message. Please check if this contains any harmful content."
    moderation_result = check_moderation(test_text)
    logger.info(f"Moderation result: {moderation_result}")