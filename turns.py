from database import Database

def handler(bot, update):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    if text.startswith('/set_turns'):
        return set_turns(chat_id, text, db)
    elif text.startswith('/turn'):
        return get_current_turn(chat_id, db)
    elif text.startswith('/next_turn'):
        return update_turn(chat_id, db, True)
    elif text.startswith('/prev_turn'):
        return update_turn(chat_id, db, False)

def get_turns_info(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    turns = campaign.get('turns', None)
    turn_index = int(campaign.get('turn_index', '0'))
    return (turns, turn_index, campaign_id)

# TODO: Test with chat_id, '/set_turns logan, bruce, tony
def set_turns(chat_id, text, db):
    command = text.replace('/set_turns', '').strip()
    turns = [u.strip() for u in command.split(',')]
    campaign_id, campaign = db.get_campaign(chat_id)
    db.set_turns(campaign_id, turns)
    return print_turns_order(turns)

def get_current_turn(chat_id, db):
    turns, turn_index, campaign_id = get_turns_info(chat_id, db)
    return print_turn(turns, turn_index % len(turns))

def update_turn(chat_id, db, is_next=True):
    diff = 1 if is_next else -1
    turns, turn_index, campaign_id = get_turns_info(chat_id, db)
    turn_index = int(turn_index) + diff
    db.set_turn_index(campaign_id, turn_index)
    return print_turn(turns, turn_index % len(turns))

def print_turns_order(turns):
    response = "Turns order is:\n"
    for idx, user in enumerate(turns):
        response += f"{idx}. {user}\n"
    return response.rstrip("\n")

def print_turn(turns, current_turn):
    return f"Next in line is {turns[current_turn]}"
