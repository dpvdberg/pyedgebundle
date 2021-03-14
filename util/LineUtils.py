import numpy as np
from bresenham import bresenham


class LineUtils:
    @staticmethod
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    @staticmethod
    def in_rectangle(rectangle, point):
        xmin, ymin, xmax, ymax = rectangle
        x, y = point
        return xmin <= x <= xmax and ymin <= y <= ymax

    @staticmethod
    def get_perpendicular_points(pivot: np.ndarray, points: np.ndarray):
        # pivot w.r.t. pivot points
        pivoted_points = points - pivot
        # flip X and Y coordinates
        transposed_points = np.fliplr(pivoted_points)
        # change sign of the first coordinate
        transposed_points[:, 0] = -transposed_points[:, 0]
        # pivot back
        perpendicular_points = transposed_points + pivot

        return perpendicular_points

    @staticmethod
    def extend(rectangle, p1, p2):
        xmin, ymin, xmax, ymax = rectangle
        x1, y1 = p1
        x2, y2 = p2

        if y1 == y2:
            if x1 > x2:
                return (xmax, y1), (xmin, y2)
            else:
                return (xmin, y1), (xmax, y2)
        if x1 == x2:
            if y1 > y2:
                return (x1, ymax), (x2, ymin)
            else:
                return (x1, ymin), (x2, ymax)

        # The lines should now intersect
        left = ((xmin, ymin), (xmin, ymax))
        right = ((xmax, ymin), (xmax, ymax))
        top = ((xmin, ymax), (xmax, ymax))
        bottom = ((xmin, ymin), (xmax, ymin))

        line = ((x1, y1), (x2, y2))

        ileft = LineUtils.line_intersection(left, line)
        iright = LineUtils.line_intersection(right, line)
        itop = LineUtils.line_intersection(top, line)
        ibottom = LineUtils.line_intersection(bottom, line)

        intersections = [ileft, iright, itop, ibottom]
        valid_intersections = {(int(i[0]), int(i[1])) for i in intersections if LineUtils.in_rectangle(rectangle, i)}

        assert len(valid_intersections) == 2, "An extended line should collide with two points in the rectangle"

        # return in correct order
        ifirst, isecond = valid_intersections
        il, ir = (ifirst, isecond) if ifirst[0] < isecond[0] else (isecond, ifirst)
        if x1 < x2:
            return il, ir
        else:
            return ir, il

    @staticmethod
    def rasterize_line(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return np.array(list(bresenham(x1, y1, x2, y2)))
