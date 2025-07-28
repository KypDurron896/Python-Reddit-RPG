# imports praw api 
import praw
import random

# --- Classes ---
class Item:
    def __init__(self, name, slot_type, description=""):
        self.name = name
        self.slot_type = slot_type
        self.description = description

class PlayerInventory:
    def __init__(self):
        self.slots = {"weapon": None, "armor": None, "special": None}

    def equip_item(self, item):
        if item.slot_type not in self.slots:
            print(f"Cannot equip item: invalid slot type '{item.slot_type}'.")
            return
        current = self.slots[item.slot_type]
        if current:
            print(f"Unequipped {current.name} from {item.slot_type} slot.")
        self.slots[item.slot_type] = item
        print(f"Equipped {item.name} to {item.slot_type} slot.")

    def unequip_item(self, slot_type):
        if slot_type in self.slots and self.slots[slot_type]:
            print(f"Unequipped {self.slots[slot_type].name} from {slot_type} slot.")
            self.slots[slot_type] = None
        else:
            print(f"No item to unequip in {slot_type} slot.")

    def show_equipment(self):
        print("Player Equipment:")
        for slot, item in self.slots.items():
            if item:
                print(f" - {slot.capitalize()}: {item.name} ({item.description})")
            else:
                print(f" - {slot.capitalize()}: Empty")

# --- Items ---
Lukes_Lightsaber = Item("Lukes Lightsaber", "weapon", "Luke Skywalkers lightsaber")
Anduril = Item("Anduril", "weapon", "Aragorns sword.")
Mjolnir = Item("Mjolnir", "weapon", "Thors magical hammer.")
Indys_Whip = Item("Indys Whip", "weapon", "Indiana Jones bullwhip.")
Captain_Americas_Shield = Item("Captain Americas Shield", "armor", "Caps vibranium shield.")
Holy_Hand_Grenade_of_Antioch = Item("Holy Hand Grenade of Antioch", "special", "O Lord, bless this thy hand grenade.")
Phaser = Item("Phaser", "weapon", "A standard Federation hand phaser.")
Chainsaw = Item("Chainsaw", "weapon", "VROOM VROOOOOOOOOM!")
Super_Shotgun = Item("Super Shotgun", "weapon", "Doomguy's super shotgun.")
Bolter = Item("Bolter", "weapon", "Purge the xenos!")
Excalibur = Item("Excalibur", "weapon", "The legendary sword of King Arthur")
sword = Item("Sword", "weapon", "A basic sword.")
helmet = Item("Helmet", "armor", "Protects your head.")
amulet = Item("Amulet of Strength", "special", "Increases strength.")

# --- Reddit Credentials ---
reddit = praw.Reddit(
    client_id='GOg6wpnbB4QkTBeiIXYcSQ',
    client_secret='KTnvLRCZ28NzkYwn0YzZBmapZEBmjg',
    user_agent='pythongame by Consistent_Pirate168'
)

# --- Setup ---
subreddit_list = ['Python', 'programming', 'gaming', 'pcmasterrace', 'videogames', 'LinusTechTips', 'StarWars', 'Steam', 'wow', 'technology', 'skyrim', 'DIY', 'dune', 'lordoftherings', 'Art', 'wholesomememes']
otherreddit_list = ['0ad', '2007scape', '3dprinting', 'boardgames', 'books', 'DnD', 'doctorwho', 'Fallout', 'GlobalOffensive', 'hardware', 'lego', 'linux', 'Marvel', 'MetalForTheMasses', 'Art', 'wholesomememes']
loot_list = ['Lukes Lightsaber', 'Anduril', 'Mjolnir', 'Captain Americas Shield', 'Indys Whip', 'Holy Hand Grenade of Antioch', 'Phaser', 'Chainsaw', 'Super Shotgun', 'Bolter', 'Excalibur']

# --- Combat Functions ---
def enemy_attack_turn(enemy_attack, bossfight, user_health):
    hityes = random.randint(1, 2)
    if hityes == 1:
        print(f'u/{bossfight} swings and misses!')
    else:
        damage = enemy_attack
        user_health -= damage
        print(f'u/{bossfight} lands a hit and deals {damage} damage!')
    return user_health

def user_attack_turn(user_attack, username, bossfight, enemy_health):
    hityes = random.randint(1, 2)
    if hityes == 1:
        print(f'u/{username} attacks u/{bossfight} and misses!')
    else:
        damage = user_attack
        enemy_health -= damage
        print(f'u/{username} hits u/{bossfight} for {damage} damage!')
    return enemy_health

# --- Game Start ---
print('+-----------------------------+')
print('|     Realms of Reddit        |')
print('|                             |')
print('+-----------------------------+')
username = input(':reddit username: u/')

try:
    user = reddit.redditor(username)
    inventory = PlayerInventory()
    inventory.equip_item(sword)
    inventory.equip_item(helmet)
    inventory.equip_item(amulet)
    print(f"\n+---------------------------------------+")
    print(f' Username:       {user.name}')
    print(f' Post Karma:     {user.link_karma}')
    print(f' Comment Karma:  {user.comment_karma}')
    print(f"+---------------------------------------+")
    user_health = user.comment_karma
    user_attack = user.link_karma
except Exception as e:
    print(f"Error: {e}")
    exit()

# --- Track Upvotes ---
total_upvotes = sum(comment.score for comment in reddit.redditor(username).comments.new(limit=50))

# --- Initial Subreddit ---
current_sub = reddit.subreddit(random.choice(subreddit_list))
bots = random.randint(1, 50)
karma_bosses = []
destinations = []

def sub_info():
    global current_sub, bots, karma_bosses, destinations
    karma_bosses.clear()
    try:
        for submission in current_sub.new(limit=10):
            if submission.author and submission.author.name not in karma_bosses:
                karma_bosses.append(submission.author.name)
            if len(karma_bosses) >= 5:
                break
    except:
        print("Couldn't load basement dwellers.")

    print(f'\n+--- r/{current_sub.display_name} ---+')
    print(f'There are {len(karma_bosses)} basement dwellers lurking.')
    print(f'{bots} comment farms infest this subreddit...')
    destinations = random.sample(otherreddit_list, 5)
    print('Travel available to:')
    for r in destinations:
        print(f' - r/{r}')
    print('+------------------------------+')
    print('Type commands like: inventory, travel, show boss, fight boss, farm, quit')

# --- Game Loop ---
sub_info()
while True:
    command = input(':> ').strip().lower()

    if command == 'travel':
        print("\nChoose a destination:")
        for i, r in enumerate(destinations, 1):
            print(f"{i}. r/{r}")
        try:
            choice = int(input("Choose 1–5: "))
            if 1 <= choice <= 5:
                current_sub = reddit.subreddit(destinations[choice - 1])
                bots = random.randint(1, 50)
                destinations = random.sample(otherreddit_list, 5)
                print(f'\nYou travel to r/{current_sub.display_name}...')
                sub_info()
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    elif command == 'inventory':
        inventory.show_equipment()

    elif command == 'farm':
        rand_farm = random.randint(1, 300) + total_upvotes // 5
        if rand_farm >= 150:
            loot = random.choice(loot_list)
            print(f'You have discovered {loot}!')
        else:
            print("You didn't find anything this time.")

    elif command == 'show boss':
        print("\nBasement dwellers in this subreddit:")
        for boss in karma_bosses:
            try:
                redditor = reddit.redditor(boss)
                total_karma = redditor.link_karma + redditor.comment_karma
                print(f" - u/{boss} | Total Karma: {total_karma}")
            except:
                print(f" - u/{boss} | Karma: [unavailable]")
        input("\nPress Enter to continue...")
        sub_info()

    elif command == 'fight boss':
        print("\nWhich basement dweller do you want to engage in combat?")
        for i, r in enumerate(karma_bosses, 1):
            print(f"{i}. u/{r}")

        try:
            choice = int(input("Choose 1–5: "))
            if 1 <= choice <= 5:
                bossfight = karma_bosses[choice - 1]
                enemy = reddit.redditor(bossfight)
                enemy_health = enemy.comment_karma
                enemy_attack = enemy.link_karma

                print(f'\nYou ready yourself to attack u/{bossfight}...')

                surprise = random.randint(1, 2)
                turn = "user" if surprise == 1 else "enemy"
                print("You have surprised the enemy!" if turn == "user" else f"You have been ambushed by u/{bossfight}!")

                while user_health > 0 and enemy_health > 0:
                    if turn == "user":
                        enemy_health = user_attack_turn(user_attack, username, bossfight, enemy_health)
                        turn = "enemy"
                    else:
                        user_health = enemy_attack_turn(enemy_attack, bossfight, user_health)
                        turn = "user"

                if user_health <= 0:
                    print(f"You were defeated by u/{bossfight}...")
                elif enemy_health <= 0:
                    print(f"You defeated u/{bossfight}!")
                    reward = random.choice(loot_list)
                    print(f"You looted: {reward}!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    elif command == 'quit':
        print(f"Your spirit fades out of r/{current_sub.display_name}... ")
        break

    else:
        print("Unknown command. Check the command list.")
