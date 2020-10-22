from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()

# # You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# # map_file = "maps/test_loop.txt"
# # map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk (['n', 'n'])
traversal_path = []

# ** DFT TO FIND ROOMS **
maze_rooms = {}

reverse_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

starting_room = player.current_room.id

q = Queue()
q.enqueue(starting_room)

previous = [None, None] # [Room, Direction]

while len(maze_rooms) < len(room_graph):
    room = q.dequeue()
    exits = player.current_room.get_exits()
    unexplored_paths = []

    if room not in maze_rooms:
        maze_rooms[room] = {}

        for exit in exits:
            maze_rooms[room][exit] = '?'
        
        if previous[0] is not None:
            maze_rooms[room][previous[1]] = previous[0]
    else:
        for exit in exits:
            if exit not in maze_rooms[room].keys():
                maze_rooms[room][exit] = '?'
        
    for direction, connection in maze_rooms[room].items():
        if connection == '?':
            unexplored_paths.append(direction)
    
    if len(unexplored_paths) > 0:
        random_exit = random.choice(unexplored_paths)
        previous = [room, random_exit]

        player.travel(random_exit)
        traversal_path.append(random_exit)

        maze_rooms[room][random_exit] = player.current_room.id

        if player.current_room.id not in maze_rooms:
            maze_rooms[player.current_room.id] = {}
            reverse = reverse_direction[previous[1]]
            maze_rooms[player.current_room.id][reverse] = previous[0]

        q.enqueue(player.current_room.id)
    else:
        break

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

# # UNCOMMENT TO WALK AROUND
# # player.current_room.print_room_description(player)
# # while True:
# #     cmds = input("-> ").lower().split(" ")
# #     if cmds[0] in ["n", "s", "e", "w"]:
# #         player.travel(cmds[0], True)
# #     elif cmds[0] == "q":
# #         break
# #     else:
# #         print("I did not understand that command.")