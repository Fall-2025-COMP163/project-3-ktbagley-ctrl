"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

import character_manager


def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")
    quest = quest_data_dict[quest_id]

    level = character.get("level", 1)
    required_level = quest.get("required_level", 1)
    if level < required_level:
        raise InsufficientLevelError("Character level too low for this quest.")

    completed = character.get("completed_quests", [])
    active = character.get("active_quests", [])
    prereq = quest.get("prerequisite", "NONE")

    if prereq and str(prereq).upper() != "NONE" and prereq not in completed:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    if quest_id in completed:
        raise QuestAlreadyCompletedError("Quest has already been completed.")

    if quest_id in active:
        return False

    active.append(quest_id)
    character["active_quests"] = active
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")

    active = character.get("active_quests", [])
    if quest_id not in active:
        raise QuestNotActiveError("Quest is not active.")

    quest = quest_data_dict[quest_id]

    active.remove(quest_id)
    completed = character.get("completed_quests", [])
    if quest_id not in completed:
        completed.append(quest_id)

    character["active_quests"] = active
    character["completed_quests"] = completed

    xp = quest.get("reward_xp", 0)
    gold = quest.get("reward_gold", 0)

    if xp:
        character_manager.gain_experience(character, xp)
    if gold:
        character_manager.add_gold(character, gold)

    return {"xp": xp, "gold": gold}


def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    """
    active = character.get("active_quests", [])
    if quest_id not in active:
        raise QuestNotActiveError("Quest is not active.")
    active.remove(quest_id)
    character["active_quests"] = active
    return True


def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    """
    result = []
    for qid in character.get("active_quests", []):
        if qid in quest_data_dict:
            result.append(quest_data_dict[qid])
    return result


def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    """
    result = []
    for qid in character.get("completed_quests", []):
        if qid in quest_data_dict:
            result.append(quest_data_dict[qid])
    return result


def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    """
    available = []
    level = character.get("level", 1)
    completed = character.get("completed_quests", [])
    active = character.get("active_quests", [])

    for qid, quest in quest_data_dict.items():
        required_level = quest.get("required_level", 1)
        if level < required_level:
            continue

        prereq = quest.get("prerequisite", "NONE")
        if prereq and str(prereq).upper() != "NONE" and prereq not in completed:
            continue

        if qid in completed or qid in active:
            continue

        available.append(quest)

    return available


# ============================================================================
# QUEST TRACKING
# ============================================================================


def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    """
    return quest_id in character.get("completed_quests", [])


def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    """
    return quest_id in character.get("active_quests", [])


def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    """
    if quest_id not in quest_data_dict:
        return False

    quest = quest_data_dict[quest_id]
    level = character.get("level", 1)
    required_level = quest.get("required_level", 1)
    if level < required_level:
        return False

    completed = character.get("completed_quests", [])
    active = character.get("active_quests", [])
    prereq = quest.get("prerequisite", "NONE")

    if prereq and str(prereq).upper() != "NONE" and prereq not in completed:
        return False

    if quest_id in completed or quest_id in active:
        return False

    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    """
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")

    chain = []
    current_id = quest_id

    while True:
        if current_id not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {current_id} not found.")
        chain.append(current_id)
        quest = quest_data_dict[current_id]
        prereq = quest.get("prerequisite", "NONE")
        if prereq and str(prereq).upper() != "NONE":
            current_id = prereq
        else:
            break

    chain.reverse()
    return chain


# ============================================================================
# QUEST STATISTICS
# ============================================================================


def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
    completed_count = len(character.get("completed_quests", []))
    percentage = (completed_count / total_quests) * 100
    return float(percentage)


def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    """
    total_xp = 0
    total_gold = 0
    for qid in character.get("completed_quests", []):
        quest = quest_data_dict.get(qid)
        if quest is None:
            continue
        total_xp += quest.get("reward_xp", 0)
        total_gold += quest.get("reward_gold", 0)
    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    """
    quests = []
    for quest in quest_data_dict.values():
        required_level = quest.get("required_level", 1)
        if required_level >= min_level and required_level <= max_level:
            quests.append(quest)
    return quests


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================


def display_quest_info(quest_data):
    """
    Display formatted quest information
    """
    title = quest_data.get("title", quest_data.get("quest_id", "Unknown Quest"))
    description = quest_data.get("description", "No description")
    required_level = quest_data.get("required_level", 1)
    reward_xp = quest_data.get("reward_xp", 0)
    reward_gold = quest_data.get("reward_gold", 0)
    prereq = quest_data.get("prerequisite", "NONE")

    print(f"\n=== {title} ===")
    print(f"Description: {description}")
    print(f"Required Level: {required_level}")
    print(f"Reward XP: {reward_xp}")
    print(f"Reward Gold: {reward_gold}")
    print(f"Prerequisite: {prereq}")


def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    """
    if not quest_list:
        print("No quests found.")
        return

    for quest in quest_list:
        title = quest.get("title", quest.get("quest_id", "Unknown Quest"))
        required_level = quest.get("required_level", 1)
        reward_xp = quest.get("reward_xp", 0)
        reward_gold = quest.get("reward_gold", 0)
        print(f"- {title} (Level {required_level}) - Rewards: {reward_xp} XP, {reward_gold} gold")


def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    """
    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    totals = get_total_quest_rewards_earned(character, quest_data_dict)

    print("\n=== QUEST PROGRESS ===")
    print(f"Active quests: {active_count}")
    print(f"Completed quests: {completed_count}")
    print(f"Completion: {percentage:.1f}%")
    print(f"Total XP from quests: {totals['total_xp']}")
    print(f"Total gold from quests: {totals['total_gold']}")


# ============================================================================
# VALIDATION
# ============================================================================


def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    """
    for qid, quest in quest_data_dict.items():
        prereq = quest.get("prerequisite", "NONE")
        if prereq and str(prereq).upper() != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {qid} has invalid prerequisite {prereq}.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

