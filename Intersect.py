#Использована библиотека https://github.com/prochitecture/sweep_intersector  
from math import inf
from collections import defaultdict
import heapq
from itertools import chain, dropwhile, count, repeat
import random

def geometric(p):
    return (next(dropwhile(lambda _: random.randint(1, int(1. / p)) == 1, count())) for _ in repeat(1))

class NIL(object):
    """Sentinel object that always compares greater than another object"""
    __slots__ = ()

    def __cmp__(self, other):
        # None is always greater than the other
        return 1

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __str__(self):
        return 'NIL'

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

class SkipNode():
    def __init__(self, key, data, succ, prev):
        self.key = key
        self.data = data
        self.succ = succ
        self.prev = prev

        for level in range(len(prev)):
            prev[level].succ[level] = self.succ[level].prev[level] = self

class SkipList():
    distribution = geometric(0.5)
    def __init__(self, **kwargs):

        self._tail = SkipNode(NIL(), None, [], [])
        self._head = SkipNode(None, 'HEAD', [self.tail], [])
        self._tail.prev.extend([self.head])

        self._size = 0

        for k, v in kwargs.items():
            self[k] = v

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def _height(self):
        return len(self.head.succ)

    def _level(self, start=None, level=0):
        node = start or self.head.succ[level]
        while node is not self.tail:
            yield node
            node = node.succ[level]

    def _scan(self, key):
        return_value = None
        height = len(self.head.succ)
        prevs = [self.head] * height
        node = self.head.succ[-1]
        for level in reversed(range(height)):
            node = next(
                dropwhile(
                    lambda node_: node_.succ[level].key <= key,
                    chain([self.head], self._level(node, level))
                )
            )
            if node.key == key:
                return_value = node
            else:
                prevs[level] = node

        return return_value, prevs

    def _insert(self, key, data):
            # Inserts data into appropriate position.

            node, update = self._scan(key)

            if node:
                node.data = data
                return node

            node_height = next(self.distribution) + 1 
            # because height should be positive non-zero
            # if node's height is greater than number of levels
            # then add new levels, if not do nothing
            height = len(self.head.succ)

            update.extend([self.head for _ in range(height, node_height)])

            self.head.succ.extend([self.tail for _ in range(height, node_height)])

            self.tail.prev.extend([self.head for _ in range(height, node_height)])

            new_node = SkipNode(key, data, [update[l].succ[l] for l in range(node_height)], [update[l] for l in range(node_height)])
            self._size += 1
            return new_node

    def _remove(self, key):
        # Removes node with given data. No operation if data is not in list.

        node, update = self._scan(key)
        if not node:
            return

        for level in range(len(node.succ)):
            update[level].succ[level] = node.succ[level]

        # trim not used head pointers
        for i in reversed(range(len(self.head.succ))):
            if self.head.succ[i] != self.tail:
                break
            elif i > 0:  # at least one pointer
                head_node = self.head.succ.pop()
                del head_node

        del node
        self._size -= 1

    def __len__(self):
        return self._size

    def __repr__(self):
        return 'skiplist({{{}}})'.format(
            ', '.join('{key}: {value}'.format(key=node.key, value=node.data) for node in self._level())
        )

    def __getitem__(self, key):
        # Returns item with given index
        node, _ = self._scan(key)
        if node is None:
            return None
        return node.data

    def __setitem__(self, key, value):
        return self._insert(key, value)

    def __delitem__(self, key):
        self._remove(key)

    def __iter__(self):
        # Iterate over keys in sorted order
        return (node.key for node in self._level())

    def iteritems(self):
        return ((node.key, node.data) for node in self._level())

    def iterkeys(self):
        return (item[0] for item in self.iteritems())

    def itervalues(self):
        return (item[1] for item in self.iteritems())


class SortSeq(SkipList):
    def insert(self, key, inf):
        """
        If there is a node <key,inf> in the structure, then inf is replaced by
        <inf> , otherwise a new node <key,inf> is added to the structure.
        In both cases the node is returned.
        """
        node, _ = self._scan(key)
        if node:
            node.data = inf
            return node
        else:
            node = self._insert(key, inf)
            return node

    def succ(self, node):
        """
        Returns the successor node of <node> in the sequence
        containing <node>, None if there is no such node.
        """
        node = node.succ[0]
        if node == self._tail:
            return None
        else:
            return node

    def pred(self, node):
        """
        Returns the predecessor node of <node> in the sequence
        containing <node>, None if there is no such node.
        """
        node = node.prev[0]
        if node == self._head:
            return None
        else:
            return node

    def changeInf(self, node, inf):
        """
        Makes <inf> be the data of <node>.
        """
        node.data = inf

    def lookup(self, key):
        """
        Returns the node with key <key>, None if there is no such item.
        """
        node, _ = self._scan(key)
        return node

    def locate(self,key):
        """
        Returns the node (key',inf) in SortSeq such that key' is minimal
        with key' >= key. None if no such node exists
        """
        _, update = self._scan(key)
        return update[0].succ[0]
 
    @staticmethod
    def key(node):
        """
        Returns the key of <node>.
        Precondition: <node> is a node in SortSeq
        """
        return node.key

    @staticmethod
    def inf(node):
        """
        Returns the element of <node>.
        Precondition: <node> is a node in SortSeq
        """
        return node.data

    def delete(self,key):
        """
        Removes the node with the key <key> from SortSeq.
        No operation if no such key exists.
        """
        self._remove(key)

    def empty(self):
        return len(self) == 0

    def min(self):
        if self.empty():
            return None
        else:
            return self.head.succ[0]

    # -----------------------------------------------------------------------
    # The following methods change the order of the structure so that it no
    # longer remains sorted. Therefore they are implemented here and
    # not in the base class <SkipList>.

    def insertAt(self, node, key, inf):
        """
        Like insert(key,inf), the node <node> gives the position of the
        node <key,inf> in the sequence.
        Precondition: <node> is a node in SortSeq with either key(node)
        is maximal with key(node) <= <key> or key(node) is minimal with 
        key(node) >= <key>.
        """
        if key == node.key:
            node.data = inf
            return node

        # Not often used, so we insert with the same height as <node>
        prevNode = node if key > node.key else node.prev[0]
        succNode = prevNode.succ[0]
        newSucc = [s for s in prevNode.succ if s == succNode]
        newPrev = [s for s in succNode.prev if s == prevNode]
        new_node = SkipNode(key, inf, newSucc, newPrev)
        self._size += 1
        return new_node

    def delItem(self, node):
        """
        Removes the <node> from SortSeq containing it.
        Precondition: <node> is a node in SortSeq.
        """
        for level in range(len(node.succ)):
            node.prev[level].succ[level] = node.succ[level]
            node.succ[level].prev[level] = node.prev[level]
        # trim not used head pointers
        for i in reversed(range(len(self.head.succ))):
            if self.head.succ[i] != self.tail:
                break
            elif i > 0:  # at least one pointer
                head_node = self.head.succ.pop()
                del head_node
        del node
        self._size -= 1

    def reverseItems(self, a, b):
        """
        The subsequence of SortSeq from nodes <a> to <b> is reversed.
	    Precondition: Node <a> appears before <b> in SortSeq.
        NOTE: This operation destroys the order in the SortSeq!
        """
        while a != b:
            c = a
            a = a.succ[0]
            self.delItem(c)

            # insert c after b
            predNode = b
            succNode = b.succ[0]
            c.succ = [s for s in predNode.succ if s == succNode]
            c.prev = [s for s in succNode.prev if s == predNode]
            for level in range(len(c.prev)):
                c.prev[level].succ[level] = c.succ[level].prev[level] = c
            self._size += 1

class Point():
    ID = 0
    EPS = 0.00001
    EPS2 = EPS*EPS
    def __init__(self,p):
        self.x = p[0]
        self.y = p[1]
        self.id = Point.ID
        Point.ID += 1

    def compare(self,other):
        if self is other: return 0
        dx = self.x - other.x
        if dx >  Point.EPS2: return  1
        if dx < -Point.EPS2: return -1
        dy = self.y - other.y
        if dy >  Point.EPS2: return  1
        if dy < -Point.EPS2: return -1
        return 0

    def __gt__(self,other):
        return self.compare(other) > 0

    def __lt__(self,other):
        return self.compare(other) < 0

    def __ge__(self,other):
        return self.compare(other) >= 0

    def __le__(self,other):
        return self.compare(other) <= 0

    def __eq__(self,other):
        if other is None: return False
        return self.compare(other) == 0

    def __iter__(self):
        # used to create tuples
        return iter([self.x,self.y])

    def __repr__(self):
        return '(%d: %6.2f,%6.2f)'%(self.id,self.x,self.y)

    def plot(self,color='k',size=3):
        import matplotlib.pyplot as plt
        plt.plot(self.x,self.y,color+'o',markersize=size)
        plt.text(self.x,self.y,str(self.id))

class Segment():
    pSweep = None
    ID = 0
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.dx = self.p2.x - self.p1.x
        self.dy = self.p2.y - self.p1.y

        self.id = Segment.ID
        Segment.ID += 1

        if self.p2.x != self.p1.x:
            self.slope = self.dy / self.dx
            self.yShift = self.p1.y - self.slope * self.p1.x
        else: # vertical segment
            self.slope = inf
            self.yShift = -1. * inf

    def start(self):
        return self.p1

    def end(self):
        return self.p2

    def isTrivial(self):
        return self.dx == 0 and self.dy == 0

    @staticmethod
    def setpSweep(pSweep):
        Segment.pSweep = pSweep

    @staticmethod
    # see https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
    # for comparison in Python >= 3.0
    def cmpVal(a, b):
        return (a > b)*1. - (a < b)*1.

    def compare(self,other):
        if self is other:
            return 0
        s = 0
        if Segment.pSweep is self.p1:
            s = Segment.orientation(other,Segment.pSweep)
        elif Segment.pSweep is other.p1:
            s = -Segment.orientation(self,Segment.pSweep)
        else:
            raise Exception('Compare error in Segment')

        if s or self.isTrivial() or other.isTrivial():
            return s
        s = Segment.orientation(other,self.p2)
        # overlapping segments will be ordered by their id-numbers
        return s if s else self.id-other.id

    @staticmethod
    def orientation(s,point):
        orient = s.dy*(point.x-s.p1.x) - s.dx*(point.y-s.p1.y)
        return Segment.cmpVal( s.dy*(s.p1.x-point.x), s.dx*(s.p1.y-point.y) )

    def intersectionOfLines(self,s):
        if self.slope == s.slope: return None
        if self.p1 == s.p1 or self.p1 == s.p2:
            return self.p1
        if self.p2 == s.p1 or self.p2 == s.p2:
            return self.p2
        if self.p1.x == self.p2.x: # is vertical
            cx = self.p1.x
        else:
            if s.p1.x == s.p2.x: # is vertical
                cx = s.p1.x
            else:
                cx = (s.yShift-self.yShift)/(self.slope-s.slope)
        if self.p1.x == self.p2.x: # is vertical
            cy = s.slope * cx + s.yShift
        else:
            cy = self.slope * cx + self.yShift
        return Point((cx,cy))

    def __gt__(self,other):
        # return self.p1 > other.p1
        return self.compare(other) > 0

    def __lt__(self,other):
        # return self.p1 < other.p1
        return self.compare(other) < 0

    def __ge__(self,other):
        # return self.p1 >= other.p1
        return self.compare(other) >= 0

    def __le__(self,other):
        # return self.p1 <= other.p1
        return self.compare(other) <= 0

    def __eq__(self,other):
        if other is None: return False
        # return self.p1 == other.p1
        return self.compare(other) == 0

    def __hash__(self):
        return self.id

    def __repr__(self):
        return '[%d: %s -> %s]'%(self.id,str(self.p1),str(self.p2))

    def plot(self,color='k'):
        import matplotlib.pyplot as plt
        self.start().plot('b')
        self.end().plot('r')
        v1 = self.start()
        v2 = self.end()
        plt.plot([v1.x,v2.x],[v1.y,v2.y],color)
        x = (v1.x+v2.x)/2
        y = (v1.y+v2.y)/2
        plt.text(x,y,str(self.id))
class QueueNode():
    def __init__(self,key,inf):
        self.key = key
        self.inf = inf
    def __gt__(self,other):
        return self.key > other.key

    def __lt__(self,other):
        return self.key < other.key

    def __ge__(self,other):
        return self.key >= other.key

    def __le__(self,other):
        return self.key <= other.key

    def __eq__(self,other):
        return self.key == other.key

class PriorityQueue():
    def __init__(self):
        self.queue = []

    @staticmethod
    def prio(node):
        """
        Returns the priority of <node>
        """
        return node.key

    @staticmethod
    def inf(node):
        """
        Returns the value of <node>
        """
        return node.inf

    def insert(self, key, value):
        """
        Adds a new node to the structure and returns it.
        """
        node = QueueNode(key,value)
        heapq.heappush(self.queue, node)
        return node

        return self.heapInsert(key, value)

    def min(self):  # corresponds to find_min() in LEDA
        """
        Returns the node with minimal priority 
        None if structure is empty
        """
        if self.queue:
            return self.queue[0]
        else:
            return None

    def delMin(self):
        """
        Removes the node node=self.findMin()
        from structure and return its priority.
        Precondition: the structure is not empty.
        """
        return heapq.heappop(self.queue)

    def size(self):
        """
        Returns the size of the structure
        """
        return len(self.queue)

    # returns True if the structure is empty
    #  and False otherwise.
    def empty(self):
        """
        Returns True if the structure is empty,
        else False.
        """
        return not self.queue

class SweepIntersector():
    def __init__(self):
        self.X_structure = SortSeq()
        self.Y_structure = SortSeq()
        self.lastNode = dict()
        self.original = dict()
        self.assoc = dict()
        self.interDic = dict()
        self.segQueue = PriorityQueue()
        self.pSweep = None
        self.N = 0
        self.isectDict = defaultdict(list)
        self.intersectingSegments = defaultdict(list)

    def findIntersections(self,origSegList):
        """
        Main method. Computes all intersections between a list <origSegList> of
        segments.
        <origSegList>: List of tuples (vs,ve) for segments, where vs is the start
                       point and ve the end point. The points v1 and v2 are given
                       as tuples (x,y) where x and y are their coordinates in the
                       plane. 
        Returns:       A dictionary <seg:isects> for all segments that had inter-
                       sections. <seg>, the key of the dictionary, is a tuple 
                       (vs,ve) identical to the one in the input list and <isects>
                       is the list of the intersections points. These points
                       are given tuples (x,y) where again x and y are their
                       coordinates in the plane. This list includes the start and
                       end points vs and ve and is ordered from vs to ve.

        Usage example:

            from SweepIntersectorLib import SweepIntersector

            origSegList = []
            origSegList.append( ((1.0,1.0),(5.0,6.0)) )
            origSegList.append( ((1.0,4.0),(4.0,0.0)) )
            origSegList.append( ((1.5,5.0),(3.0,1.0)) )
            ...

            isector = SweepIntersector()
            isectDic = isector.findIntersections(origSegList)
            for seg,isects in isectDic.items():
                ...

        """
        self.initializeStructures(origSegList)

        # Main loop
        while not self.X_structure.empty():
            # move <pSweep> to next event point.
            event = self.X_structure.min()
            Segment.pSweep = self.pSweep = self.X_structure.key(event)
            v = self.pSweep

            # self.G.append(self.pSweep);
            # print('GRAPH')
            # for elem in self.G:
            #     print(elem)
            # print(self.Y_structure)
            # p = self.Y_structure.head
            # while p.succ[0].key:
            #     node = p.succ[0]
            #     if node.data:
            #         print('*')
            #         print('k--> ',node.key)
            #         print('d--> ',node.data,type(node.data))
            #         print('dk---> ',node.data.key)
            #         print('dd---> ',node.data.data,type(node.data.data))
            #     p = p.succ[0]
            # for key,val in self.interDic.items():
            #     print('dic',key, val.key)
            # self.plotAll()

            # If there is an item <sit> associated with <event>,
            # key(sit) is either an ending or passing segment.
            # We use <sit> as an entry point to compute the bundle of
            # segments ending at or passing through <pSweep>.
            # In particular, we compute the first <sitFirst> and last
            # <sitLast> item of this bundle and the successor <sitSucc>
            # and predecessor <sitPred> items.
            sit = SortSeq.inf(event)

            if sit is None:
                # Here we do not know any segments ending or passing through 
                # <pSweep>. However, <pSweep> could come to lie on a segment 
                # inserted before. To check this we look up the zero length 
                # segment (pSweep,pSweep).
                sit = self.Y_structure.lookup(Segment(self.pSweep,self.pSweep))

            sitSucc  = None
            sitPred  = None
            sitFirst = None
            sitLast  = None

            # A value of None for <sitSucc> and <sitPred> after the 
            # following computation indicates that there are no segments 
            # ending at or passing through <pSweep>

            if sit: # key(sit) is an ending or passing segment
                # first walk up until <sitSucc>
                while self.Y_structure.inf(sit) == event:
                    sit = self.Y_structure.succ(sit)
                sitSucc = self.Y_structure.succ(sit)
                xit = self.Y_structure.inf(sit)
                if xit: 
                    s1 = self.Y_structure.key(sit)
                    s2 = self.Y_structure.key(sitSucc)
                    self.interDic[(s1.id,s2.id)] = xit

                # Walk down until <sitPred>, construct edges for all segments
                # in the bundle, assign information <None> to continuing segments,
                # and delete ending segments from the Y_structure
                while True:
                    s = self.Y_structure.key(sit)
                    sr = self.assoc[s]

                    self.lastNode[s] = v
                    if self.pSweep is s.p2: #  ending segment
                        it = self.Y_structure.pred(sit)
                        self.Y_structure.delItem(sit)
                        sit = it;
                    else:   # passing segment
                        self.Y_structure.changeInf(sit,None)
                        sit = self.Y_structure.pred(sit)
                        if (sr is not s) and (sr.p2 is self.pSweep):
                            self.assoc[s] = s

                    if self.Y_structure.inf(sit) != event:
                        break # end of while True:

                sitPred  = sit
                sitFirst = self.Y_structure.succ(sitPred)

                # reverse the bundle of continuing segments (if existing)
                if sitFirst != sitSucc:
                    sitLast = self.Y_structure.pred(sitSucc)
                    self.Y_structure.reverseItems(sitFirst,sitLast)

            # Insert all segments starting at <pSweep>
            while self.pSweep is self.nextSeg.start():  # identity
                # insert <nextSeg> into the Y-structure and associate the
                # corresponding item with the right endpoint of <nextSeg> in
                # the X-structure (already present)
                sit = self.Y_structure.locate(self.nextSeg)
                seg0 = self.Y_structure.key(sit)

                if self.nextSeg != seg0:
                    # <next_seg> is not collinear with <seg0>, insert it
                    sit = self.Y_structure.insertAt(sit, self.nextSeg, None)
                    self.X_structure.insert(self.nextSeg.end(),sit)
                    self.lastNode[self.nextSeg] = v

                    if sitSucc is None:
                        # There are only starting segments, compute <sitSucc>
                        # and <sitPred> using the first inserted segment
                        sitSucc = self.Y_structure.succ(sit)
                        sitPred = self.Y_structure.pred(sit)
                        sitFirst = sitSucc
                else:
                    # <nextSeg> and <seg0> are collinear; if <next_seg> is
                    # longer insert (seg0.end(),next_seg.end()) into <segQueue>
                    p = seg0.end()
                    q = self.nextSeg.end()
                    self.assoc[seg0] = self.nextSeg
                    if p < q:
                        newSeg = Segment(p,q) 
                        self.assoc[newSeg] = newSeg
                        self.original[newSeg] = self.original[self.nextSeg]
                        self.segQueue.insert(p,newSeg)

                # delete minimum and assign new minimum to <nextSeg>
                self.segQueue.delMin()
                self.nextSeg = self.segQueue.inf(self.segQueue.min())

            # if <sitPred> still has the value <None>, there were no ending, 
            # passing or starting segments, i.e., <pSweep> is an isolated 
            # point. In this case we are done, otherwise we delete the event 
            # associated with <sitPred> from the X-structure and compute 
            # possible intersections between new neighbors.
            if sitPred is not None:
                # <sitPred> is no longer adjacent to its former successor we 
                # change its intersection event to None.
                xit = self.Y_structure.inf(sitPred) 

                if xit is not None: 
                    s1 = self.Y_structure.key(sitPred)
                    s2 = self.Y_structure.key(sitFirst)
                    self.interDic[(s1.id,s2.id)] = xit
                    self.Y_structure.changeInf(sitPred, None)

                # compute possible intersections between <sitPred> and its
                # successor and <sit_succ> and its predecessor
                self.computeIntersection(sitPred)
                sit = self.Y_structure.pred(sitSucc)
                if sit != sitPred:
                    self.computeIntersection(sit)
            self.X_structure.delItem(event)

        self.collectAndSortResult()
        return self.intersectingSegments
 
    def initializeStructures(self,origSegList):
        """
        Initializes the class using the provided list of segments <origSegList>.
        A vertex <v> is represented as a tuple (x,y).
        A segment <s> is represented by a tuple of vertices (vs,ve), where <vs> is the 
        starting point and <ve> the end point. <origSegList> is a list of segments <s>.
        """
        infinity = 1
        for segIndex, seg in enumerate(origSegList):
            v1, v2 = seg

            # Compute an upper bound |Infinity| for the input coordinates
            while abs(v1[0]) >= infinity or abs(v1[1]) >= infinity or \
                  abs(v2[0]) >= infinity or abs(v2[1]) >= infinity:
                infinity *= 2;

            it1 = self.X_structure.insert(Point(seg[0]),None)
            it2 = self.X_structure.insert(Point(seg[1]),None)
            if it1 == it2: continue  # Ignore zero-length segments

            # Insert operations into the X-structure leave previously
            # inserted points unchanged to achieve that any pair of
            # endpoints <p1> and <p2> with p1 == p2 are identical.
            p1 = SortSeq.key(it1)
            p2 = SortSeq.key(it2)
            s = Segment(p1,p2) if p1 < p2 else Segment(p2,p1)

            # use maps to associate with every segment its original
            self.original[s] = (seg,segIndex)
            self.assoc[s] = s

            # for every created segment (p1,p2) insert the pair (p1,(p1,p2)) 
            # into priority queue <segQueue>
            self.segQueue.insert(s.start(),s)

        # insert a lower and an upper sentinel segment to avoid special
        # cases when traversing the Y-structure
        lowerSentinel = Segment( Point((-infinity,-infinity)), Point((infinity,-infinity)))
        upperSentinel = Segment( Point((-infinity, infinity)), Point((infinity, infinity)))

        # the sweep begins at the lower left corner
        Segment.pSweep = self.pSweep = lowerSentinel.start()
        self.Y_structure.insert(upperSentinel,None);
        self.Y_structure.insert(lowerSentinel,None);

        # insert a stopper into <segQueue> and initialize |next_seg| with
        # the first segment in the queue.
        pStop = Point((infinity,infinity))
        sStop = Segment(pStop,pStop)
        self.segQueue.insert(pStop,sStop)
        self.nextSeg = self.segQueue.inf(self.segQueue.min())
        self.N = sStop.id

    def computeIntersection(self,sit0):
        # Given an item <sit0> in the Y-structure compute the point of 
        # intersection with its successor and (if existing) insert it into 
        # the event queue and do all necessary updates.
        sit1 = self.Y_structure.succ(sit0)
        s0   = self.Y_structure.key(sit0)
        s1   = self.Y_structure.key(sit1)

        # <s1> is the successor of <s0> in the Y-structure, hence,
        # <s0> and <s1> intersect right or above of the sweep line
        # if (s0.start(),s0.end(),s1.end() is not a left turn and 
        # (s1.start(),s1.end(),s0.end() is not a right turn.
        # In this case we intersect the underlying lines
        if Segment.orientation(s0,s1.end()) <= 0 and Segment.orientation(s1,s0.end()) >= 0:
            it = self.interDic.get((s0.id,s1.id),None)
            if it is not None:
                self.Y_structure.changeInf(sit0,it)
                del self.interDic[(s0.id,s1.id)]
            else:
                q = s0.intersectionOfLines(s1)
                if q:
                    self.Y_structure.changeInf(sit0, self.X_structure.insert(q,sit0))

                    # insert intersection point into result dictionary
                    if s0.p1 != q and s0.p2 != q:
                        self.isectDict[self.original[s0]].append((q.x,q.y))
                    if s1.p1 != q and s1.p2 != q:
                        self.isectDict[self.original[s1]].append((q.x,q.y))

    @staticmethod
    def inorderExtend(segment, v1, v2, points):
        # Extend a segment <segment> by <points> that are on
        # between the points v1, v2
        k, r = None, False
        if v1[0] < v2[0]:   k, r = lambda i: i[0], True
        elif v1[0] > v2[0]: k, r = lambda i: i[0], False
        elif v1[1] < v2[1]: k, r = lambda i: i[1], True
        else:               k, r = lambda i: i[1], False
        l = [ p for p in sorted(points, key=k, reverse=r) ]
        i = next((i for i, p in enumerate(segment) if p == v2), -1)
        assert(i>=0)
        for e in l:
            # a vertex can appear only once in a segment
            if not e in segment:
                segment.insert(i, e)
        return segment

    def collectAndSortResult(self):
        for seg,isects in self.isectDict.items():
            v1,v2 = seg[0]
            segment = self.inorderExtend([v1,v2],v1,v2,isects)
            self.intersectingSegments[seg[0]] = segment
            
    def plotY(self):
        import matplotlib.pyplot as plt
        for node in self.Y_structure._level():
            node.key.plot()
            if node.data:
                node.data.plot('m')
        plt.gca().axis('equal')
        plt.show()

    def plotResult(self):
        import matplotlib.pyplot as plt
        plt.close()
        for key,value in self.original.items():
            v1,v2 = key.p1,key.p2
            plt.plot([v1.x,v2.x],[v1.y,v2.y],'k:')
            plt.plot(v1.x,v1.y,'k.')
            plt.plot(v2.x,v2.y,'k.')
            # plt.text(v1.x,v1.y,str(v1.id))
        # for isect in self.isects:
        #     plt.plot(isect.x,isect.y,'ro',markersize=3,zorder=10)
        # plt.gca().axis('equal')
        # plt.show()

    def plotAll(self):
        import matplotlib.pyplot as plt
        plt.subplot(2,2,1)
        for isect in self.isects:
            plt.plot(isect.x,isect.y,'rx',markersize=12)
        count = 0
        for key,value in self.original.items():
            v1,v2 = key.p1,key.p2
            plt.plot([v1.x,v2.x],[v1.y,v2.y],'k')
            plt.text(v1.x,v1.y,str(v1.id))
            count += 1
        plt.gca().axis('equal')
        plt.gca().set_title('Original Segs')
        plt.subplot(2,2,2)
        for s in self.original.keys():
            v1,v2 = s.p1, s.p2
            plt.plot([v1.x,v2.x],[v1.y,v2.y],'k')
            x = (v1.x+v2.x)/2
            y = (v1.y+v2.y)/2
            plt.text(x,y,str(s.id))
        plt.gca().axis('equal')
        plt.gca().set_title('Segments')
        plt.subplot(2,2,3)
        for node in self.X_structure._level():
            node.key.plot()
            if node.data:
                node.data.key.plot()
        plt.plot(self.pSweep.x,self.pSweep.y,'co',markersize=8)
        plt.gca().axis('equal')
        plt.gca().set_title('X-Structure')
        plt.subplot(2,2,4)
        for node in self.Y_structure._level():
            node.key.plot()
            if node.data:
                if isinstance(node.data.key,Segment):
                    node.data.key.plot('m')
                else:
                    node.data.key.plot('m',10)
        plt.plot(self.pSweep.x,self.pSweep.y,'co',markersize=8)
        for isect in self.isects:
            plt.plot(isect.x,isect.y,'rx',markersize=3)
        plt.gca().axis('equal')
        plt.gca().set_title('Y-Structure')
        plt.show()
