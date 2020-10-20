import random

def list_shuffle(list):
    for i in range(len(list)):
        random_index = random.randint(i, len(list) - 1)
        list[random_index], list[i] = list[i], list[random_index]

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        
        if avg_friendships > num_users:
            print('WARNING: There must be more users than average friendships')

        friendships = []

        # Add users
        for user in range(1, num_users + 1):
            self.add_user(user)
            friendships.append(user)

        # Create friendships
        for user in self.users:
            list_shuffle(friendships)
            num_of_friends = random.randint(0, 4)
            friends_list = friendships[:num_of_friends]

            for friend in friends_list:
                if user < friend:
                    self.add_friendship(user, friend)

    def path_to_friend(self, user, friend):
        queue = []
        queue.append([user])

        while len(queue) > 0:
            path = queue.pop(0)
            current_user = path[-1]
            friends = self.friendships[current_user]

            if current_user == friend:
                return path

            for f in friends:
                path_copy = path.copy()
                path_copy.append(f)
                queue.append(path_copy)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        visited[user_id] = set()
        social_connections = []
        social_connections.append(user_id)

        # Generate a list of all possible social connections and add each one to visited
        while len(social_connections) > 0:
            current_user = social_connections.pop(0)
            friends = self.friendships[current_user]

            for f in friends:
                if f not in visited:
                    visited[f] = set()
                    social_connections.append(f)
        
        for friend in visited:
            visited[friend] = self.path_to_friend(user_id, friend)

        return visited

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)