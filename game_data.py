"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Kayla Bagley

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
# loading quests from a text file, validating its format. 
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError as e:
        raise MissingDataFileError(f"Quest data file not found: {filename}") from e
    except OSError as e:
        raise CorruptedDataError(f"Could not read quest data file: {filename}") from e
    blocks = []
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    quests = {}
    try:
        for block in blocks:
            quest = parse_quest_block(block)
            validate_quest_data(quest)
            quests[quest["quest_id"]] = quest
    except InvalidDataFormatError as e:
        raise InvalidDataFormatError(f"Invalid quest data format in file {filename}: {e}") from e
    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError as e:
        raise MissingDataFileError(f"Item data file not found: {filename}") from e
    except OSError as e:
        raise CorruptedDataError(f"Could not read item data file: {filename}") from e
    blocks = []
    current = []
    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    items = {}
    try:
        for block in blocks:
            item = parse_item_block(block)
            validate_item_data(item)
            items[item["item_id"]] = item
    except InvalidDataFormatError as e:
        raise InvalidDataFormatError(f"Invalid item data format in file {filename}: {e}") from e
    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
# make sure each quest dictionary has all required fields and correct types.
    if not isinstance(quest_dict, dict):
        raise InvalidDataFormatError("Quest data must be a dictionary.")
    required_fields = [
        "quest_id",
        "title",
        "description",
        "reward_xp",
        "reward_gold",
        "required_level",
        "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {field}")
    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in numeric_fields:
        if not isinstance(quest_dict[field], int):
            raise InvalidDataFormatError(f"Quest field {field} must be an integer.")
    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
# if ANYTHING is missing from required fields raise error
    if not isinstance(item_dict, dict):
        raise InvalidDataFormatError("Item data must be a dictionary.")
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {field}")
    valid_types = {"weapon", "armor", "consumable"}
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be an integer.")
    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
# test all txt files, if they some aren't created, create 
# it with defaults.
    os.makedirs("data", exist_ok=True)
    quests_path = os.path.join("data", "quests.txt")
    items_path = os.path.join("data", "items.txt")
    if not os.path.exists(quests_path):
        quests_content = (
            "QUEST_ID: goblin_cave\n"
            "TITLE: Goblin Cave\n"
            "DESCRIPTION: Clear out the goblins attacking the village.\n"
            "REWARD_XP: 50\n"
            "REWARD_GOLD: 30\n"
            "REQUIRED_LEVEL: 1\n"
            "PREREQUISITE: NONE\n"
            "\n"
            "QUEST_ID: dragon_mountain\n"
            "TITLE: Dragon of the Mountain\n"
            "DESCRIPTION: Defeat the dragon terrorizing the kingdom.\n"
            "REWARD_XP: 200\n"
            "REWARD_GOLD: 150\n"
            "REQUIRED_LEVEL: 5\n"
            "PREREQUISITE: goblin_cave\n"
        )
        with open(quests_path, "w", encoding="utf-8") as f:
            f.write(quests_content)
    if not os.path.exists(items_path):
        items_content = (
            "ITEM_ID: health_potion\n"
            "NAME: Small Health Potion\n"
            "TYPE: consumable\n"
            "EFFECT: health:20\n"
            "COST: 25\n"
            "DESCRIPTION: Restores a small amount of health.\n"
            "\n"
            "ITEM_ID: iron_sword\n"
            "NAME: Iron Sword\n"
            "TYPE: weapon\n"
            "EFFECT: strength:5\n"
            "COST: 100\n"
            "DESCRIPTION: A basic but reliable iron sword.\n"
        )
        with open(items_path, "w", encoding="utf-8") as f:
            f.write(items_content)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
# raise error and then split into key & valye
    data = {}
    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Missing ':' in quest line.")
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        data[key] = value
    try:
        quest_id = data["QUEST_ID"]
        title = data["TITLE"]
        description = data["DESCRIPTION"]
        reward_xp = int(data["REWARD_XP"])
        reward_gold = int(data["REWARD_GOLD"])
        required_level = int(data["REQUIRED_LEVEL"])
        prereq_raw = data.get("PREREQUISITE", "NONE")
    except (KeyError, ValueError) as e:
        raise InvalidDataFormatError("Invalid quest block format.") from e
    prerequisite = None if prereq_raw.upper() == "NONE" else prereq_raw
    quest = {
        "quest_id": quest_id,
        "title": title,
        "description": description,
        "reward_xp": reward_xp,
        "reward_gold": reward_gold,
        "required_level": required_level,
        "prerequisite": prerequisite
    }
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
# parse KEY/VALUE pairs, raise error 
    data = {}
    for line in lines:
        if ":" not in line:
            raise InvalidDataFormatError("Missing ':' in item line.")
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        data[key] = value
    try:
        item_id = data["ITEM_ID"]
        name = data["NAME"]
        item_type = data["TYPE"].lower()
        effect = data["EFFECT"]
        cost = int(data["COST"])
        description = data["DESCRIPTION"]
    except (KeyError, ValueError) as e:
        raise InvalidDataFormatError("Invalid item block format.") from e
    item = {
        "item_id": item_id,
        "name": name,
        "type": item_type,
        "effect": effect,
        "cost": cost,
        "description": description
    }
    return item


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

