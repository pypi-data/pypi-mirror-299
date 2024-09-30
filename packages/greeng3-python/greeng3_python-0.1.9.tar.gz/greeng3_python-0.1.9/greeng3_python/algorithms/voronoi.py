#############################################################################
#
# Voronoi diagram calculator/ Delaunay triangulator
# Translated to Python by Bill Simons
# September, 2005
#
# Calculate Delaunay triangulation or the Voronoi polygons for a set of
# 2D input points.
#
# Derived from code bearing the following notice:
#
#  The author of this software is Steven Fortune.  Copyright (c) 1994 by AT&T
#  Bell Laboratories.
#  Permission to use, copy, modify, and distribute this software for any
#  purpose without fee is hereby granted, provided that this entire notice
#  is included in all copies of any software which is or includes a copy
#  or modification of this software and in all copies of the supporting
#  documentation for such software.
#  THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
#  WARRANTY.  IN PARTICULAR, NEITHER THE AUTHORS NOR AT&T MAKE ANY
#  REPRESENTATION OR WARRANTY OF ANY KIND CONCERNING THE MERCHANTABILITY
#  OF THIS SOFTWARE OR ITS FITNESS FOR ANY PARTICULAR PURPOSE.
#
# Comments were incorporated from Shane O'Sullivan's translation of the
# original code into C++ (http://mapviewer.skynet.ie/voronoi.html)
#
# Steve Fortune's homepage: http://netlib.bell-labs.com/cm/cs/who/sjf/index.html
#
#############################################################################
import math


def cmp(l, r):
    """
    We no longer have this function in python3, so duplicate its functionality

    Args:
        l (Any):  left param
        r (Any):  right param
    """
    if l < r:
        return -1
    if l > r:
        return 1
    return 0


#############################################################################
#
# For programmatic use two functions are available:
#
#   compute_voronoi_diagram(points)
#
#        Takes a list of point objects (which must have x and y fields).
#        Returns a 3-tuple of:
#
#           (1) a list of 2-tuples, which are the x,y coordinates of the
#               Voronoi diagram vertices
#           (2) a list of 3-tuples (a,b,c) which are the equations of the
#               lines in the Voronoi diagram: a*x + b*y = c
#           (3) a list of 3-tuples, (l, v1, v2) representing edges of the
#               Voronoi diagram.  l is the index of the line, v1 and v2 are
#               the indices of the vetices at the end of the edge.  If
#               v1 or v2 is -1, the line extends to infinity.
#
#   compute_delaunay_triangulation(points):
#
#        Takes a list of point objects (which must have x and y fields).
#        Returns a list of 3-tuples: the indices of the points that form a
#        Delaunay triangle.
#
#############################################################################

TOLERANCE = 1e-9
BIG_FLOAT = 1e38
CRADIUS = 1.0  # Totally undefined value, presumably during translation to C++-ish python


# ------------------------------------------------------------------
class Context:
    def __init__(self):
        self.doPrint = 0
        self.debug = 0
        self.plot = 0
        self.triangulate = False
        self.vertices = []  # list of vertex 2-tuples: (x,y)
        # equation of line 3-tuple (a b c), for the equation of the line a*x+b*y = c
        self.lines = []
        # edge 3-tuple: (line index, vertex 1 index, vertex 2 index)   if either vertex index is -1,
        self.edges = []
        # the edge extends to infiinity
        self.triangles = []  # 3-tuple of vertex indices

    def circle(self, x, y, rad):
        pass

    def clip_line(self, edge):
        pass

    def line(self, x0, y0, x1, y1):
        pass

    def out_site(self, s):
        if self.debug:
            print(f'site ({s.sitenum}) at {s.x} {s.y}')
        elif self.triangulate:
            pass
        elif self.plot:
            self.circle(s.x, s.y, CRADIUS)
        elif self.doPrint:
            print(f's {s.x} {s.y}')

    def out_vertex(self, s):
        self.vertices.append((s.x, s.y))
        if self.debug:
            print(f'vertex({s.sitenum}) at {s.x} {s.y}')
        elif self.triangulate:
            pass
        elif self.doPrint and not self.plot:
            print(f'v {s.x} {s.y}')

    def out_triple(self, s1, s2, s3):
        self.triangles.append((s1.sitenum, s2.sitenum, s3.sitenum))
        if self.debug:
            print(
                f'circle through left={s1.sitenum} right={s2.sitenum} bottom={s3.sitenum}')
        elif self.triangulate and self.doPrint and not self.plot:
            print(f'{s1.sitenum} {s2.sitenum} {s3.sitenum}')

    def out_bisector(self, edge):
        self.lines.append((edge.a, edge.b, edge.c))
        if self.debug:
            print(
                f'line({edge.edgenum}) {edge.a}x+{edge.b}y={edge.c}, bisecting {edge.reg[0].sitenum} {edge.reg[1].sitenum}')
        elif self.triangulate:
            if self.plot:
                self.line(edge.reg[0].x, edge.reg[0].y,
                          edge.reg[1].x, edge.reg[1].y)
        elif self.doPrint and not self.plot:
            print(f'l {edge.a} {edge.b} {edge.c}')

    def out_edge(self, edge):
        sitenum_l = -1
        if edge.ep[Edge.LE] is not None:
            sitenum_l = edge.ep[Edge.LE].sitenum
        sitenum_r = -1
        if edge.ep[Edge.RE] is not None:
            sitenum_r = edge.ep[Edge.RE].sitenum
        self.edges.append((edge.edgenum, sitenum_l, sitenum_r))
        if not self.triangulate:
            if self.plot:
                self.clip_line(edge)
            elif self.doPrint:
                print(f'e {edge.edgenum} {sitenum_l} {sitenum_r}')


# ------------------------------------------------------------------
def voronoi(site_list, context):
    edge_list = EdgeList(site_list.xmin, site_list.xmax, len(site_list))
    priority_q = PriorityQueue(site_list.ymin, site_list.ymax, len(site_list))
    site_iter = site_list.iterator()

    bottomsite = site_iter.next()
    context.out_site(bottomsite)
    newsite = site_iter.next()
    minpt = Site(-BIG_FLOAT, -BIG_FLOAT)
    while True:
        if not priority_q.is_empty():
            minpt = priority_q.get_min_pt()

        if newsite and (priority_q.is_empty() or cmp(newsite, minpt) < 0):
            # newsite is smallest -  this is a site event
            context.out_site(newsite)

            # get first Halfedge to the LEFT and RIGHT of the new site
            lbnd = edge_list.leftbnd(newsite)
            rbnd = lbnd.right

            # if this halfedge has no edge, bot = bottom site (whatever that is)
            # create a new edge that bisects
            bot = lbnd.rightreg(bottomsite)
            edge = Edge.bisect(bot, newsite)
            context.out_bisector(edge)

            # create a new Halfedge, setting its pm field to 0 and insert
            # this new bisector edge between the left and right vectors in
            # a linked list
            bisector = Halfedge(edge, Edge.LE)
            edge_list.insert(lbnd, bisector)

            # if the new bisector intersects with the left edge, remove
            # the left edge's vertex, and put in the new one
            p = lbnd.intersect(bisector)
            if p is not None:
                priority_q.delete(lbnd)
                priority_q.insert(lbnd, p, newsite.distance(p))

            # create a new Halfedge, setting its pm field to 1
            # insert the new Halfedge to the right of the original bisector
            lbnd = bisector
            bisector = Halfedge(edge, Edge.RE)
            edge_list.insert(lbnd, bisector)

            # if this new bisector intersects with the right Halfedge
            p = bisector.intersect(rbnd)
            if p is not None:
                # push the Halfedge into the ordered linked list of vertices
                priority_q.insert(bisector, p, newsite.distance(p))

            newsite = site_iter.next()

        elif not priority_q.is_empty():
            # intersection is smallest - this is a vector (circle) event

            # pop the Halfedge with the lowest vector off the ordered list of
            # vectors.  Get the Halfedge to the left and right of the above HE
            # and also the Halfedge to the right of the right HE
            lbnd = priority_q.pop_min_halfedge()
            llbnd = lbnd.left
            rbnd = lbnd.right
            rrbnd = rbnd.right

            # get the Site to the left of the left HE and to the right of
            # the right HE which it bisects
            bot = lbnd.leftreg(bottomsite)
            top = rbnd.rightreg(bottomsite)

            # output the triple of sites, stating that a circle goes through them
            mid = lbnd.rightreg(bottomsite)
            context.out_triple(bot, top, mid)

            # get the vertex that caused this event and set the vertex number
            # couldn't do this earlier since we didn't know when it would be processed
            v = lbnd.vertex
            site_list.set_site_number(v)
            context.out_vertex(v)

            # set the endpoint of the left and right Halfedge to be this vector
            if lbnd.edge.set_endpoint(lbnd.pm, v):
                context.out_edge(lbnd.edge)

            if rbnd.edge.set_endpoint(rbnd.pm, v):
                context.out_edge(rbnd.edge)

            # delete the lowest HE, remove all vertex events to do with the
            # right HE and delete the right HE
            edge_list.delete(lbnd)
            priority_q.delete(rbnd)
            edge_list.delete(rbnd)

            # if the site to the left of the event is higher than the Site
            # to the right of it, then swap them and set 'pm' to RIGHT
            pm = Edge.LE
            if bot.y > top.y:
                bot, top = top, bot
                pm = Edge.RE

            # Create an Edge (or line) that is between the two Sites.  This
            # creates the formula of the line, and assigns a line number to it
            edge = Edge.bisect(bot, top)
            context.out_bisector(edge)

            # create a HE from the edge
            bisector = Halfedge(edge, pm)

            # insert the new bisector to the right of the left HE
            # set one endpoint to the new edge to be the vector point 'v'
            # If the site to the left of this bisector is higher than the right
            # Site, then this endpoint is put in position 0; otherwise in pos 1
            edge_list.insert(llbnd, bisector)
            if edge.set_endpoint(Edge.RE - pm, v):
                context.out_edge(edge)

            # if left HE and the new bisector don't intersect, then delete
            # the left HE, and reinsert it
            p = llbnd.intersect(bisector)
            if p is not None:
                priority_q.delete(llbnd)
                priority_q.insert(llbnd, p, bot.distance(p))

            # if right HE and the new bisector don't intersect, then reinsert it
            p = bisector.intersect(rrbnd)
            if p is not None:
                priority_q.insert(bisector, p, bot.distance(p))
        else:
            break

    he = edge_list.leftend.right
    while he is not edge_list.rightend:
        context.out_edge(he.edge)
        he = he.right


# ------------------------------------------------------------------
def is_equal(a, b, relative_error=TOLERANCE):
    # is nearly equal to within the allowed relative error
    norm = max(abs(a), abs(b))
    return (norm < relative_error) or (abs(a - b) < (relative_error * norm))


# ------------------------------------------------------------------
class Site:
    def __init__(self, x=0.0, y=0.0, sitenum=0):
        self.x = x
        self.y = y
        self.sitenum = sitenum

    def dump(self):
        print(f'Site #{self.sitenum} ({self.x}, {self.y})')

    def __cmp__(self, other):
        if self.y < other.y:
            return -1
        elif self.y > other.y:
            return 1
        elif self.x < other.x:
            return -1
        elif self.x > other.x:
            return 1
        else:
            return 0

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)


# ------------------------------------------------------------------
class Edge:
    LE = 0
    RE = 1
    EDGE_NUM = 0
    DELETED = {}  # marker value

    def __init__(self):
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0
        self.ep = [None, None]
        self.reg = [None, None]
        self.edgenum = 0

    def dump(self):
        print(f'(#{self.edgenum} a={self.a}, b={self.b}, c={self.c})')
        print(f'ep {self.ep}')
        print(f'reg {self.reg}')

    def set_endpoint(self, lr_flag, site):
        self.ep[lr_flag] = site
        if self.ep[Edge.RE - lr_flag] is None:
            return False
        return True

    @staticmethod
    def bisect(s1, s2):
        newedge = Edge()
        newedge.reg[0] = s1  # store the sites that this edge is bisecting
        newedge.reg[1] = s2

        # to begin with, there are no endpoints on the bisector - it goes to infinity
        # ep[0] and ep[1] are None

        # get the difference in x dist between the sites
        dx = float(s2.x - s1.x)
        dy = float(s2.y - s1.y)
        adx = abs(dx)  # make sure that the difference in positive
        ady = abs(dy)

        # get the slope of the line
        newedge.c = float(s1.x * dx + s1.y * dy + (dx * dx + dy * dy) * 0.5)
        if adx > ady:
            # set formula of line, with x fixed to 1
            newedge.a = 1.0
            newedge.b = dy / dx
            newedge.c /= dx
        else:
            # set formula of line, with y fixed to 1
            newedge.b = 1.0
            newedge.a = dx / dy
            newedge.c /= dy

        newedge.edgenum = Edge.EDGE_NUM
        Edge.EDGE_NUM += 1
        return newedge


# ------------------------------------------------------------------
class Halfedge:
    def __init__(self, edge=None, pm=Edge.LE):
        self.left = None  # left Halfedge in the edge list
        self.right = None  # right Halfedge in the edge list
        self.qnext = None  # priority queue linked list pointer
        self.edge = edge  # edge list Edge
        self.pm = pm
        self.vertex = None  # Site()
        self.ystar = BIG_FLOAT

    def dump(self):
        print('Halfedge--------------------------')
        print('left: {self.left}')
        print('right: {self.right}')
        print('edge: {self.edge}')
        print('pm: {self.pm}')
        print('vertex: ', end='')
        if self.vertex:
            self.vertex.dump()
        else:
            print('None')
        print('ystar: {self.ystar}')

    def __cmp__(self, other):
        if self.ystar > other.ystar:
            return 1
        elif self.ystar < other.ystar:
            return -1
        elif self.vertex.x > other.vertex.x:
            return 1
        elif self.vertex.x < other.vertex.x:
            return -1
        else:
            return 0

    def leftreg(self, default):
        if not self.edge:
            return default
        elif self.pm == Edge.LE:
            return self.edge.reg[Edge.LE]
        else:
            return self.edge.reg[Edge.RE]

    def rightreg(self, default):
        if not self.edge:
            return default
        elif self.pm == Edge.LE:
            return self.edge.reg[Edge.RE]
        else:
            return self.edge.reg[Edge.LE]

    # returns True if p is to right of halfedge self
    def is_point_right_of(self, pt):
        e = self.edge
        topsite = e.reg[1]
        right_of_site = pt.x > topsite.x

        if right_of_site and self.pm == Edge.LE:
            return True

        if not right_of_site and self.pm == Edge.RE:
            return False

        if e.a == 1.0:
            dyp = pt.y - topsite.y
            dxp = pt.x - topsite.x
            fast = 0
            if (not right_of_site and e.b < 0.0) or (right_of_site and e.b >= 0.0):
                above = dyp >= e.b * dxp
                fast = above
            else:
                above = pt.x + pt.y * e.b > e.c
                if e.b < 0.0:
                    above = not above
                if not above:
                    fast = 1
            if not fast:
                dxs = topsite.x - (e.reg[0]).x
                above = e.b * (dxp * dxp - dyp * dyp) < dxs * \
                    dyp * (1.0 + 2.0 * dxp / dxs + e.b * e.b)
                if e.b < 0.0:
                    above = not above
        else:  # e.b == 1.0
            yl = e.c - e.a * pt.x
            t1 = pt.y - yl
            t2 = pt.x - topsite.x
            t3 = yl - topsite.y
            above = t1 * t1 > t2 * t2 + t3 * t3

        if self.pm == Edge.LE:
            return above
        else:
            return not above

    # --------------------------
    # create a new site where the Halfedges el1 and el2 intersect
    def intersect(self, other):
        e1 = self.edge
        e2 = other.edge
        if (e1 is None) or (e2 is None):
            return None

        # if the two edges bisect the same parent return None
        if e1.reg[1] is e2.reg[1]:
            return None

        d = e1.a * e2.b - e1.b * e2.a
        if is_equal(d, 0.0):
            return None

        xint = (e1.c * e2.b - e2.c * e1.b) / d
        yint = (e2.c * e1.a - e1.c * e2.a) / d
        if cmp(e1.reg[1], e2.reg[1]) < 0:
            he = self
            e = e1
        else:
            he = other
            e = e2

        right_of_site = xint >= e.reg[1].x
        if (right_of_site and he.pm == Edge.LE) or (not right_of_site and he.pm == Edge.RE):
            return None

        # create a new site at the point of intersection - this is a new
        # vector event waiting to happen
        return Site(xint, yint)


# ------------------------------------------------------------------
class EdgeList:
    def __init__(self, xmin, xmax, nsites):
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        self.hashsize = int(2 * math.sqrt(nsites + 4))

        self.xmin = xmin
        self.deltax = float(xmax - xmin)
        self.hash = [None] * self.hashsize

        self.leftend = Halfedge()
        self.rightend = Halfedge()
        self.leftend.right = self.rightend
        self.rightend.left = self.leftend
        self.hash[0] = self.leftend
        self.hash[-1] = self.rightend

    def insert(self, left, he):
        he.left = left
        he.right = left.right
        left.right.left = he
        left.right = he

    def delete(self, he):
        he.left.right = he.right
        he.right.left = he.left
        he.edge = Edge.DELETED

    # Get entry from hash table, pruning any deleted nodes
    def gethash(self, b):
        if b < 0 or b >= self.hashsize:
            return None
        he = self.hash[b]
        if he is None or he.edge is not Edge.DELETED:
            return he

        # Hash table points to deleted half edge.  Patch as necessary.
        self.hash[b] = None
        return None

    def leftbnd(self, pt):
        # Use hash table to get close to desired halfedge
        bucket = int(((pt.x - self.xmin) / self.deltax * self.hashsize))

        if bucket < 0:
            bucket = 0

        if bucket >= self.hashsize:
            bucket = self.hashsize - 1

        he = self.gethash(bucket)
        if he is None:
            i = 1
            while True:
                he = self.gethash(bucket - i)
                if he is not None:
                    break
                he = self.gethash(bucket + i)
                if he is not None:
                    break
                i += 1

        # Now search linear list of halfedges for the corect one
        if (he is self.leftend) or (he is not self.rightend and he.isPointRightOf(pt)):
            he = he.right
            while he is not self.rightend and he.is_point_right_of(pt):
                he = he.right
            he = he.left
        else:
            he = he.left
            while he is not self.leftend and not he.is_point_right_of(pt):
                he = he.left

        # Update hash table and reference counts
        if 0 < bucket < self.hashsize - 1:
            self.hash[bucket] = he
        return he


# ------------------------------------------------------------------
class PriorityQueue:
    def __init__(self, ymin, ymax, nsites):
        self.ymin = ymin
        self.deltay = ymax - ymin
        self.hashsize = int(4 * math.sqrt(nsites))
        self.count = 0
        self.minidx = 0
        self.hash = []
        for i in range(self.hashsize):
            self.hash.append(Halfedge())

    def __len__(self):
        return self.count

    def is_empty(self):
        return self.count == 0

    def insert(self, he, site, offset):
        he.vertex = site
        he.ystar = site.y + offset
        last = self.hash[self.get_bucket(he)]
        next = last.qnext
        while (next is not None) and cmp(he, next) > 0:
            last = next
            next = last.qnext
        he.qnext = last.qnext
        last.qnext = he
        self.count += 1

    def delete(self, he):
        if he.vertex is not None:
            last = self.hash[self.get_bucket(he)]
            while last.qnext is not he:
                last = last.qnext
            last.qnext = he.qnext
            self.count -= 1
            he.vertex = None

    def get_bucket(self, he):
        bucket = int(((he.ystar - self.ymin) / self.deltay) * self.hashsize)
        if bucket < 0:
            bucket = 0
        if bucket >= self.hashsize:
            bucket = self.hashsize - 1
        if bucket < self.minidx:
            self.minidx = bucket
        return bucket

    def get_min_pt(self):
        while self.hash[self.minidx].qnext is None:
            self.minidx += 1
        he = self.hash[self.minidx].qnext
        x = he.vertex.x
        y = he.ystar
        return Site(x, y)

    def pop_min_halfedge(self):
        curr = self.hash[self.minidx].qnext
        self.hash[self.minidx].qnext = curr.qnext
        self.count -= 1
        return curr


# ------------------------------------------------------------------
class SiteList:
    def __init__(self, point_list):
        self.__sites = []
        self.__sitenum = 0

        self.__xmin = point_list[0].x
        self.__ymin = point_list[0].y
        self.__xmax = point_list[0].x
        self.__ymax = point_list[0].y
        for i, pt in enumerate(point_list):
            self.__sites.append(Site(pt.x, pt.y, i))
            if pt.x < self.__xmin:
                self.__xmin = pt.x
            if pt.y < self.__ymin:
                self.__ymin = pt.y
            if pt.x > self.__xmax:
                self.__xmax = pt.x
            if pt.y > self.__ymax:
                self.__ymax = pt.y
        self.__sites.sort()

    def set_site_number(self, site):
        site.sitenum = self.__sitenum
        self.__sitenum += 1

    class Iterator:
        def __init__(self, lst):
            self.generator = (s for s in lst)

        def __iter__(self):
            return self

        def next(self):
            try:
                return self.generator.next()
            except StopIteration:
                return None

    def iterator(self):
        return SiteList.Iterator(self.__sites)

    def __iter__(self):
        return SiteList.Iterator(self.__sites)

    def __len__(self):
        return len(self.__sites)

    def _getxmin(self):
        return self.__xmin

    def _getymin(self):
        return self.__ymin

    def _getxmax(self):
        return self.__xmax

    def _getymax(self):
        return self.__ymax

    xmin = property(_getxmin)
    ymin = property(_getymin)
    xmax = property(_getxmax)
    ymax = property(_getymax)


# ------------------------------------------------------------------
def compute_voronoi_diagram(points):
    """ Takes a list of point objects (which must have x and y fields).
        Returns a 3-tuple of:

           (1) a list of 2-tuples, which are the x,y coordinates of the 
               Voronoi diagram vertices
           (2) a list of 3-tuples (a,b,c) which are the equations of the
               lines in the Voronoi diagram: a*x + b*y = c
           (3) a list of 3-tuples, (l, v1, v2) representing edges of the 
               Voronoi diagram.  l is the index of the line, v1 and v2 are
               the indices of the vetices at the end of the edge.  If 
               v1 or v2 is -1, the line extends to infinity.
    """
    site_list = SiteList(points)
    context = Context()
    voronoi(site_list, context)
    return context.vertices, context.lines, context.edges


# ------------------------------------------------------------------
def compute_delaunay_triangulation(points):
    """ Takes a list of point objects (which must have x and y fields).
        Returns a list of 3-tuples: the indices of the points that form a
        Delaunay triangle.
    """
    site_list = SiteList(points)
    context = Context()
    context.triangulate = True
    voronoi(site_list, context)
    return context.triangles
