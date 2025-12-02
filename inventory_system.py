"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Kayla Bagley

AI Usage: Needed help to parse through item effect strings and managing the character's inventory list with files, used Google Gemini.

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
# checks if inventory full. full, raise error. else, append 
# item_id to inventory list
    inventory = character.get("inventory", [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")
    inventory.append(item_id)
    character["inventory"] = inventory
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
# if item isn't in inventory list, raise error. else, 
# remove 1 copy and return True.
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
    inventory.remove(item_id)
    character["inventory"] = inventory
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
# returns true if item is in inventory list, else false
    return item_id in character.get("inventory", [])

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
# return how many copies of specific item, 'count()'.
    return character.get("inventory", []).count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    return MAX_INVENTORY_SIZE - len(character.get("inventory", []))

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
# saves copy of current inventory, then clears it. returns 
# the list of removed items.
    inventory = character.get("inventory", [])
    removed = list(inventory)
    character["inventory"] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
# checks for item, then it is described by type & effect.
# if not, raise error. else, parse effect,

    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
    if item_data.get("type") != "consumable":
        raise InvalidItemTypeError("Only consumable items can be used.")
    effect_string = item_data.get("effect", "")
    stat_name, value = parse_item_effect(effect_string)
    apply_stat_effect(character, stat_name, value)
    remove_item_from_inventory(character, item_id)
    item_name = item_data.get("name", item_id)
    return f"Used {item_name}. {stat_name} changed by {value}."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
# makes sure character has item. if not, raise error. if 
# weapon is already equpped reme state bonus.
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")
    current_id = character.get("equipped_weapon_id")
    current_bonus = character.get("equipped_weapon_bonus", 0)
    current_stat = character.get("equipped_weapon_stat")
    if current_id is not None:
        apply_stat_effect(character, current_stat, -current_bonus)
        add_item_to_inventory(character, current_id)
    stat_name, value = parse_item_effect(item_data.get("effect", "strength:0"))
    remove_item_from_inventory(character, item_id)
    apply_stat_effect(character, stat_name, value)
    character["equipped_weapon_id"] = item_id
    character["equipped_weapon_bonus"] = value
    character["equipped_weapon_stat"] = stat_name
    item_name = item_data.get("name", item_id)
    return f"Equipped {item_name}."

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
# same thing as 'equip_weapon', but for armor.
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
    if item_data.get("type") != "armor":
        raise InvalidItemTypeError("Item is not armor.")
    current_id = character.get("equipped_armor_id")
    current_bonus = character.get("equipped_armor_bonus", 0)
    current_stat = character.get("equipped_armor_stat")
    if current_id is not None:
        apply_stat_effect(character, current_stat, -current_bonus)
        add_item_to_inventory(character, current_id)
    stat_name, value = parse_item_effect(item_data.get("effect", "max_health:0"))
    remove_item_from_inventory(character, item_id)
    apply_stat_effect(character, stat_name, value)
    character["equipped_armor_id"] = item_id
    character["equipped_armor_bonus"] = value
    character["equipped_armor_stat"] = stat_name
    item_name = item_data.get("name", item_id)
    return f"Equipped {item_name}."

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
# if no weapon equipped, return none. if inventory full, raise
    current_id = character.get("equipped_weapon_id")
    if current_id is None:
        return None
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")
    current_bonus = character.get("equipped_weapon_bonus", 0)
    current_stat = character.get("equipped_weapon_stat")
    apply_stat_effect(character, current_stat, -current_bonus)
    add_item_to_inventory(character, current_id)
    character["equipped_weapon_id"] = None
    character["equipped_weapon_bonus"] = 0
    character["equipped_weapon_stat"] = None
    return current_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
# same as 'unequip_weapon', but for armor.
    current_id = character.get("equipped_armor_id")
    if current_id is None:
        return None
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")
    current_bonus = character.get("equipped_armor_bonus", 0)
    current_stat = character.get("equipped_armor_stat")
    apply_stat_effect(character, current_stat, -current_bonus)
    add_item_to_inventory(character, current_id)
    character["equipped_armor_id"] = None
    character["equipped_armor_bonus"] = 0
    character["equipped_armor_stat"] = None
    return current_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
# price of item. subtract cost from character, then add to 
# inventory.if not enough gold, raise error. same for full inv
    cost = item_data.get("cost", 0)
    gold = character.get("gold", 0)
    if gold < cost:
        raise InsufficientResourcesError("Not enough gold to purchase item.")
    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")
    character["gold"] = gold - cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
# sell price: '//2'. if don't have item, raise error. remove
#  item from inv, add self price to character, then return gold gained.
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item {item_id} not found in inventory.")
    cost = item_data.get("cost", 0)
    sell_price = cost // 2
    remove_item_from_inventory(character, item_id)
    character["gold"] = character.get("gold", 0) + sell_price
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
# SPLITS STRINGS
    parts = effect_string.split(":", 1)
    if len(parts) != 2:
        raise ValueError("Invalid effect format.")
    stat_name = parts[0].strip()
    value = int(parts[1].strip())
    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
# adding specific value to stats 
    if stat_name not in character:
        character[stat_name] = 0
    character[stat_name] += value
    if stat_name == "health":
        max_health = character.get("max_health", character["health"])
        if character["health"] > max_health:
            character["health"] = max_health

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
# gets inventory list. and full databse of full items.
#  if empty, print empty message. 
    inventory = character.get("inventory", [])
    if not inventory:
        print("Inventory is empty.")
        return
    counts = {}
    for item_id in inventory:
        counts[item_id] = counts.get(item_id, 0) + 1
    print("Inventory:")
    for item_id, qty in counts.items():
        data = item_data_dict.get(item_id, {})
        name = data.get("name", item_id)
        item_type = data.get("type", "unknown")
        print(f"- {name} (x{qty}) [{item_type}]")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

