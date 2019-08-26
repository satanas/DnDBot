import math

from models.armor import Armor
from models.weapon import Weapon

class Character:
    def __init__(self, json_data, race_data):
        self.id = json_data['character']['id']
        self.beyond_url = json_data['character']['readonlyUrl']
        self.name = json_data['character']['name']
        self.race = json_data['character']['race']['fullName']
        self.str = int(json_data['character']['stats'][0]['value']) + int(race_data['ability_bonuses'][0])
        self.dex = int(json_data['character']['stats'][1]['value']) + int(race_data['ability_bonuses'][1])
        self.con = int(json_data['character']['stats'][2]['value']) + int(race_data['ability_bonuses'][2])
        self.int = int(json_data['character']['stats'][3]['value']) + int(race_data['ability_bonuses'][3])
        self.wis = int(json_data['character']['stats'][4]['value']) + int(race_data['ability_bonuses'][4])
        self.cha = int(json_data['character']['stats'][5]['value']) + int(race_data['ability_bonuses'][5])
        self.str_mod = math.floor((self.str - 10) / 2)
        self.dex_mod = math.floor((self.dex - 10) / 2)
        self.con_mod = math.floor((self.con - 10) / 2)
        self.int_mod = math.floor((self.int - 10) / 2)
        self.wis_mod = math.floor((self.wis - 10) / 2)
        self.cha_mod = math.floor((self.cha - 10) / 2)
        self.walking_speed = int(json_data['character']['race']['weightSpeeds']['normal']['walk'])
        self.max_hit_points = int(json_data['character']['baseHitPoints']) + self.con_mod
        self.current_hit_points = self.max_hit_points - int(json_data['character']['removedHitPoints'])
        self.initiative = self.dex_mod
        self.weapons = [Weapon(x) for x in json_data['character']['inventory'] if x['definition']['filterType'] == "Weapon"]
        self.armor = [Armor(x) for x in json_data['character']['inventory'] if x['definition']['filterType'] == "Armor"]
        self.proficiencies = [x['friendlySubtypeName'] for x in json_data['character']['modifiers']['class'] if x['type'] == 'proficiency']
        # FIXME: Put the real value here
        self.proficiency = 2


    def has_weapon_proficiency(self, weapon):
        return True if weapon in self.proficiencies else False

    def get_weapon(self, weapon_name):
        result = [w for w in self.weapons if w.name == weapon_name]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def __str__(self):
        return (f"Character name={self.name}, race={self.race}, str={self.str}({self.str_mod}), dex={self.dex}({self.dex_mod}), "
                f"con={self.con}({self.con_mod}), int={self.int}({self.int_mod}), wis={self.wis}({self.wis_mod}), "
                f"cha={self.cha}({self.cha_mod}), walking_speed={self.walking_speed}, max_hit_points={self.max_hit_points}, "
                f"current_hit_points={self.current_hit_points}, initiative={self.initiative}")

