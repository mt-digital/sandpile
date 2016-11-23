import numpy as np
import progressbar

from random import randint


def run_sandpile_experiment(width, num_iter):

    pile = np.zeros((width, width), dtype='i4')

    drop_coords = ((randint(0, width - 1), randint(0, width - 1))
                   for _ in range(num_iter))

    pile_series = []
    avalanche_series = []

    bar = progressbar.ProgressBar(max_value=num_iter)

    for coord in bar(drop_coords):

        avalanche_count = 0

        val = pile[coord]

        if val < 3:
            pile[coord] += 1

        elif val == 3:

            # initialize a list to keep track of sources of avalanches
            # or other coordinates that have already been processed
            prev_coords = [coord]

            pile[coord] = 0
            neighbors = coord_neighbors(coord)

            avalanche_count += 1

            while neighbors:

                new_neighbors = []

                for neighbor in neighbors:

                    if (valid_coord(neighbor, width) and
                            neighbor not in prev_coords):

                        val = pile[neighbor]

                        if val < 3:
                            pile[neighbor] += 1

                            prev_coords.append(neighbor)

                        elif val == 3:

                            pile[neighbor] = 0
                            prev_coords.append(neighbor)
                            new_neighbors.extend(coord_neighbors(neighbor))
                            avalanche_count += 1

                neighbors = new_neighbors

        pile_series.append(pile)
        avalanche_series.append(avalanche_count)

    return Experiment(avalanche_series, pile_series)


class Experiment:

    avalanche_series = None
    pile_series = None

    def __init__(self, avalanche_series, pile_series):
        self.avalanche_series = avalanche_series
        self.pile_series = pile_series


def valid_coord(coord, width):
    return not (coord[0] < 0 or coord[1] < 0 or
                coord[0] >= width or coord[1] >= width)


def coord_neighbors(coord):

    top = (coord[0], coord[1] + 1)
    bottom = (coord[0], coord[1] - 1)
    right = (coord[0] + 1, coord[1])
    left = (coord[0] - 1, coord[1])

    return [top, bottom, right, left]
