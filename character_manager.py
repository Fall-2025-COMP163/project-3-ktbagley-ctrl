"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Kayla Bagley]

AI Usage: For the save character section, Gemini helped me to save the directory exists with the 'os.makedirs'.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================
# module is responsible for creating, saving, loading, 
# and updating player characters

# creating new characters, loads and saves save files. 
# as well as raising custom exceptions.
def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
# validates class that user requests by returning dictionary
# of base stats. If invalid, raises error

    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid character class: {character_class}")
    base = valid_classes[character_class]
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    validate_character_data(character)
    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
# make sure to write all of the character info line by 
# line in the file.


    validate_character_data(character)
    os.makedirs(save_directory, exist_ok=True)
    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)
    inventory_str = ",".join(character["inventory"])
    active_str = ",".join(character["active_quests"])
    completed_str = ",".join(character["completed_quests"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"NAME: {character['name']}\n")
        f.write(f"CLASS: {character['class']}\n")
        f.write(f"LEVEL: {character['level']}\n")
        f.write(f"HEALTH: {character['health']}\n")
        f.write(f"MAX_HEALTH: {character['max_health']}\n")
        f.write(f"STRENGTH: {character['strength']}\n")
        f.write(f"MAGIC: {character['magic']}\n")
        f.write(f"EXPERIENCE: {character['experience']}\n")
        f.write(f"GOLD: {character['gold']}\n")
        f.write(f"INVENTORY: {inventory_str}\n")
        f.write(f"ACTIVE_QUESTS: {active_str}\n")
        f.write(f"COMPLETED_QUESTS: {completed_str}\n")
    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
# i make sure to have a bunch of errors ready to be raised 
# if saving the file goes wrong.
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        raise SaveFileCorruptedError(f"Could not read save file for '{character_name}'.") from e
    data_map = {}
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()
        data_map[key] = value
    try:
        inventory_list = [item for item in data_map.get("INVENTORY", "").split(",") if item] if "INVENTORY" in data_map else []
        active_list = [q for q in data_map.get("ACTIVE_QUESTS", "").split(",") if q] if "ACTIVE_QUESTS" in data_map else []
        completed_list = [q for q in data_map.get("COMPLETED_QUESTS", "").split(",") if q] if "COMPLETED_QUESTS" in data_map else []
        character = {
            "name": data_map["NAME"],
            "class": data_map["CLASS"],
            "level": int(data_map["LEVEL"]),
            "health": int(data_map["HEALTH"]),
            "max_health": int(data_map["MAX_HEALTH"]),
            "strength": int(data_map["STRENGTH"]),
            "magic": int(data_map["MAGIC"]),
            "experience": int(data_map["EXPERIENCE"]),
            "gold": int(data_map["GOLD"]),
            "inventory": inventory_list,
            "active_quests": active_list,
            "completed_quests": completed_list
        }
    except (KeyError, ValueError) as e:
        raise InvalidSaveDataError("Save data is missing fields or has invalid types.") from e
    validate_character_data(character)
    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
# scans saved directory and then returns base name of files.
# if directory doesn't exist, returns empty list.

    if not os.path.isdir(save_directory):
        return []
    names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            base = filename[:-9]
            names.append(base)
    return names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
# scans for the character save file and deletes it.
# raises CharacterNotFoundError if file doesn't exist.

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    os.remove(filepath)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
# handles experience gain and levels up character. When 
# character levels up, stats are increased and health restored.
# Raises CharacterDeadError if character is dead.
    if character.get("health", 0) <= 0:
        raise CharacterDeadError("Cannot gain experience when dead.")
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
# adds or subtracts gold from character. Raises ValueError
# if resulting gold would be negative.
    new_total = character.get("gold", 0) + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative.")
    character["gold"] = new_total
    return new_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """

# heals character by given amount without exceeding max health.
# returns actual amount healed, so user knows. 
    if amount <= 0:
        return 0
    max_health = character.get("max_health", 0)
    current_health = character.get("health", 0)
    missing = max_health - current_health
    if missing <= 0:
        return 0
    actual_heal = amount if amount <= missing else missing
    character["health"] = current_health + actual_heal
    return actual_heal

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
# helper that checks if character is dead based on health.
    return character.get("health", 0) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
# revives character if dead by setting health to 50% of max health.
    if not is_character_dead(character):
        return False
    max_health = character.get("max_health", 0)
    revived_health = max_health // 2
    if revived_health <= 0 and max_health > 0:
        revived_health = max_health
    character["health"] = revived_health
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """

# safety check on all files 
    if not isinstance(character, dict):
        raise InvalidSaveDataError("Character data must be a dictionary.")
    required_fields = [
        "name",
        "class",
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold",
        "inventory",
        "active_quests",
        "completed_quests"
    ]
    for field in required_fields:
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
    if not isinstance(character["name"], str) or not isinstance(character["class"], str):
        raise InvalidSaveDataError("Name and class must be strings.")
    numeric_fields = [
        "level",
        "health",
        "max_health",
        "strength",
        "magic",
        "experience",
        "gold"
    ]
    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Field {field} must be an integer.")
    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Field {field} must be a list.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

