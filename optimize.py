import time
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()
    
def greatestKDist(pts):
    maxdist = 0 #Start 0 and increase...
    maxpt = []
    for x in np.arange(0,1,0.01):
        for y in np.arange(0,1,0.01):
            closeone = 1E99 # 10^99 is large, decrease this to the closest nearby station distance. 
            #What is closest?
            for [ptx, pty] in pts:
                dist = np.sqrt( np.square(x-ptx) + np.square(y-pty) )
                if dist < closeone:
                    closeone = dist
            if( closeone > maxdist ):
                #This point is currently the max closest distance found.
                maxdist = closeone
                maxpt = [x,y]
    #print("max pt, dist:")
    #print(maxpt)
    return maxdist
    
n = int(input("How many stations?"))
plt.ion()
plt.figure()
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()

tellme('Choose beginning points')

while True:
    pts = []
    while len(pts) < n:
        pts = np.asarray(plt.ginput(n, timeout=-1))
        if len(pts) < n:
            tellme('Too few points, starting over')
            time.sleep(1)  # Wait a second

    print(pts)
    print( "max distance from station is %s" % (greatestKDist(pts),) )
    sleep(1)
    
    #Adjust until optimal:
    directions = [[1,0],[-1,0],[0,1],[0,-1]]
    adjustment = 0.1
    while adjustment > 0.001:
        changes = 0
        for i in range(len(pts)): #Each point
            #What direction should this go in?
            for direction in directions:
                #If we say tmp = pts then it would change when changing it. make a copy.
                tmp = [x for x in pts]
                # array + array appends them using python "+", so use add:
                # (Python * doesn't multiply arr * float
                tmp[i] = np.add(tmp[i], np.multiply(direction,adjustment))
                if( greatestKDist(pts) > greatestKDist(tmp) ):
                    #Found a more optimal one.
                    print("%0.4lf %0.4lf should move %s,%s to %0.4lf,%0.4lf" % 
                       (pts[i][0], pts[i][1], direction[0]*adjustment,direction[1]*adjustment, tmp[i][0], tmp[i][1] ))
                    pts[i] = tmp[i]
                    #changed the actual position to a better one.
                    changes += 1
        print('changed %s positions' % (changes,) )
        plt.clf() #Clear previous
        # Get x and y with p[0] and p[1] of each [x,y] point, plot it with linewidth=0, no line:
        plt.plot( [p[0] for p in pts], [p[1] for p in pts], color='green', marker='o', lw='0')
                
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.pause(0.1) # render to screen
        if changes == 0:
            adjustment = adjustment/2
    print( "max distance from station is %s" % (greatestKDist(pts),) )

    if plt.waitforbuttonpress():
        break
