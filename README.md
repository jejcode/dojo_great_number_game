# Dojo assignment: The great number game

What I learned:
Session variables struggle to update mutable objects like dictionaries and lists.
So if you want to append an item to a list stored in session, you need to add an additional command:
session['key_name'].append(new_list_item)
session.modified = True

To Do:
Sort the leaderboard so that fewest tries is on top