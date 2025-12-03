"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Kayla Bagley

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================
# brings everything together
def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
# displays starting choices, returns user choice as well as
# route to either new game, load game, or quit.
    def main_menu():
     print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Quit")
    choice = input("Choose an option (1-3): ").strip()
    try:
        return int(choice)
    except ValueError:
        return 0

def new_game():
    global current_character
# ask character their name & class. calls character manager 
# to build character dictionary. stores it.
    print("\n=== NEW GAME ===")
    name = input("Enter your character's name: ").strip()
    print("Choose a class: Warrior, Mage, Rogue, Cleric")
    character_class = input("Class: ").strip().title()
    try:
        current_character = character_manager.create_character(name, character_class)
        print(f"\nCreated {current_character['name']} the {current_character['class']}!")
        game_loop()
    except Exception as e:
        print(f"Error creating character: {e}")

def load_game():
# shows all saved characters, lets player pick one to load. 
# uses load_character to restoore it.
    global current_character
    print("\n=== LOAD GAME ===")
    try:
        saved_names = character_manager.list_saved_characters()
    except Exception as e:
        print(f"Error listing saves: {e}")
        return
    if not saved_names:
        print("No saved games found.")
        return
    print("Saved Characters:")
    for index, name in enumerate(saved_names, start=1):
        print(f"{index}. {name}")
    choice = input("Select a character number to load: ").strip()
    try:
        idx = int(choice)
        if idx < 1 or idx > len(saved_names):
            print("Invalid selection.")
            return
        selected_name = saved_names[idx - 1]
        try:
            current_character = character_manager.load_character(selected_name)
            print(f"\nLoaded {current_character['name']} the {current_character['class']}.")
            game_loop()
        except CharacterNotFoundError:
            print("Character save not found.")
        except SaveFileCorruptedError:
            print("Save file is corrupted.")
        except InvalidSaveDataError as e:
            print(f"Invalid save data: {e}")
    except ValueError:
        print("Invalid input. Please enter a number.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
# main game loop. shows gamme menu, execute functions, and 
# keeps going until player choses to save & quit.
    global game_running, current_character
    
    game_running = True
    
    while game_running and current_character is not None:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Returning to main menu.")
            game_running = False
        else:
            print("Invalid choice. Please select 1-6.")

def game_menu():
    """
    Display game menu and get player choice
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    choice = input("Choose an option (1-6): ").strip()
    try:
        return int(choice)
    except ValueError:
        return 0
    
# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
# just simply reads fields from character dictionary while 
# also displaying all quests
    global current_character
    
    if current_character is None:
        print("No character loaded.")
        return
    c = current_character
    print("\n=== CHARACTER STATS ===")
    print(f"Name:   {c.get('name')}")
    print(f"Class:  {c.get('class')}")
    print(f"Level:  {c.get('level')}")
    print(f"HP:     {c.get('health')}/{c.get('max_health')}")
    print(f"STR:    {c.get('strength')}")
    print(f"MAG:    {c.get('magic')}")
    print(f"XP:     {c.get('experience')}")
    print(f"Gold:   {c.get('gold')}")
    active = c.get("active_quests", [])
    completed = c.get("completed_quests", [])
    print("\nActive Quests:")
    if not active:
        print("  None")
    else:
        for qid in active:
            q = all_quests.get(qid, {})
            title = q.get("title", qid)
            print(f"  - {title} ({qid})")
    print("\nCompleted Quests:")
    if not completed:
        print("  None")
    else:
        for qid in completed:
            q = all_quests.get(qid, {})
            title = q.get("title", qid)
            print(f"  - {title} ({qid})")

def view_inventory():
    """Display and manage inventory"""
# lets player usee items, equip gear, or drop items from inventory.
    global current_character, all_items
    if current_character is None:
        print("No character loaded.")
        return
    while True:
        print("\n=== INVENTORY ===")
        inventory_system.display_inventory(current_character, all_items)
        print("\nInventory Options:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            break
        item_id = input("Enter item ID: ").strip()
        if item_id not in all_items:
            print("Unknown item ID.")
            continue
        item_info = all_items[item_id]
        try:
            if choice == "1":
                message = inventory_system.use_item(current_character, item_id, item_info)
                print(message)
            elif choice == "2":
                message = inventory_system.equip_weapon(current_character, item_id, item_info)
                print(message)
            elif choice == "3":
                message = inventory_system.equip_armor(current_character, item_id, item_info)
                print(message)
            elif choice == "4":
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_info.get('name', item_id)}.")
            else:
                print("Invalid choice.")
        except ItemNotFoundError as e:
            print(e)
        except InvalidItemTypeError as e:
            print(e)
        except InventoryFullError as e:
            print(e)
        except InsufficientResourcesError as e:
            print(e)

def quest_menu():
    """Quest management menu"""
# MANAGES quest lists stored on character. show active/available/completed quests.
# lets player accept new quests, abandon active quests, and complete quests for rewards.
    global current_character, all_quests
    if current_character is None:
        print("No character loaded.")
        return
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        choice = input("Choose an option (1-7): ").strip()
        c = current_character
        active = c.get("active_quests", [])
        completed = c.get("completed_quests", [])
        if choice == "1":
            print("\nActive Quests:")
            if not active:
                print("  None")
            else:
                for qid in active:
                    q = all_quests.get(qid, {})
                    title = q.get("title", qid)
                    print(f"  - {title} ({qid})")
        elif choice == "2":
            print("\nAvailable Quests:")
            available = []
            for qid, q in all_quests.items():
                if qid in active or qid in completed:
                    continue
                if c.get("level", 1) >= q.get("required_level", 1):
                    available.append((qid, q))
            if not available:
                print("  None")
            else:
                for qid, q in available:
                    print(f"  - {q.get('title', qid)} ({qid})")
        elif choice == "3":
            print("\nCompleted Quests:")
            if not completed:
                print("  None")
            else:
                for qid in completed:
                    q = all_quests.get(qid, {})
                    title = q.get("title", qid)
                    print(f"  - {title} ({qid})")
        elif choice == "4":
            qid = input("Enter quest ID to accept: ").strip()
            if qid not in all_quests:
                print("Quest not found.")
                continue
            if qid in active:
                print("Quest already active.")
                continue
            if qid in completed:
                print("Quest already completed.")
                continue
            quest = all_quests[qid]
            required = quest.get("required_level", 1)
            if c.get("level", 1) < required:
                print("Level too low for this quest.")
                continue
            active.append(qid)
            c["active_quests"] = active
            print(f"Accepted quest: {quest.get('title', qid)}")
        elif choice == "5":
            qid = input("Enter quest ID to abandon: ").strip()
            if qid not in active:
                print("Quest is not active.")
                continue
            active.remove(qid)
            c["active_quests"] = active
            print(f"Abandoned quest: {qid}")
        elif choice == "6":
            qid = input("Enter quest ID to complete (testing): ").strip()
            if qid not in active:
                print("Quest must be active to complete.")
                continue
            quest = all_quests.get(qid)
            if quest is None:
                print("Quest not found in data.")
                continue
            active.remove(qid)
            completed.append(qid)
            c["active_quests"] = active
            c["completed_quests"] = completed
            xp = quest.get("reward_xp", 0)
            gold = quest.get("reward_gold", 0)
            try:
                character_manager.gain_experience(c, xp)
            except CharacterDeadError:
                print("Cannot gain experience when dead.")
            try:
                character_manager.add_gold(c, gold)
            except ValueError:
                print("Error adding gold.")
            print(f"Completed quest: {quest.get('title', qid)}. Gained {xp} XP and {gold} gold.")
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

def explore():
    """Find and fight random enemies"""
# trigger a random emnemy to go through combat_system. 
# After reads battle result & update XP/gold
    global current_character
    if current_character is None:
        print("No character loaded.")
        return
    print("\n=== EXPLORE ===")
    level = current_character.get("level", 1)
    enemy = combat_system.get_random_enemy_for_level(level)
    print(f"You encounter a {enemy['name']}!")
    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        result = battle.start_battle()
    except CharacterDeadError:
        print("You are too injured to fight.")
        handle_character_death()
        return
    winner = result.get("winner")
    xp_gained = result.get("xp_gained", 0)
    gold_gained = result.get("gold_gained", 0)
    if winner == "player":
        print(f"You defeated the {enemy['name']}!")
        if xp_gained > 0:
            try:
                character_manager.gain_experience(current_character, xp_gained)
                print(f"Gained {xp_gained} XP.")
            except CharacterDeadError:
                print("Cannot gain experience when dead.")
        if gold_gained > 0:
            try:
                character_manager.add_gold(current_character, gold_gained)
                print(f"Gained {gold_gained} gold.")
            except ValueError:
                print("Error adding gold.")
    elif winner == "enemy":
        print(f"The {enemy['name']} defeated you...")
        handle_character_death()
    else:
        print("The battle ended without a clear winner.")

def shop():
    """Shop menu for buying/selling items"""
# uses item data to show items for sale, relies on inventory 
# system. handle purchases and errors, like insuffient funds or full inventory.
    global current_character, all_items
    if current_character is None:
        print("No character loaded.")
        return
    while True:
        print("\n=== SHOP ===")
        print(f"Your gold: {current_character.get('gold', 0)}")
        print("\nItems for sale:")
        for item_id, data in all_items.items():
            name = data.get("name", item_id)
            cost = data.get("cost", 0)
            item_type = data.get("type", "unknown")
            print(f"- {item_id}: {name} [{item_type}] - {cost} gold")
        print("\nShop Options:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        choice = input("Choose an option (1-3): ").strip()
        if choice == "3":
            break
        item_id = input("Enter item ID: ").strip()
        if item_id not in all_items:
            print("Unknown item ID.")
            continue
        data = all_items[item_id]
        try:
            if choice == "1":
                inventory_system.purchase_item(current_character, item_id, data)
                print(f"Purchased {data.get('name', item_id)}.")
            elif choice == "2":
                gold_gained = inventory_system.sell_item(current_character, item_id, data)
                print(f"Sold {data.get('name', item_id)} for {gold_gained} gold.")
            else:
                print("Invalid choice.")
        except InsufficientResourcesError as e:
            print(e)
        except InventoryFullError as e:
            print(e)
        except ItemNotFoundError as e:
            print(e)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
# file writing for character_maanager.save_character.
# handle basic file errors 
    global current_character
    
    if current_character is None:
        print("No character to save.")
        return
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except PermissionError:
        print("Permission error: could not save game.")
    except OSError as e:
        print(f"File error while saving: {e}")

def load_game_data():
    """Load all quest and item data from files"""
# assume all quests and items are ready to be loaded.
    global all_quests, all_items
    all_quests = game_data.load_quests()
    all_items = game_data.load_items()

def handle_character_death():
    """Handle character death"""
# gives player choice to revive using gold or quit, 
# using 'add_gold'
    global current_character, game_running
    print("\n=== YOU DIED ===")
    print("Your character has fallen in battle.")
    if current_character is None:
        game_running = False
        return
    while True:
        print("\n1. Revive for 50 gold")
        print("2. Quit to main menu")
        choice = input("Choose an option (1-2): ").strip()
        if choice == "1":
            try:
                character_manager.add_gold(current_character, -50)
            except ValueError:
                print("Not enough gold to revive.")
                continue
            revived = character_manager.revive_character(current_character)
            if revived:
                print("You have been revived!")
                return
            else:
                print("Could not revive character.")
        elif choice == "2":
            print("Returning to main menu...")
            game_running = False
            return
        else:
            print("Invalid choice.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
# displays welcome message, loads game data, & handle errors.
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

