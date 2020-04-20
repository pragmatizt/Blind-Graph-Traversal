from room import Room
from player import Player
from world import World

import pdb
import random
from ast import literal_eval
from util import Queue, Stack

import random

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def traverse_world(player, traversal_path):
    ### Instantiate Everything ### 
    # Create dictionary with opposite directions
    reverse = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
    # Creates room with all exits
    mapped = {player.current_room.id: {}}
    # Adds '?'s to each of the exits
    mapped = add_exits_to_map(mapped, player.current_room)
    # Finds unvisited rooms.  Pass pick_direction with map and current room info
    move = pick_direction(mapped, player.current_room, None)
    # Check
    if move is False:
        print("There are no more exits to visit")

    # Change pointers prior to moving
    previous_room = player.current_room
    # Move
    player.travel(move)
    # Add that move (nsew) to traversal_path
    traversal_path.append(move)


    # We live in this while loop for duration of traversal
    while True:
        # If room not in map, add it
        if player.current_room.id not in mapped:
            # Update our dictionary
            mapped[player.current_room.id] = {}
            # Find exits - returns empty dict with exits and '?'s
            mapped = add_exits_to_map(mapped, player.current_room)

        # If current room has no value in previous room,
        if mapped[player.current_room.id][reverse[move]] == '?':
            # Current room becomes previous room
            mapped[player.current_room.id][reverse[move]] = previous_room.id
            # Add 'previous' room id as 'current room'
            mapped[previous_room.id][move] = player.current_room.id

        # If there is still an unexplored exits, return list of exits with '?'s
        move = pick_direction(mapped, player.current_room, None)
        # If no more exits
        if move is False:
            # map path to closest unexplored exit
            return_path = bfs_pathfinding(mapped,player.current_room.id)
            # if there are no unexplored rooms, return
            if return_path is None:
                """If None then I have visited all my rooms"""
                break
            # Walk path while adding to traversal path, remove from return_path
            while return_path:
                # bfs_pathfinding has a queue in its definition
                move = return_path.pop(0)
                # move function
                player.travel(move)
                # add to traversal_path
                traversal_path.append(move)
        else:
            # Change pointer
            previous_room = player.current_room
            # Move
            player.travel(move)
            # Append to traversal_path
            traversal_path.append(move)
    return mapped


def add_exits_to_map(mapped,current_room):
    # Extract possible exits in current room
    # returns array of exits
    for exits in current_room.get_exits():
        # For each element in array, create '?'
        mapped[current_room.id][exits] = '?'
    return mapped


def pick_direction(mapped, current_room=None, id_room=None):
    """
    Sends current room info
    Input: player.current_room
    Output: exits of that room
    
    note: id_room = current_room.id
    """
    # Send current room info
    if current_room is not None:
        exits = current_room.get_exits()
        random.shuffle(exits)
        for ex in exits:
            if mapped[current_room.id][ex]=='?':
                return ex
    # Sends id_room info
    if id_room is not None:
        for ex in id_room.keys():
            # print("ID*****************",id_room, id_room.get(ex))
            visited = id_room.get(ex)
            if visited == '?':
                return ex
    
    return False


def pathfinding(mapped, path):
    """
    Checks for exits by going back one room and finding 
    a direction unexplored.  
    Returns a new path to go to that direction
    """
    # Goes back one room to find a room unexplored and
    # returns a new path to go to that direction
    new_path = []
    # From 1 to length of path
    for i in range(1, len(path)):
        # Check each room less one (backtracking by one)
        for room_direction, room_id in mapped[path[i-1]].items():
            #print("CHECK",room_direction, room_id)
            if room_id == path[i]:
                new_path.append(room_direction)
                break
    return new_path


def bfs_pathfinding(mapped,current_room):
    # Create an empty queue
    queue = Queue()
    # Add a path between room_id and queue
    queue.enqueue([current_room])
    # Create an empty set to store visited rooms
    visited = set()
    # As long as there's something in queue
    while queue.size() > 0:
        # Dequeue first in the path
        path = queue.dequeue()
        # Grab last room from path, and make current
        # room most recent added
        current_room = path[-1]
        # print('map values', mapped[current_room.id].values())

        if pick_direction(mapped,None,mapped[current_room]):
            # print('current_room.id', current_room.id, current_room_id)
            new_path = pathfinding(mapped, path)
            return new_path
        # If current room has not been visited
        if current_room not in visited:
            # Mark as visited
            visited.add(current_room)
            # Add a path to all unvisited rooms to back of queue
            # print(mapped[current_room].values())
            # breakpoint()
            for next_room in mapped[current_room].values():
                if next_room not in visited:
                    # queue.append(path + [next_room])
                    new_path = path + [next_room]
                    queue.enqueue(new_path)

    return None

# TRAVERSAL TEST
traverse_world(player, traversal_path)
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
