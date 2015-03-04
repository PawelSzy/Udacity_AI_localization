# The function localize takes the following arguments:
#
# colors:       a 2D list, each entry either 'R' (for a red cell) or 'G' (for a green cell)
#
# measurements: a list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:      a list of actions taken by the robot, each entry of the form [dy,dx], where
#               dx refers to the change in the x-direction (positive meaning movement to the right)
#               and dy refers to the change in the y-direction (positive meaning movement downward)
#               NOTE: the *first* coordinate is change in y; the *second* coordinate is change in x
#
# sensor_right: a float between 0 and 1, giving the probability that any given measurement is
#               correct; the probability that the measurement is incorrect is 1-sensor_right
#
# p_move:       a float between 0 and 1, giving the probability that any given movement command takes
#               place; the probability that the movement command fails (and the robot remains still);
#               the robot will NOT overshoot its destination in this exercise
#
# The function should RETURN (not just show) a 2D list (of the same dimensions as colors) that 
# gives the probabilities that the robot occupies each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform probability of being 
# in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.


def sense(p, measure, colors, pHit):
    q=[]
    row_lenght = len(colors[0])
    p = polacz_tabele(p)
    colors = polacz_tabele(colors)
    pMiss = 1-pHit
    for i in range(len(p)):
        hit = (measure == colors[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
        
    q = podziel_tabele(q, row_lenght)    
    return q

def polacz_tabele(tab):
    new_tab = []
    for row in tab:
        new_tab +=row
     
    return new_tab    

def podziel_tabele(tab, row_lenght):
    new_tab=[]
    for i in xrange(len(tab)/row_lenght):
        row = tab[(i*row_lenght):(i*row_lenght+row_lenght)]
        new_tab.append(row)
        
    return new_tab    
def move(p, move, pExact):
    pOvershoot = 1 - pExact
    
    #function move one row
    def move_row(row, move,pExact, pOvershoot):
        new_row = []
        if move==0:
            return row
        U = move
        for i in range(len(row)):
            s = pExact * row[(i-U) % len(row)]
            s += row[i]*(1-pExact)
            #s = s + pOvershoot * row[(i-U-1) % len(row)]
            #s = s + pUndershoot * row[(i-U+1) % len(row)]
            new_row.append(s)
        return new_row
    
    if move == [0,0]:
        return p
    
    #move up, down
    if move[0] !=0:
        q = []
        print "p", p
        transpoze_p = zip(*p)
        print "transpoze_p", transpoze_p
        for row in transpoze_p:
            new_row = move_row(row, move[0],pExact, pOvershoot)
            q.append(new_row)    
        print "q", q
        q = zip(*q)
        p=q
        print "p", p   
    #move right, left
    if move[1] !=0:
        q = []
        for row in p:
            new_row = move_row(row, move[1],pExact, pOvershoot)
            q.append(new_row)    
    return q




def localize(colors,measurements,motions,sensor_right,p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    
    # >>> Insert your code here <<<
    print p
    #measure
    
    #for i in xrange(len(colors)):
    for next_move, measure in zip(motions, measurements):
        p = move(p,next_move,p_move)
        p= sense(p, measure, colors, sensor_right)
    #print "move\n", p
    
    return p

def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print '[' + ',\n '.join(rows) + ']'
    
#############################################################
# For the following test case, your output should be 
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

colors = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
sensor_right = 0.7
p_move = 0.8
p = localize(colors,measurements,motions,sensor_right,p_move)
show(p) # displays your answer

#z = [[0,1,0,0,0],[0,0,0,0,0]]
#print "\n\n", move(z, [1,0], p_move)
