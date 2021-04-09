import argparse
import csv
import os
from typing import Tuple, List

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np


class IntPoint:
    __fields__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y


def is_digit(n: str) -> bool:
    try:
        int(n)
        return True
    except ValueError:
        return False

def clamp(n, n_min, n_max):
    return max(n_min, min(n_max, n))

def is_in_range(n, n_min, n_max, *, inclusive: bool = True):
    if inclusive:
        return n_min <= n <= n_max
    else:
        return n_min < n < n_max
    

class Parsers:
    @staticmethod
    def parse_location_csv(location_data_csv: str, csv_delimiter: str = ';') -> List[Tuple[IntPoint, int]]:
        """
        Parse a location data CSV file and return a list of tuples containing locations and the velocity at that location.
        Expected format of the CSV: LocationX, LocationY, Velocity
        """
        location_data: List[Tuple[IntPoint, int]] = []

        with open(location_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=csv_delimiter)
            for row in reader:
                if is_digit(row[0]):
                    location_data.append((IntPoint(int(row[0]), int(row[1])), int(row[2])))

        return location_data
        
    @staticmethod
    def parse_bump_csv(bump_data_csv: str, csv_delimiter: str = ';') -> List[IntPoint]:
        """
        Parse a bump data CSV file and return a list locations.
        Expected format of the CSV: LocationX, LocationY
        """
        bump_data: List[IntPoint] = []

        with open(bump_data_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=csv_delimiter)
            for row in reader:
                if is_digit(row[0]):
                    bump_data.append(IntPoint(int(row[0]), int(row[1])))

        return bump_data

def create_heatmap(x, y, z, background_image: str, map_min_point: IntPoint, map_max_point: IntPoint, plot_alpha: float,
                   plot_title: str, color_bin_count: int):
    # Determine where to place ticks on the color map (i.e. how to divide the colors between different values)
    levels = MaxNLocator(nbins=color_bin_count).tick_values(z.min(), z.max())
    # Choose a color map
    cmap = plt.get_cmap('coolwarm')
    # Create a subplot
    fig, ax0 = plt.subplots(nrows=1)

    # Create a contour plot
    cont = ax0.contourf(x[:-1, :-1] + dx/2.0, y[:-1, :-1] + dy/2.0, z, levels=levels,
                  cmap=cmap, alpha=plot_alpha if os.path.exists(background_image) else 1.0)

    # Add a color bar
    fig.colorbar(cont, ax=ax0)
    ax0.set_title(plot_title)
    
    # Add a background image if it can be found
    if os.path.exists(background_image):
        img = plt.imread(background_image)
        ax0.imshow(img, extent=[map_min_point.x, map_max_point.x, map_min_point.y, map_max_point.y])

    # Show the plot
    plt.show()

def create_frequency_heatmap(data: List[IntPoint], x_grid: np.mgrid, y_grid: np.mgrid, map_min_point: IntPoint, map_max_point: IntPoint,
                             background_image: str, plot_alpha: float, plot_title: str = 'Frequency Heatmap', color_bin_count: int = 15,
                             use_log_scale: bool = True):
    """Create a heatmap based on how often a point appears in data"""
    bucket_count_x = len(x_grid) - 1
    bucket_count_y = len(x_grid[0]) - 1
    frequency = np.zeros([bucket_count_y, bucket_count_x])

    map_extents = IntPoint(map_max_point.x - map_min_point.x, map_max_point.y - map_min_point.y)
    
    for point in data:
        # Determine in which bucket the point fits and increment the count in that bucket by one
        container_x = int(((point.x - map_min_point.x) / map_extents.x) * (bucket_count_x - 1))
        container_y = int(((point.y - map_min_point.y) / map_extents.y) * (bucket_count_y - 1))
        
        # Clamp the indices to a correct range
        container_y = clamp(container_y, 0, len(frequency) - 1)
        container_x = clamp(container_x, 0, len(frequency[container_y]) - 1)

        frequency[container_y][container_x] += 1
    
    # Logarithmic scale
    if use_log_scale:
        plot_title += " (Logarithmic)"

        for y in range(len(frequency)):
            for x in range(len(frequency[y])):
                if frequency[y][x] != 0:
                    frequency[y][x] = np.log(frequency[y][x])
    
    create_heatmap(x=x_grid, y=y_grid, z=frequency, map_min_point=map_min_point, map_max_point=map_max_point,
                   background_image=background_image, plot_alpha=plot_alpha, plot_title=plot_title, color_bin_count=color_bin_count)
    

def create_average_heatmap(data: List[Tuple[IntPoint, int]], x_grid: np.mgrid, y_grid: np.mgrid, map_min_point: IntPoint, map_max_point: IntPoint,
                           background_image: str, plot_alpha: str, plot_title: str ='Average Heatmap', color_bin_count: int = 15):
    """Create a heatmap based on the average of something"""
    bucket_count_x = len(x_grid) - 1
    bucket_count_y = len(x_grid[0]) - 1
    speed = np.ndarray((bucket_count_y, bucket_count_x), dtype=np.ndarray)
    
    map_extents = IntPoint(map_max_point.x - map_min_point.x, map_max_point.y - map_min_point.y)

    for y in range(0, bucket_count_y):
        for x in range(0, bucket_count_x):
            speed[y][x] = []
    
    for val in data:
        # Determine in which bucket the point fits and append a value to the list
        container_x = int(((val[0].x - map_min_point.x) / map_extents.x) * (bucket_count_x - 1))
        container_y = int(((val[0].y - map_min_point.y) / map_extents.y) * (bucket_count_y - 1))

        # Clamp the indices to a correct range
        container_y = clamp(container_y, 0, len(speed) - 1)
        container_x = clamp(container_x, 0, len(speed[container_y]) - 1)

        speed[container_y][container_x].append(val[1])

    for y in range(0, bucket_count_y):
        for x in range(0, bucket_count_x):
            if speed[y][x]:
                speed[y][x] = np.mean(speed[y][x])
            else:
                speed[y][x] = 0.0

    create_heatmap(x=x_grid, y=y_grid, z=speed, map_min_point=map_min_point, map_max_point=map_max_point,
                   background_image=background_image, plot_alpha=plot_alpha, plot_title=plot_title, color_bin_count=color_bin_count)


if __name__ == '__main__':
    ''' Parse arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--LocationData', type=str, metavar='FILE.csv',  help='The path to the csv containing location- and speed data', default='')
    parser.add_argument('--BumpData', type=str, metavar='FILE.csv', help='The path to the csv containing bump location data', default='')
    parser.add_argument('--BackgroundImage', type=str, metavar='IMAGE.png', help='The path to an image to place behind the heatmap', default='SnowMap.png')
    parser.add_argument('--PlotAlpha', type=float, metavar='ALPHA', help='The alpha of the float, where 0 is transparent and 1 is opaque', default=0.75)
    parser.add_argument('--CsvDelimiter', type=str, metavar='DELIMITER', help='The delimiter used in the csv files', default=';')
    parser.add_argument('--HorizontalBuckets', type=int, help='The number of buckets to divide the data into on the horizontal axis. higher is more detailed, but also slower and more memory-intensive', default=100)
    parser.add_argument('--VerticalBuckets', type=int, help='The number of buckets to divide the data into on the vertical axis. higher is more detailed, but also slower and more memory-intensive', default=100)
    parser.add_argument('--MapBounds', type=int, nargs=4, metavar=('MinX', 'MaxX', 'MinY', 'MaxY'),  help='The bounds of the map', default=(-204000, 204000, -204000, 204000))
    parser.add_argument('--DiscardOutOfBounds', type=int, choices=[0, 1],  help='If 0, values that are outside of the map bounds are not discarded, but are instead counted as if they were on the edge of the map', default=1)
    parser.add_argument('--ColorBinCount', type=int, choices=range(2, 257), metavar="[2, 256]", help='The number of color bins to divide the data into', default=16)
    parser.add_argument('--UseLogScale', type=int, choices=[0, 1], help='If 1, frequency heatmaps will use a logarithmic scale', default=1)

    args = parser.parse_args()

    location_csv: str = args.LocationData
    bump_csv: str = args.BumpData
    background_image: str = args.BackgroundImage
    plot_alpha: float = args.PlotAlpha
    csv_delimiter: str = args.CsvDelimiter
    discard_out_of_bounds: bool = args.DiscardOutOfBounds != 0
    color_bin_count: int = args.ColorBinCount
    use_logarithmic_scale: bool = args.UseLogScale != 0

    # Heatmap detail (higher is more detailed, but also slower and more memory-intensive)
    bucket_count_x: int = args.HorizontalBuckets
    bucket_count_y: int = args.VerticalBuckets

    # Map bounds (of the in-game map)
    map_min_point: IntPoint = IntPoint(args.MapBounds[0], args.MapBounds[2])
    map_max_point: IntPoint = IntPoint(args.MapBounds[1], args.MapBounds[3])

    ''' Check if the path to a location- or bump data file is passed '''
    if location_csv == '' and bump_csv == '':
        print("Please provide a file path to get the data for the heatmap from!\nUse --LocationData and/or --BumpData for this.")
        exit()

    ''' Set up variables '''
    map_extents_x: int = map_max_point.x - map_min_point.x
    map_extents_y: int = map_max_point.y - map_min_point.y

    dx: int = map_extents_x / bucket_count_x
    dy: int = map_extents_y / bucket_count_y

    y_grid, x_grid = np.mgrid[slice(map_min_point.y, map_max_point.y + dy, dy),
                              slice(map_min_point.x, map_max_point.x + dx, dx)]

    ''' Generate heatmaps '''
    # Location- and speed heatmap
    if location_csv != '':
        location_data = Parsers.parse_location_csv(location_data_csv=location_csv, csv_delimiter=csv_delimiter)

        if discard_out_of_bounds:
            location_data = [l for l in location_data if is_in_range(l[0].x, map_min_point.x, map_max_point.x) and is_in_range(l[0].y, map_min_point.y, map_max_point.y)]

        create_frequency_heatmap(data=[l[0] for l in location_data], x_grid=x_grid, y_grid=y_grid, map_min_point=map_min_point,
                                map_max_point=map_max_point, background_image=background_image,
                                plot_alpha=plot_alpha, plot_title='Location Heatmap', color_bin_count=color_bin_count,
                                use_log_scale=use_logarithmic_scale)

        create_average_heatmap(data=location_data, x_grid=x_grid, y_grid=y_grid, map_min_point=map_min_point,
                                map_max_point=map_max_point, background_image=background_image,
                                plot_alpha=plot_alpha, plot_title='Speed Heatmap', color_bin_count=color_bin_count)

    # Bump heatmap
    if bump_csv != '':
        bump_data = Parsers.parse_bump_csv(bump_csv, csv_delimiter)
        if discard_out_of_bounds:
            bump_data = [b for b in bump_data if is_in_range(b.x, map_min_point.x, map_max_point.x) and is_in_range(b.y, map_min_point.y, map_max_point.y)]

        create_frequency_heatmap(data=bump_data, x_grid=x_grid, y_grid=y_grid, map_min_point=map_min_point,
                                map_max_point=map_max_point, background_image=background_image,
                                plot_alpha=plot_alpha, plot_title='Bump Heatmap', color_bin_count=color_bin_count,
                                use_log_scale=use_logarithmic_scale)
