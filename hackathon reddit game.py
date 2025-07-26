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

inventory = PlayerInventory()
inventory.equip_item(sword)
inventory.equip_item(helmet)
inventory.equip_item(amulet)

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

# Ask for Reddit username
print('+-----------------------------+')
print('|     Realms of Reddit        |')
print('|                             |')
print('+-----------------------------+')
username = input(':reddit username: u/')

# Get and show karma stats
try:
    user = reddit.redditor(username)
    print('+---------------------------------------+')
    print(f' Username:       {user.name}')
    print(f' Post Karma:     {user.link_karma}')
    print(f' Comment Karma:  {user.comment_karma}')
    print('+---------------------------------------+')
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
    print(f'There are {len(karma_bosses)} basement dwellers in r/{current_sub.display_name}')
    print(f'There are {bots} bots lurking here...')

    # Choose destinations and display them
    destinations = random.sample(otherreddit_list, 5)
    print('Travel is available to these subreddits:')
    for r in destinations:
        print(f' - r/{r}')
    print('+------------------------------+')
    print('Check readme.txt to view all the available commands.')

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
        print(f"Your spirit fades out of r/{current_sub.display_name} ")
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
    else:
        print("Unknown command. Check the Readme file to view commands.")



