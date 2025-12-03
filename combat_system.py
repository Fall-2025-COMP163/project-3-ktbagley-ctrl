"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Kayla Bagley

AI Usage: Used AI to help me import is_character_dead to make sure not to re-implement anything, while making sure everything from character manager is confident in the user's character state. 

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================
#the main battle system, handlinig classes, special abilitees, & more.

# doesnt let a dead character start a battle
from character_manager import is_character_dead

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
# based on enemy type, creates an dictionary with base stats.
# if user passes unknown type, raises error.
    enemy_type = enemy_type.lower()
    base_stats = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }
    if enemy_type not in base_stats:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    base = base_stats[enemy_type]
    enemy = {
        "name": enemy_type.capitalize(),
        "type": enemy_type,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"]
    }
    return enemy

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
# picks appropriate enemy based on character level
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
# holding current character & enemy
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""

        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_count = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy'|None, 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
# COMBAT LOOP, between player and enemy. if player wins, 
# then rewards calculated with dictionary (gold & XP)
        if is_character_dead(self.character):
            raise CharacterDeadError("Character is already dead and cannot fight.")
        xp_gained = 0
        gold_gained = 0
        while self.combat_active:
            winner = self.check_battle_end()
            if winner is not None:
                break
            self.turn_count += 1
            self.player_turn()
            winner = self.check_battle_end()
            if not self.combat_active or winner is not None:
                break
            self.enemy_turn()
        winner = self.check_battle_end()
        if winner == "player":
            rewards = get_victory_rewards(self.enemy)
            xp_gained = rewards["xp"]
            gold_gained = rewards["gold"]
        self.combat_active = False
        return {"winner": winner, "xp_gained": xp_gained, "gold_gained": gold_gained}
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
# shows player's options each turn, branches off with choices.
# Error can also be raised if combat not active.
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        display_combat_stats(self.character, self.enemy)
        print("\nYour turn:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        choice = input("Choose an action (1-3): ").strip()
        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage.")
        elif choice == "2":
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped from battle!")
            else:
                display_battle_log("You failed to escape!")
        else:
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"Invalid choice. You perform a basic attack for {damage} damage.")
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
# enemy ALWAYS attacks player each turn. damage logic and logs everything.
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        if self.enemy["health"] <= 0:
            return
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage.")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
# makes sure damage is calculated correctly based on strength stats.
        base = attacker.get("strength", 0) - (defender.get("strength", 0) // 4)
        if base < 1:
            base = 1
        return base
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
# updates health, NEVER GO NEG
        current = target.get("health", 0)
        new_health = current - damage
        if new_health < 0:
            new_health = 0
        target["health"] = new_health
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
# if either player or enemy won
        if self.enemy.get("health", 0) <= 0:
            self.combat_active = False
            return "player"
        if self.character.get("health", 0) <= 0:
            self.combat_active = False
            return "enemy"
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
# 50/50 chance to escape battle
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
# based on character class, uses special ability.
    char_class = character.get("class", "").lower()
    if char_class == "warrior":
        damage = warrior_power_strike(character, enemy)
        return f"You use Power Strike and deal {damage} damage!"
    elif char_class == "mage":
        damage = mage_fireball(character, enemy)
        return f"You cast Fireball and deal {damage} damage!"
    elif char_class == "rogue":
        damage, crit = rogue_critical_strike(character, enemy)
        if crit:
            return f"Critical Strike! You deal {damage} damage!"
        return f"You strike for {damage} damage."
    elif char_class == "cleric":
        healed = cleric_heal(character)
        return f"You cast a healing spell and restore {healed} health."
    else:
        raise AbilityOnCooldownError("Special ability not available for this class.")

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character.get("strength", 0) * 2
    new_health = enemy.get("health", 0) - damage
    if new_health < 0:
        new_health = 0
    enemy["health"] = new_health
    return damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character.get("magic", 0) * 2
    new_health = enemy.get("health", 0) - damage
    if new_health < 0:
        new_health = 0
    enemy["health"] = new_health
    return damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    strength = character.get("strength", 0)
    if random.random() < 0.5:
        damage = strength * 3
        crit = True
    else:
        damage = strength
        crit = False
    new_health = enemy.get("health", 0) - damage
    if new_health < 0:
        new_health = 0
    enemy["health"] = new_health
    return damage, crit

def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30
    max_health = character.get("max_health", 0)
    current_health = character.get("health", 0)
    missing = max_health - current_health
    if missing <= 0:
        return 0
    actual = heal_amount if heal_amount <= missing else missing
    character["health"] = current_health + actual
    return actual

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """

    return character.get("health", 0) > 0

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

