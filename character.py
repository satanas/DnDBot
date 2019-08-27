import sys
import requests

from roll import roll
from database import Database
from models.character import Character

CLOSE_COMBAT_DISTANCE = 5 # feet

SIZE_MODIFIER = {
    'Colossal': -8,
    'Small': 1,
    'Gargantuan': -4,
    'Tiny': 2,
    'Huge': -2,
    'Diminutive': 4,
    'Large': -1,
    'Fine': 8,
    'Medium': 0
}

def handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name

    if text.startswith('/import_char'):
        return import_char(text, db)
    elif text.startswith('/attack_roll'):
        return attack_roll(username, text, db)
    return import_character(url, chat_id, db)

def import_character(text, db):
    # 1. Get campaign for chat_id
    # 2. Get usernames for campaign
    # 3. Get character id from username
    # Goal: Get character_id from chat_id and username
    url = text.replace('/import_char', '').strip()
    character_data = requests.get(url).json()

    return db.save_character_info(character_id, character_data)

def get_weapons(chat_id, username, db):
    character = db.get_character(chat_id, username)

def initiative_roll(chat_id):
    pass

def ability_check(chat_id, username, ability):
    pass

def attack_roll(username, text, db):
    args = [a.strip() for a in text.replace('/attack_roll ', '').split(' ')]
    if len(args) < 3:
        return "Invalid syntax. Usage:\r\n/attack_roll <character> <weapon> <attack(melee|range)> [distance] [adv|disadv]"

    character_name = args[0]
    weapon_name = args[1]
    attack_type = args[2]
    distance = 5 if len(args) <= 3 else args[3]
    adv = False
    disadv = False
    if len(args) > 4 and args[4] == 'adv':
        adv = True
    elif len(args) > 4 and args[4] == 'disadv':
        disadv = True

    mods = 0
    txt_mod = ''
    adv_mod = ''
    prof = ''
    base_notation = '1d20'
    distance = int(distance)

    character = db.get_character(character_name)
    if character == None:
        return f'Character "{character_name}" not found'

    weapon = character.get_weapon(weapon_name)

    if attack_type in ["ranged", "r"] and distance > weapon.long_range:
        return f"You can attack a target beyond the range of your weapon ({weapon_name}, {weapon.long_range}ft)"

    prof = " + PRO(0)"
    if character.has_weapon_proficiency(weapon_name):
        mods += character.proficiency
        prof = f" + PRO({character.proficiency})"

    if attack_type in ["melee", "m"]:
        if weapon.has_finesse() and character.dex_mod > character.str_mod:
            txt_mod += f" + DEX({character.dex_mod})<finesse>"
            mods += character.dex_mod
        else:
            txt_mod += f" + STR({character.str_mod})"
            mods += character.str_mod
    elif attack_type in ["ranged", "r"]:
        if weapon.has_thrown() and character.str_mod > character.dex_mod:
            txt_mod += f" + STR({character.str_mod})<thrown>"
            mods += character.str_mod
        else:
            txt_mod += f" + DEX({character.dex_mod})"
            mods += character.dex_mod

    size_mod = SIZE_MODIFIER[character.size]
    txt_mod += f" + SIZE({size_mod})"
    mods += size_mod

    if attack_type in ["ranged", "r"] and \
            (distance <= CLOSE_COMBAT_DISTANCE or (distance >= weapon.range and distance <= weapon.long_range)):
        if not adv:
            adv_mod = " + DISADV"
    elif disadv == True:
        adv_mod = " + DISADV"
    elif adv == True:
        adv_mod = " + ADV"

    txt_formula = f"{base_notation}{prof}{txt_mod}{adv_mod}"
    if mods > 0:
        dice_notation = f"{base_notation}+{mods}"
    else:
        dice_notation = base_notation

    if adv_mod != "":
        dice_notation = f"{dice_notation},{dice_notation}"

    results = roll(dice_notation)
    dice_rolls = results[list(results.keys())[0]]

    return (f"@{username} attack roll for {character_name} with {weapon_name} ({attack_type}):"
            f"\r\nFormula: {txt_formula}"
            f"\r\n*{dice_notation}*: {dice_rolls}")


if __name__ == "__main__":
    db = Database()
    url = "https://dl.dropbox.com/s/awlpwcwi0eetdoq/ghamorz.json?dl=0"
    #import_character(url)
    #load_character('123456')
    print(attack_roll('satanas82', '/attack_roll Ghamorz Javelin ranged 10', db))
