import math
import random
from qubots.base_problem import BaseProblem
import os

class SmallestCircleProblem(BaseProblem):
    """
    Given a set of points in the plane, find the circle with the minimal radius that contains all the points.

    Instance file format:
      - The first token is an integer representing the number of points.
      - Then for each point, two numbers (x and y coordinates) are provided.
    
    Decision Variables:
      - A list of two floats [x, y] representing the coordinates of the circle's center.
        The domain of x is set to [min_x, max_x] and y to [min_y, max_y],
        where these bounds are computed from the instance data.
    
    Objective:
      - Minimize the radius of the circle, where the radius is computed as:
          r = max_{point in instance} sqrt((x - x_i)^2 + (y - y_i)^2)
    """

    def __init__(self, instance_file):
        self.instance_file = instance_file
        self._load_instance(instance_file)

    def _load_instance(self, filename):

        # Resolve relative path with respect to this module’s directory.
        if not os.path.isabs(filename):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir, filename)

        with open(filename, "r") as f:
            tokens = f.read().split()
        # First token: number of points
        self.nb_points = int(tokens[0])
        self.points = []
        idx = 1
        for i in range(self.nb_points):
            x = float(tokens[idx])
            y = float(tokens[idx + 1])
            self.points.append((x, y))
            idx += 2
        # Compute bounding box for the points
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        self.min_x = min(xs)
        self.max_x = max(xs)
        self.min_y = min(ys)
        self.max_y = max(ys)

    def evaluate_solution(self, candidate) -> float:
        """
        Evaluate a candidate solution.

        Parameters:
          candidate: A list of two floats [x, y] representing the center of the circle.

        Returns:
          The radius required to enclose all points.
        """
        if len(candidate) != 2:
            raise ValueError("Candidate solution must have exactly two values: [x, y].")
        x_center, y_center = candidate
        max_sq_dist = 0.0
        for (xi, yi) in self.points:
            dx = x_center - xi
            dy = y_center - yi
            sq_dist = dx * dx + dy * dy
            if sq_dist > max_sq_dist:
                max_sq_dist = sq_dist
        return math.sqrt(max_sq_dist)

    def random_solution(self):
        """
        Generate a random candidate solution.
        x is sampled uniformly from [min_x, max_x] and y from [min_y, max_y].
        """
        x_rand = random.uniform(self.min_x, self.max_x)
        y_rand = random.uniform(self.min_y, self.max_y)
        return [x_rand, y_rand]
