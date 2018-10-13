import sys
from random import shuffle
"""
	N - the total number of nodes
	K - number of border nodes
	k - number of neighRooms of K border nodes
	p - number of neighRooms of remaining N-K nodes

	Output form: (id: wall, hole, monster, gold, wind, smell all_connected_rooms)
"""

"""
	1) When a hole is in the room the wind
		in the same room has nominal value 1.
	2) When a monster is in the room the smell in the same room
has nominal value 1.
	3) When a wall is in the room, you cannot go anywhere but back but you can still
smell the smell and feel the wind spread from other rooms
"""

"""
	4)  if delta is 0, both wind and smell do not spread outside of the room where it is generated.
	If delta = 1 both will go to the first neighbor, with delta = 2 they will spread to two neighbors, etc.

	5) omega specifies the decay rate of smell and of wind : it indicates rate indicates how the values of
	smell/wind change when changing room. If decay rate is 1 and the spread is 2, all rooms have
	the same smell.
	If the decay is 0.5, in the room where the monster is the smell will have value 1,
	the first neighbor have smell 0.5, the next rooms have smell 0.25.

	6) For any interaction of multiple winds or smells, use max function to determine the value of sell
or wind in the room.
"""
class Room:
    id = 1
    potentialConns = 0
    wind = 0
    hole = 0
    monster = 0
    gold = 0
    smell = 0
    wall = 0
    visited = False

    def __init__(self, potentialConns):
        self.id = Room.id
        Room.id += 1
        self.potentialConns = potentialConns
        self.neighRooms = []
        self.visited = False

    def addEdge(self, room):
        self.neighRooms.append(room)

    def delEdge(self, room):
        if room in self.neighRooms:
            self.neighRooms.remove(room)
            return True
        else:
            return False

    def __str__ (self):
        s = str(self.id) + ": wall - " + str(self.wall) + ", hole - " + str(self.hole) + ", monster - " + \
        str(self.monster) + ", gold - " + str(self.gold) + ", wind - " + str(self.wind) + ", smell - " + str(self.smell) + ", neighrooms: "
        for i in self.neighRooms:
            s += str(i.id)
            s += " "
        return s

rooms = []

def mazeClear():
	global rooms
	rooms = []


def getMaxPotential():
	ans = None
	for room in rooms:
		if (ans is None) or (room.potentialConns - len(room.neighRooms) >= ans.potentialConns - len(ans.neighRooms)):
			ans = room
	return ans

#get room with minimum number of possible connections
def getMinPotential(u):
	ans = None

	for room in rooms:
		if (room != u) and (room not in u.neighRooms) and (room.potentialConns - len(room.neighRooms)):
			if (ans is None) or (room.potentialConns - len(room.neighRooms) < ans.potentialConns - len(ans.neighRooms)):
				ans = room

	return ans

#check if all rooms are connected to each other, starting with room 'u'
def checkConnections(u):
	u.visited = True
	q = [u]

	while q:
		u = q.pop(0)
		for room in u.neighRooms:
			if not room.visited:
				q.append(room)
				room.visited = True

	for room in rooms:
		if not room.visited:
			return False

	return True


def buildMaze(N, K, k, p):
	mazeClear()

	if N < 0 or K < 0 or K > N or k < 0 or k > N - 1 or p < 0 or p > N - 1:
		raise ValueError("The input values are incorrect!")

	if N == 0:
		raise ValueError("The graph is empty!")

	if (K * k + (N - K) * p) % 2:
		raise Exception("It is impossible to build a graph!")

#Room(potentialConns = number of free connections)
	for i in range(K):
		rooms.append(Room(k))
	for i in range(K, N):
		rooms.append(Room(p))

#get the room with maximum possible connections
	u = getMaxPotential()
#while there is any potential in room - connect it with room with less potential
	while u.potentialConns - len(u.neighRooms):
	    v = getMinPotential(u)

	    if v is None:
	    	raise Exception("It is impossible to build a graph!")

	    u.addEdge(v)
	    v.addEdge(u)

	    u = getMaxPotential()

	if not checkConnections(rooms[0]):
		raise Exception("Not every room is connected!")

	for room in rooms:
		if room.potentialConns - len(room.neighRooms):
			raise Exception("It is impossible!")


def allocate(num_walls, num_holes, num_monster, num_golds):
    global rooms
    if num_walls + num_golds + num_holes > len(rooms):
        return "Number of features can not exceed the number of rooms"
    arr = rooms[:]
    shuffle(arr)

    for i in arr[:num_walls]:
        i.wall = 1

    for i in arr[num_walls:(num_walls + num_holes)]:
        i.hole = 1

    for i in arr[(len(rooms) - num_golds):]:
        i.gold = 1


def main(argv):
    N, K, k, p = int(argv[0]), int(argv[1]), int(argv[2]), int(argv[3])
    num_walls = int(argv[4])
    num_holes = int(argv[5])
    num_monster = int(argv[6])
    num_golds = int(argv[7])
    global rooms
    buildMaze(N, K, k, p)
    allocate(num_walls, num_holes, num_monster, num_golds)
    for room in rooms:
        print room


if __name__ == "__main__":
    main(sys.argv[1:])
