import math
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock
from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from networkx import DiGraph
from scipy import spatial

from data.Ant import Ant


# euclidean distance between two cells
def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


class PheromoneField:

    def __init__(self, pixels: Tuple[int, int, int], graph: DiGraph, decreaseByConstant, decreaseValue, p, threshold,
                 maxUpdateDistance, path_exp):
        self.field = np.zeros(pixels)
        self.g = graph
        self.decreaseByConstant = decreaseByConstant
        self.decreaseValue = decreaseValue
        self.p = p
        self.t = threshold
        self.maxUpdateDistance = maxUpdateDistance
        self.path_exp = path_exp

        self.diff_matrix_lock = Lock()
        self.diff_matrix = np.zeros(self.field.shape)

        self.columns, self.rows, self.numtypes = self.field.shape

    def get_rectangle(self):
        # xmin, ymin, xmax, ymax
        return 0, 0, self.columns - 1, self.rows - 1

    def ant_walk_loop(self, ant: Ant):
        while not ant.reachedGoal():
            self.antWalk(ant)
        # print('processed: ' + str(ant.goal))


    # Generate a pheromone field in r runs, where each run all edges are traversed by one ant
    def buildField(self, r):
        for run in range(r):
            print("run: ", run)
            ants = []
            with ThreadPoolExecutor() as executor:
                for e in self.g.edges:
                    # For each edge, create an ant and let it walk until it reaches its goal
                    ant = self.initializeEdge(e)
                    ants.append(ant)
                    executor.submit(self.ant_walk_loop, ant)

                # Wait for ants to finish walking
                executor.shutdown(wait=True)

            # print("All ants completed walk")
            # Update the field with the new found paths

            self.diff_matrix = np.zeros(self.field.shape)

            with ThreadPoolExecutor() as executor:
                for ant in ants:
                    executor.submit(self.updateField, ant.path, ant.start_index, ant.end_index)

                executor.shutdown(wait=True)

            self.field += self.diff_matrix

            # Evaporate value of all fields such that bad paths will eventually disappear
            self.evaporate()

    # Return an ant that walks along the given edge
    def initializeEdge(self, edge) -> Ant:
        return Ant((self.g.nodes[edge[0]]['x'], self.g.nodes[edge[0]]['y']),
                   (self.g.nodes[edge[1]]['x'], self.g.nodes[edge[1]]['y']), edge[0], edge[1])

    # Calculate the new direction for an individual ant
    def antWalk(self, ant: Ant):
        neighbours = self.getCandidateNeighbours(ant)
        # If only one neighbour is valid, walk to that pixel
        if len(neighbours) == 1:
            newDirec = ant.calcAngle(neighbours[0]) - ant.direction
        elif ant.goal in neighbours:
            newDirec = ant.calcAngle(ant.goal) - ant.direction
        else:
            newDirec = None
            while newDirec is None or not self.is_valid_location(*ant.calcPixel(ant.direction + newDirec)):
                # With chance p we either get a random directional change, or a pheromone based directional change
                rand = np.random.uniform(0, 1)
                if rand < self.p:
                    newDirec = self.randomDirectionalChange()
                else:
                    newDirec = self.pheromoneBasedDirection(neighbours, ant)

        # Update the ant's new direction
        ant.updateDirection(newDirec)
        # Let the ant take a step
        ant.takeStep()

    def is_valid_location(self, x, y):
        return 0 <= x < self.columns and 0 <= y < self.rows

    # Update values of field using the given path
    def updateField(self, path, start_index, end_index):
        path = np.array(path)
        update_indices = np.array(path)
        # find relevant indices to update
        directions = ([0, 1], [0, -1], [1, 0], [-1, 0])
        for direction in np.array(directions):
            for i in range(1, self.maxUpdateDistance + 1):
                update_indices = np.vstack([update_indices, path + i * direction])

        # find relevant indices around start and end points
        ball_offsets = list(range(-self.maxUpdateDistance, self.maxUpdateDistance + 1))
        ball_offsets.remove(0)
        ball_vectors = np.array(np.meshgrid(ball_offsets, ball_offsets)).T.reshape(-1, 2)
        for p in [path[0], path[-1]]:
            for ball_vector in ball_vectors:
                update_indices = np.vstack([update_indices, p + ball_vector])

        # remove duplicate vectors
        update_indices = np.unique(update_indices, axis=0)

        # remove out of bounds indices
        # - No index can ever be negative
        update_indices = update_indices[~(update_indices < 0).any(axis=1)]
        x_mask = update_indices[:, 0] < self.columns
        update_indices = update_indices[x_mask]
        y_mask = update_indices[:, 1] < self.rows
        update_indices = update_indices[y_mask]

        # lexicographical sort
        update_indices = update_indices[np.lexsort(update_indices.T[::-1])]

        # compute the distance from the relevant indices to the path
        distances = spatial.distance.cdist(update_indices, np.array(path)).min(axis=1)

        # apply path diffuse function
        path_constant = self.getPathUpdateConstant(path)
        distances = path_constant * np.exp(-distances ** 2 / (2 * (self.maxUpdateDistance / 3) ** 2))

        # create the difference matrix which will store the matrix added to the pheromone field
        diff_matrix = np.zeros(self.field.shape[:2])

        # put distance at correct position by raveling the indices
        flat_index_array = np.ravel_multi_index(update_indices.T, diff_matrix.shape)
        np.ravel(diff_matrix)[flat_index_array] = distances

        # add type axis
        diff_matrix = np.repeat(diff_matrix[:, :, np.newaxis], self.numtypes, axis=2)

        # filter unmodified types
        diff_matrix[:, :, ~np.isin(np.arange(self.numtypes), [start_index, end_index])] = 0

        self.diff_matrix_lock.acquire()
        self.diff_matrix += diff_matrix
        self.diff_matrix_lock.release()

    def getPathUpdateConstant(self, path):
        return (euclidean(path[0], path[-1]) / self.getPathLength(path)) ** self.path_exp

    def getPathLength(self, path):
        s = 0
        for i in range(len(path) - 1):
            s = s + euclidean(path[i], path[i + 1])
        return s

    # Evaporate field values after a run
    def evaporate(self):
        # Depending on whether the user choose a constant value decrease, or multiplying by a factor between (0, 1)
        if (self.decreaseByConstant):
            self.field = self.field - self.decreaseValue
            self.field[self.field < 0] = 0
        else:
            self.field = self.field * self.decreaseValue

    # Take random new directional change
    def randomDirectionalChange(self) -> float:
        return np.random.normal(0, math.pi / 6)

    # Calculate directional change based on neighbours
    def pheromoneBasedDirection(self, neighbours, ant) -> float:
        # Calculate left and right antenna pixels and their values
        l = ant.getLeftAntenna()
        r = ant.getRightAntenna()

        fLeft, fRight = 0, 0

        if l in neighbours:
            fLeft = sum(self.field[l])

        if r in neighbours:
            fRight = sum(self.field[r])

        if l in neighbours and r in neighbours:
            if fLeft == 0 and fRight == 0:
                if sum(self.field[ant.location]) > 0:
                    # If both are 'bad' neighbours and we are on a path with a high pheromone value, continue walking
                    return 0
                else:
                    # If both are 'bad' neighbours and we are on a 'bad' path, take a random directional change
                    return np.random.normal(0, math.pi / 6)

            # If both antenna are our neighbours but the difference in their values is too small, random change
            elif math.fabs(fLeft - fRight) < self.t:
                return np.random.normal(0, math.pi / 6)
            else:
                # Else, both antenna are neighbours but their value difference is large enough
                rand = np.random.uniform(0, fLeft ** 4 + fRight ** 4)
                # Go left or right, depending on the pheromone values of l and r
                return (-1 if rand < fLeft ** 4 else 1) * math.pi / 4

        # If only l is a neighbour, go left
        elif l in neighbours and not r in neighbours:
            return math.pi / 4

        # If only r is a neighbour, go right
        elif not l in neighbours and r in neighbours:
            return -math.pi / 4

        # If neither are neighbours, pick a random directional change
        else:
            return np.random.normal(0, math.pi / 6)

    def getCandidateNeighbours(self, ant) -> list:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.is_valid_location(ant.location[0] + i, ant.location[1] + j) and not (i == 0 and j == 0):
                    neighbours.append((ant.location[0] + i, ant.location[1] + j))

        trail = ant.path[:10]
        # Only use neighbours that have not been visited before
        nvisited = [x for x in neighbours if x not in trail]
        if not nvisited:
            return neighbours

        # Only consider neighbours that are not further away from the goal
        angleEnd = ant.calcAngle(ant.goal)
        # TODO: optimize using modulo operation instead of arctan
        nborder = [x for x in nvisited if -math.pi * 3 / 4 < math.atan2(math.sin(angleEnd - ant.calcAngle(x)), math.cos(
            angleEnd - ant.calcAngle(x))) < math.pi * 3 / 4]
        if not nborder:
            return nvisited

        # Only consider neighbours that make sharp turns w.r.t. our current position
        nfinal = [x for x in nborder if -math.pi / 2 <= math.atan2(math.sin(ant.direction - ant.calcAngle(x)), math.cos(
            ant.direction - ant.calcAngle(x))) <= math.pi / 2]
        if not nfinal:
            return nborder
        return nfinal

    def plot(self, cm='viridis', log_scale=True):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        acc_field = self.field.sum(axis=-1).T
        if log_scale:
            acc_field = np.log1p(acc_field)
        im = plt.imshow(acc_field, interpolation='nearest', cmap=plt.cm.get_cmap(cm), origin='lower')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)

        plt.colorbar(im, cax=cax)
        plt.show()
