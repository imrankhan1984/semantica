
import os
import sys
import json
from pprint import pprint

# Ensure the package is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantica.semantic_extract.methods import (
    extract_entities_llm, 
    extract_relations_llm, 
    extract_triplets_llm
)
from semantica.semantic_extract.providers import create_provider
from semantica.utils.exceptions import ProcessingError

# Set the API key
# Set the API key from environment
# We recommend setting it as an environment variable NOVITA_API_KEY
if not os.environ.get("NOVITA_API_KEY"):
    print("Warning: NOVITA_API_KEY not set. Test will likely fail.")

def test_NOVITA_all():
    text = "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. It is headquartered in Cupertino, California. The company designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories."
    
    print("--- Testing NOVITA Provider Availability ---")
    try:
        provider = create_provider("NOVITA")
        available = provider.is_available()
        print(f"NOVITA Available: {available}")
        if not available:
            print("Error: NOVITA is not available. Check library installation or API key.")
            return
    except Exception as e:
        print(f"Error checking provider: {e}")
        return

    print("\n--- Testing Entity Extraction ---")
    try:
        entities = extract_entities_llm(text, provider="NOVITA", model="deepseek/deepseek-v3.2")
        print(f"Extracted {len(entities)} entities:")
        pprint(entities)
    except Exception as e:
        print(f"Entity extraction failed: {e}")

    print("\n--- Testing Relation Extraction ---")
    try:
        # Use a few entities for relation extraction
        from semantica.semantic_extract.models import Entity
        sample_entities = [
            Entity(name="Apple Inc.", type="ORGANIZATION"),
            Entity(name="Steve Jobs", type="PERSON")
        ]
        relations = extract_relations_llm(text, entities=sample_entities, provider="NOVITA", model="deepseek/deepseek-v3.2")
        print(f"Extracted {len(relations)} relations:")
        pprint(relations)
    except Exception as e:
        print(f"Relation extraction failed: {e}")

    print("\n--- Testing Triplet Extraction ---")
    try:
        triplets = extract_triplets_llm(text, provider="NOVITA", model="deepseek/deepseek-v3.2")
        print(f"Extracted {len(triplets)} triplets:")
        pprint(triplets)
    except Exception as e:
        print(f"Triplet extraction failed: {e}")

    print("\n--- Testing Auto-Chunking ---")
    long_text = " ".join([text] * 10) # Roughly 1000-1500 tokens
    try:
        entities_chunked = extract_entities_llm(
            long_text, 
            provider="NOVITA", 
            model="deepseek/deepseek-v3.2",
            max_text_length=200 # Force chunking
        )
        print(f"Extracted {len(entities_chunked)} entities from long text (chunked):")
        # Just show count to avoid clutter
    except Exception as e:
        print(f"Chunked extraction failed: {e}")

if __name__ == "__main__":
    test_NOVITA_all()
