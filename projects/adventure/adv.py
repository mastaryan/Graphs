from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

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

# Fill this out with directions to walk (['n', 'n'])
traversal_path = []

# Track explored rooms
maze_rooms = {}

reverse_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

starting_room = player.current_room.id

# For BFS of all rooms
q = Queue()
q.enqueue(starting_room)

# Track current path to reverse direction when a dead end is encountered
current_path = []

# While there are unexplored rooms
while len(maze_rooms) < len(room_graph):
    room = q.dequeue()
    exits = player.current_room.get_exits()
    unexplored_exits = []

    # If new room, add all exits to maze_rooms graph
    if room not in maze_rooms:
        maze_rooms[room] = {}

        for exit in exits:
            maze_rooms[room][exit] = '?'
        
    # Find each unexplored exit
    for direction, connection in maze_rooms[room].items():
        if connection == '?':
            unexplored_exits.append(direction)
    
    # If there are unexplored exits, randomly choose a direction to move and continue exploring
    if len(unexplored_exits) > 0:
        # previous_room = player.current_room.id

        random_exit = random.choice(unexplored_exits)
        reverse = reverse_direction[random_exit]

        player.travel(random_exit)
        traversal_path.append(random_exit)
        current_path.append(random_exit)

        current = player.current_room.id

        # If new room not explored, add all exits to maze_rooms graph
        if current not in maze_rooms:
            maze_rooms[current] = {}
            exits = player.current_room.get_exits()

            for exit in exits:
                maze_rooms[current][exit] = '?'

        # Connect the rooms together
        maze_rooms[room][random_exit] = current
        maze_rooms[current][reverse] = room

        # Add current room to queue
        q.enqueue(player.current_room.id)
    
    # If all exits have been explored, reverse the path until an unexplored exit appears
    else:
        if len(current_path) > 0:
            direction = current_path.pop()
            reverse = reverse_direction[direction]
            player.travel(reverse)
            traversal_path.append(reverse)

        # Add current room to queue
        q.enqueue(player.current_room.id)

# TRAVERSAL TEST
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

# UNCOMMENT TO WALK AROUND
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")