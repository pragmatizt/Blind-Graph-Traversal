##### SETUP #####
# init set up
# get current room
# - 0
# get the exits of the current room
# - [n, s, w, e]

# add to visited
# should look like this
# - {0: {n: ?, s: ?, w: ?, e: ?}}

# initialize Stack
# Options:
# 1. push -> 0 <---   this looks like this will not work for us
# 2. (direction = none, previous_room = none) <---- so we will go with this one

# start traversal in DFT MODE
# room_info = pop -> (direction, previous_room)
# current_room = current_room.id
# previous_room = room_info[1]
# direction = 
# get the current room exits from our visited

# check if current room is in visted
# if not, then add to visited
# add to visited
# should look like this:
# - {current room: {exits....: ?}}


# this should fail on the first iteration because there is no previous room
# if previous room is not None:
# This is where we update our previous room
# visited[previous_room][direction] = current_room

# this should fail on first iteration becaues there is no direction
# Update current room exits if we have a direction
# if direction is not None:
# visited[current_room][reverseDirection] = previous_room  

# loop over unvisited neighbors / or maybe all neighbors?
#   move in that direction
#   update traversal_path -> direction
#   update the stack -> (direction, current_room)

# CONDITION: if there are no exits that are unvisited
#               enter into bft mode this will probably be a help function


# bft (might not be bft? might be search) will traverse over our visited graph (this is like the visited dictionary - building a new graph)
    # the destination is a room with question marks
    # building a path to traverse after finding the destination

    

