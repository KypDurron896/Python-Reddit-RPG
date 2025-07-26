# imports praw api 
import praw
import random
#player inventory setup
class Item:
    def __init__(self, name, slot_type, description=""):
        # slot_type can be "weapon", "armor", or "special"
        self.name = name
        self.slot_type = slot_type
        self.description = description

class PlayerInventory:
    def __init__(self):
        # starts slots with as empty
        self.slots = {
            "weapon": None,
            "armor": None,
            "special": None,
        }

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

# Example usage:
sword = Item("Sword", "weapon", "A basic sword.")
helmet = Item("Helmet", "armor", "Protects your head.")
amulet = Item("Amulet of Strength", "special", "Increases strength.")
# Reddit app credentials
client_id = 'GOg6wpnbB4QkTBeiIXYcSQ'
client_secret = 'KTnvLRCZ28NzkYwn0YzZBmapZEBmjg'
user_agent = 'pythongame by Consistent_Pirate168'

# Initialize Reddit
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Starting location subreddits
subreddit_list = [
    'Python', 'programming', 'gaming', 'pcmasterrace', 'videogames', 'LinusTechTips',
    'StarWars', 'Steam', 'wow', 'technology', 'skyrim', 'DIY',
    'dune', 'lordoftherings', 'Art', 'wholesomememes'
]

# Travel locations
otherreddit_list = [
    '0ad', '2007scape', '3dprinting', 'boardgames', 'books', 'DnD',
    'doctorwho', 'Fallout', 'GlobalOffensive', 'hardware', 'lego', 'linux',
    'Marvel', 'MetalForTheMasses', 'Art', 'wholesomememes'
]

def enemy_attack_turn(enemy_attack, bossfight, user_health):
    try:
        boss_weapon = sword
        hityes = random.randint(1, 2)
        if hityes == 1:
            print(f'u/{bossfight} swings his {boss_weapon.name} and misses!')
        else:
            damage = enemy_attack
            user_health -= damage
            print(f'u/{bossfight} lands a hit on you with his {boss_weapon.name} and does {damage} damage!')
        return user_health
    except Exception as e:
        print(f"Error during enemy attack: {e}")
        return user_health

def user_attack_turn(user_attack, username, bossfight, enemy_health):
    try:
        user_weapon = sword
        hityes = random.randint(1, 2)
        if hityes == 1:
            print(f'u/{username} swings his {user_weapon.name} at u/{bossfight} and misses!')
        else:
            damage = user_attack
            enemy_health -= damage
            print(f'u/{username} swings his {user_weapon.name} at u/{bossfight} and deals {damage} damage!')
        return enemy_health
    except Exception as e:
        print(f"Error during user attack: {e}")
        return enemy_health

    
# Ask for Reddit username
print('+-----------------------------+')
print('|     Realms of Reddit        |')
print('|                             |')
print('+-----------------------------+')
username = input(':reddit username: u/')

# Get and show karma stats
try:
    user = reddit.redditor(username)
    inventory = PlayerInventory()
    inventory.equip_item(sword)
    inventory.equip_item(helmet)
    inventory.equip_item(amulet)
    print('+---------------------------------------+')
    print(f' Username:       {user.name}')
    print(f' Post Karma:     {user.link_karma}')
    print(f' Comment Karma:  {user.comment_karma}')
    print('+---------------------------------------+')
    user_health = user.comment_karma
    user_attack = user.link_karma
except Exception as e:
    print(f"Error: {e}")

# Game state
current_sub = reddit.subreddit(random.choice(subreddit_list))
bots = random.randint(1, 50)
karma_bosses = []
destinations = []
# Function to show subreddit info and handle commands
def sub_info():
    global current_sub
    global bots
    global karma_bosses
    global destinations
    # Set up bosses from recent active users
    karma_bosses.clear()
    try:
        for submission in current_sub.new(limit=10):
            if submission.author and submission.author.name not in karma_bosses:
                karma_bosses.append(submission.author.name)
            if len(karma_bosses) >= 5:
                break
    except:
        print("Couldn't load basement dwellers.")
#displays info
    print(f'\n+--- r/{current_sub.display_name} ---+')
    print(f'There are {len(karma_bosses)} basement dwellers lurking in r/{current_sub.display_name}')
    print(f'There are {bots} comment farms here...')

    # Choose destinations and display them
    destinations = random.sample(otherreddit_list, 5)
    print('Travel is available to these subreddits:')
    for r in destinations:
        print(f' - r/{r}')
    print('+------------------------------+')
    print('Check commands.txt to view all the available commands.')

    # Handle command input
sub_info()
while True:
    command = input(':> ').strip().lower()

    if command == 'travel':
        print("\nWhich subreddit do you want to travel to?")
        for i, r in enumerate(destinations, 1):
            print(f"{i}. r/{r}")
        try:
            choice = int(input("Choose 1–5: "))
            if 1 <= choice <= 5:
                new_sub_name = destinations[choice - 1]
                current_sub = reddit.subreddit(new_sub_name)
                bots = random.randint(1, 50)
                destinations = random.sample(otherreddit_list, 5)  # Refresh options
                print(f'\nYou travel to r/{current_sub.display_name}...')
                sub_info()
            else:
                print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

    elif command == 'inventory':
        inventory.show_equipment()

    elif command == 'quit':
        print(f"Your spirit fades out of r/{current_sub.display_name}... ")
        break
#shows bosses
    elif command == 'show boss':
        print("\nBasement dwellers in this subreddit:")
        for boss in karma_bosses:
            try:
                redditor = reddit.redditor(boss)
                total_karma = redditor.link_karma + redditor.comment_karma
                print(f" - u/{boss} | Total Karma: {total_karma}")
            except Exception:
                print(f" - u/{boss} | Karma: [unavailable]")
        input("\nPress Enter to continue...")
        sub_info()

    elif command == 'fight boss':
        print("\nWhich basement dweller do you want to engage in mortal combat with?")
        for i, r in enumerate(karma_bosses, 1):
            print(f"{i}. u/{r}")

        try:
            choice = int(input("Choose 1–5: "))
            if 1 <= choice <= 5:
                bossfight = karma_bosses[choice - 1]

                # Equip items
                inventory = PlayerInventory()
                inventory.equip_item(sword)
                inventory.equip_item(helmet)
                inventory.equip_item(amulet)
                enemy = reddit.redditor(bossfight)
                enemy_health = enemy.comment_karma
                enemy_attack = enemy.link_karma
                print(f'\nYou ready yourself to attack u/{bossfight}...')

                # Assign user karma values to stats
                user_health = user.comment_karma
                user_attack = user.link_karma

                # Determine who attacks first
                surprise = random.randint(1, 2)
                if surprise == 1:
                    print(f'You have surprised u/{bossfight}!')
                    enemy_health = user_attack_turn(user_attack, username, bossfight, enemy_health)
                else:
                    print(f'You have been ambushed by u/{bossfight}!')
                    user_health = enemy_attack_turn(enemy_attack, bossfight, user_health)

# Now continue with the fight loop
                while user_health > 0 and enemy_health > 0:
                    enemy_health = user_attack_turn(user_attack, username, bossfight, enemy_health)
                    if enemy_health <= 0:
                        print(f"You defeated u/{bossfight}!")
                        break
        
                    user_health = enemy_attack_turn(enemy_attack, bossfight, user_health)
                    if user_health <= 0:
                        print(f"You were defeated by u/{bossfight}...")
                        break

            else:
                print("Invalid choice. Choose a number from 1 to 5.")
        except ValueError:
            print("Please enter a valid number.")

    else:
        print("Unknown command. Check the commands file to view commands.")
