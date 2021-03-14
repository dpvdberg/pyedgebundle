from typing import Tuple, List

from algorithms.BundleAlgorithm import BundleAlgorithm
from data.PheromoneField import PheromoneField
from networkx import DiGraph
from bresenham import bresenham
import numpy as np

# Edge bundling algorithm that performs edge bundling based on ant colony optimization
from parser.GraphUtils import GraphUtils
from util.LineUtils import LineUtils


class AntBundleAlgorithm(BundleAlgorithm):

    def __init__(self, graph: DiGraph, runs, segments, decreaseByConstant, decreaseValue, p, threshold,
                 maxUpdateDistance):
        self.graph = graph
        self.field = PheromoneField(
            GraphUtils.getGraphFieldShape(self.graph), self.graph, decreaseByConstant, decreaseValue, p, threshold,
            maxUpdateDistance)
        self.r = runs
        self.segments = segments

    # Bundle edges in the given graph and return a BundledGraph object
    def bundle(self):
        self.field.buildField(self.r)
        curve_points = self.createCurvePoints()
        # todo: interpolate points and create bundledgraph

    def rasterizeEdge(self, edge) -> np.ndarray:
        start, end = edge
        p1 = self.graph.nodes[start]['x'], self.graph.nodes[start]['y']
        p2 = self.graph.nodes[end]['x'], self.graph.nodes[end]['y']
        # Use the Bresenham algorithm to rasterize a straight line
        return LineUtils.rasterize_line(p1, p2)

    def perpendicularWeightedMean(self, perpendicular_line, p, start_index, end_index):
        line_size, _ = perpendicular_line.shape

        # The sum of pheromone values of start and end type, weighted w.r.t. the distance to starting point p
        weighted_ps = 0
        # The sum of pheromone values of start and end type
        ps = 0

        relative_perpendicular = perpendicular_line - p
        for q in range(line_size):
            pheromone = self.field.field[tuple(perpendicular_line[q])][start_index] \
                        + self.field.field[tuple(perpendicular_line[q])][end_index]
            pheromone_exp = pheromone ** 8
            ps += pheromone_exp

            weighted_ps += relative_perpendicular[q] * pheromone_exp

        return p + np.round(weighted_ps / ps)

    # Create and return a BundledGraph with curved edges based on the given Pheromone field
    def createCurvePoints(self) -> List[List[np.ndarray]]:
        curves = []
        for e in self.graph.edges():
            start_node_index, end_node_index = e

            field_line = self.rasterizeEdge(e)
            start_point = field_line[0]
            end_point = field_line[-1]

            # The starting point is always part of the curve
            curve_points = [start_point]
            point_count, _ = field_line.shape
            segment_point_count = int(point_count / self.segments)

            for segment in range(1, self.segments):
                segment_point_index = segment_point_count * segment
                p = field_line[segment_point_index]
                # Get the start and end points on the perpendicular line through p
                start_perp, end_perp = LineUtils.get_perpendicular_points(p, np.array([start_point, end_point]))
                # Extend the perpendicular line to the field bounds
                start_perp_ext, end_perp_ext = LineUtils.extend(self.field.get_rectangle(), start_perp, end_perp)
                # Rasterize the perpendicular line
                perp_line = LineUtils.rasterize_line(start_perp_ext, end_perp_ext)

                c = self.perpendicularWeightedMean(perp_line, p, start_node_index, end_node_index)

                curve_points.append(c)

            curve_points.append(end_point)
            curves.append(curve_points)

        return curves
