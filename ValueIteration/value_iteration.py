# Assignment Globals
GOAL_STATE = (3,6)
WIND = 0 # takes values 0, 1, 2 for the three cases in the assignment description
gamma = 1 # discount value
epsilon = 0.001
MAX_ITERS = 1000

# Actions
STAY = u"\u2022"
North = u"\u2191"
South = u"\u2193"
East = u"\u2192"
West = u"\u2190"
NW = u"\u2196"
NE = u"\u2197"
SW = u"\u2199"
SE = u"\u2198"
A = [STAY, North, South, East, West, NW, NE, SW, SE]

dir_matrix = [[STAY for x in range(7)] for x in range(7)] 
values_matrix = [[0 for x in range(7)] for x in range(7)] 

# Reward function
def R(s):
    if s[0] == 3 and s[1] == 6:
        return 0
    else:
        return -1

# Wind function
def W(s):
    if s[1] > 2 and s[1] < 6:
        s = (s[0] - WIND, s[1])
    if s[0] < 0:
        s = (0, s[1])
    return s

# Transition function
def T(s,a):
    s = W(s)
    if a == North:
        if s[0] > 0:
            s = (s[0]-1,s[1])
    elif a == South:
        if s[0] < 6:
            s = (s[0]+1,s[1])
    elif a == East:
        if s[1] < 6:
            s = (s[0],s[1]+1)
    elif a == West:
        if s[1] > 0:
            s = (s[0],s[1]-1)
    elif a == NE:
        # corner -> stay
        if s[0] == 0 and s[1] == 6:
            return s
        # against north wall -> move east
        elif s[0] == 0:
            s = (s[0],s[1]+1)
        # against east wall -> move north
        elif s[1] == 6:
            s = (s[0]-1,s[1])
        # anywhere else -> s = (i-1, j+1)
        else:
            s = (s[0]-1,s[1]+1)
    elif a == NW:
        # corner -> stay
        if s[0] == 0 and s[1] == 0:
            return s
        # against north wall -> move west
        elif s[0] == 0:
            s = (s[0],s[1]-1)
        # against west wall -> move north
        elif s[1] == 0:
            s = (s[0]-1,s[1])
        # anywhere else -> s = (i-1, j-1)
        else:
            s = (s[0]-1,s[1]-1)
    elif a == SE:
        # corner -> stay
        if s[0] == 6 and s[1] == 6:
            return s
        # against south wall -> move east
        elif s[0] == 6:
            s = (s[0],s[1]+1)
        # against east wall -> move south
        elif s[1] == 6:
            s = (s[0]+1,s[1])
        # anywhere else -> s = (i+1, j+1)
        else:
            s = (s[0]+1,s[1]+1)
    elif a == SW:
        # corner -> stay
        if s[0] == 6 and s[1] == 0:
            return s
        # against south wall -> move west
        elif s[0] == 6:
            s = (s[0],s[1]-1)
        # against west wall -> move south
        elif s[1] == 0:
            s = (s[0]+1,s[1])
        # anywhere else -> s = (i+1, j-1)
        else:
            s = (s[0]+1,s[1]-1)
    return s

# initialize U'
u = [[0 for x in range(7)] for x in range(7)] 
iters = 0
while iters <= MAX_ITERS:
    iters += 1
    delta = 0
    values_matrix = u
    for i in range(7):
        for j in range(7):
            s = (i,j)
            max_utility = -999999999
            max_a = STAY
            for a in A:
                s_prime = T(s,a)
                utility = values_matrix[s_prime[0]][s_prime[1]]
                if utility > max_utility:
                    max_utility = utility
                    max_a = a
            u[i][j] = R(s) + gamma * max_utility
            dir_matrix[i][j] = max_a
            if u[i][j]-values_matrix[i][j] > delta:
                delta = u[i][j]-values_matrix[i][j]
    if delta >= epsilon:
        break

# print results
for k in range(7):
    print(values_matrix[k])
print()
line = ''
for k in range(7):
    for l in range(7):
        line += dir_matrix[k][l] + ' '
        if len(line) == 14:
            print(line)
            line = ''

