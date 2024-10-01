from typing import List, Dict, Any, Optional
import hashlib


def extract_required_fields(settings: List[Dict[str, Any]], required_fields: List[str]) -> List[Dict[str, Any]]:
    """Extract only the required fields from the settings."""
    extracted_settings = []

    for setting in settings:
        extracted = {field: setting.get(field) for field in required_fields}
        extracted_settings.append(extracted)

    return extracted_settings


def extract_required_fields_v2(settings: List[Dict[str, Any]], field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    """Extract fields based on the field mapping and return them in the new structure."""
    extracted_settings = []

    for setting in settings:
        extracted = {source_field: setting.get(target_field) for source_field, target_field in field_mapping.items()}
        extracted_settings.append(extracted)

    return extracted_settings


def build_single_key_lookup_table(
        settings: List[Dict[str, Any]],
        key_field: str
) -> Dict[Any, List[Dict[str, Any]]]:
    """Build a lookup table with a single key field."""

    lookup_table = {}

    for setting in settings:
        key_value = setting.get(key_field)

        if key_value is not None:
            if key_value in lookup_table:
                lookup_table[key_value].append(setting)
            else:
                lookup_table[key_value] = [setting]

    return lookup_table


def get_setting_by_single_key(
        lookup_table: Dict[Any, List[Dict[str, Any]]],
        key_value: Any
) -> Optional[List[Dict[str, Any]]]:
    """Fetch settings based on a single key in O(1) time."""
    return lookup_table.get(key_value, None)


def encode_in_sha256(input_string):
    """Generate a SHA256 hash of the given string."""
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()


async def generate_md5_to_push_mention_to_cache(category_id, brand_id, channel_type, social_id):
    """Generate an SHA256 hash based on category ID, brand ID, channel type, and social ID."""
    try:
        # Build the base string using the provided parameters
        base_string = f"{category_id}:{brand_id}:{channel_type}:"

        # Validate the social_id
        if not social_id:
            raise ValueError("Invalid or Null SocialID")

        # Append the social_id to the base string
        base_string += social_id

        # Generate the SHA256 hash from the base string
        md5_cache_key = encode_in_sha256(base_string.lower())

        return md5_cache_key
    except Exception as ex:
        print(f"Error: {ex}")
        return None
