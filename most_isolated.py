from array import *
from operator import itemgetter
import sys

"""
Define a node in which coordinate data will be stored.
These nodes will be combined to build a 2d-tree

Parameters
    place (String): place name
    x (int): x-coordinate
    y (int): y-coordinate
    left (Node): left child
    right (Node): right child
"""
class Node:
    def __init__(self, place, x, y, left, right):
        self.place = place
        self.x = x
        self.y = y
        self.left = left
        self.right = right

"""
Function to convert 2d array to 2d tree

Arguments:
    coords (Array[][3]): coordinate data read from file

The input array takes the form
[
    [place1, x1, y1],
    [place2, x2, y2],
    [place3, x3, y3]
]

Return:
    2dTree (Node): the array represented as a 2D tree 
"""
def construct2dTree(*, coords):

    def construct(*, coords, depth):
        if len(coords) == 0:
            return None
    
        """
        Find the median coordinate on the given axis.
        Alternate the axis used to divide the coordinates
        if depth is even, use x axis
        otherwise, use y axis
        """
        sortedCoords = sorted(coords, key=itemgetter(depth%2 + 1))
        middle = len(coords) // 2

        """
        Call function recursively to obtain left and right nodes
        """
        return Node(
            place=sortedCoords[middle][0], 
            x=sortedCoords[middle][1], 
            y=sortedCoords[middle][2],
            left=construct(
                coords=sortedCoords[:middle], 
                depth=depth+1),
            right=construct(
                coords=sortedCoords[middle+1:],
                depth=depth+1
            )
        )
    
    return construct(coords=coords, depth=0)

"""
Calculate the distance to a node's nearest neighbour.

Arguments:
    root (Node): the coordinate tree
    target (Node): the node who's nearest neighbour I am trying to find

Return:
    minDistance (int): distance squared to the target's nearest neighbour
"""
def getNearestNeighbour(*, root, target):
    minDistance = None

    """
    Return the Euclidian distance squared between two points
    """
    def getSquaredDistance(*, x1, y1, x2, y2):
        return (x1 - x2)**2 + (y1 - y2)**2

    """
    Search for nearest neighbour
    """
    def search(*, root, target, depth):
        nonlocal minDistance

        if root is None:
            return

        distance = getSquaredDistance(
            x1=root.x,
            y1=root.y,
            x2=target.x,
            y2=target.y
        )

        """
        Check that we are not calculating a node's distance from itself.
        This assumes no duplication of place names
        """
        if root.place != target.place:
            if minDistance is None or distance < minDistance:
                minDistance = distance
        
        """
        Calculate distance along axis between the current point and the target point
        """
        if depth%2 == 0:
            diff = int(target.x) - int(root.x)
        else:
            diff = int(target.y) - int(root.y)


        """
        If diff <= 0, first check if the left child node is closer than the current node.
        Then check if a nearer node may exist on the other side of the dividing line (under the right child node)
        This may be the case if the distance to the dividing line along the axis is less that the distance to the nearest node.
        Follow the reverse procedure for diff > 0
        """
        if diff <= 0:
            search(
                root=root.left, 
                target=target, 
                depth=depth+1)
            if diff**2 < minDistance:
                search(
                    root=root.right, 
                    target=target, 
                    depth=depth+1)
        else:
            search(
                root=root.right, 
                target=target, 
                depth=depth+1)
            if diff**2 < minDistance:
                search(
                    root=root.left, 
                    target=target, 
                    depth=depth+1)

    search(
        root=root,
        target=target,
        depth=0
    )

    return minDistance


"""
MAIN PROGRAMME
"""

"""
pass filename as a parameter when calling the script
e.g python3 most_isolated.py problem_big.txt
"""
file = open(sys.argv[1], "r")

data = []

"""
Convert text file to 2d array
"""
for line in file:
    placeData = line.split()
    data.append([placeData[0], int(placeData[1]), int(placeData[2])])

file.close()

if (len(data) == 0):
    print("No data provided")
else:
    tree = construct2dTree(coords=data)
    maxDistance = 0
    mostIsolated = tree.place
    """
    Iterate through all points.
    Find the point with the largest distance to its nearest neighbour
    """
    for point in data:
        distance = getNearestNeighbour(root=tree, target=Node(
            place=point[0],
            x=point[1],
            y=point[2],
            left=None,
            right=None
        ))
        if distance != None and distance > maxDistance:
            maxDistance = distance
            mostIsolated = point[0]
            
    print(mostIsolated)