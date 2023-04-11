import math
import numpy as np
from templates import templates as default_templates

EPSILON = 0.5

def get_distance(points):
    #reused this method from $1 pre-processing
    """
    Utility method to get distance b/w 2 points
    :param points: array of points
    :return: dist b/w 2 points within the array
    """

    dist_x = (points[1][0] - points[0][0]) ** 2
    dist_y = (points[1][1] - points[0][1]) ** 2
    dist = math.sqrt(dist_x + dist_y)
    return dist


def get_path_length(points):
    #reused this method from $1 pre-processing

    """
    Utility method to calculate total path length from all points of user's gesture
    :param points: array of points retrieved from user's gesture
    :return: Total path length of all points
    """

    path_length = 0
    n = len(points)
    for i in range(n - 1):
        curr_point = points[i]
        next_point = points[i + 1]
        dist = get_distance([curr_point, next_point])
        path_length = path_length + dist

    return path_length

def scale(points):
    #reused this method from $1 pre-processing
    """
    Method to scale the points
    :param points: array of coordinates , size of the square.
    :param square_size: size of the bounding box to be scaled to
    :return: new points as an array after scaling
    """
    maximum_x, maximum_y = np.max(points, 0)
    minimum_x, minimum_y = np.min(points, 0)

    box_width = maximum_x - minimum_x
    box_height = maximum_y - minimum_y

    new_points = np.zeros((1, 2))

    for point in points:
        q = np.array([0., 0.])
        q[0] = point[0] * (square_size / box_width)
        q[1] = point[1] * (square_size / box_height)
        new_points = np.append(new_points, [q], 0)

    return new_points[1:]
def get_centroid(points):
    #reused from $1 pre-processing
    """
    Utility method to get centroid of points
    :param points: array of coordinates
    :return: x, y coordinate of centroid
    """

    n = len(points)
    # sum_x = 0
    # sum_y = 0
    # for point in points:
    #     sum_x = sum_x + point[0]
    #     sum_y = sum_y + point[1]
    temp_points = np.array(points)
    sum_x_coords = np.sum(temp_points[:, 0])
    sum_y_coords = np.sum(temp_points[:, 1])

    # return sum_x / n, sum_y / n
    return sum_x_coords / n, sum_y_coords / n
def translate_to_origin(points, n):
    #reused this method from $1 pre-processing
    #needs to be changed
    centroid_x, centroid_y = get_centroid(np.array(points))
    new_points = np.zeros((1, 2))

    for point in points:
        q = np.array([0., 0.])
        q[0] = point[0] - centroid_x
        q[1] = point[1] - centroid_y
        new_points = np.append(new_points, [q], 0)

    return new_points[1:]
def resample(points, n):
    #reused this method from $1 pre-processing

    """
    Method to execute 1st step of preprocessing for $1 recogniser. Resample points array to have consistent
    number of points
    :param points: All points identified from user's gesture
    :param n: Size of points array
    :return: new_points array after applying Resampling step.
    """

    path_length = get_path_length(points)
    length = path_length / (n - 1)
    d = 0
    temp_points = list(points[:])
    new_points = [points[0]]
    i = 1
    while i < len(temp_points):
        prev_point = temp_points[i - 1]
        curr_point = temp_points[i]
        dist = get_distance([prev_point, curr_point])
        if (d + dist) >= length:
            qx = temp_points[i - 1][0] + ((length - d) / dist) * (temp_points[i][0] - temp_points[i - 1][0])
            qy = temp_points[i - 1][1] + ((length - d) / dist) * (temp_points[i][1] - temp_points[i - 1][1])
            new_points.append([qx, qy])
            temp_points.insert(i, [qx, qy])
            d = 0
        else:
            d = d + dist
        i = i + 1

    # Check if size of new array is exactly equal to required n. If not add the last point again to the array
    if len(new_points) < n:
        new_points.append([new_points[-1][0], new_points[-1][1]])

    return new_points

def normalize(points, n):
    
    resampled_points = resample(points, n)
    scaled_points = scale(resampled_points)
    translated_points = translate_to_origin(scaled_points , n)

    return translated_points

def get_cloud_distance( points, template, n, start):

    matched_array = [False] * n
    distance_sum = 0

    i = start
    
    while True:
        minimum = float("inf")
        index = None
        j = 0
        while j < n:
            if not matched_array[j]:
                d = get_distance(points[i], template[j])
                if d < minimum:
                    minimum = d
                    index = j
            j += 1
        matched_array[index] = True

        weight = 1 - ((i - start + n) % n) / n

        distance_sum += weight * minimum
    
        i = (i + 1) % n
        if i == start:
            break
        


def greedy_cloud_match(points, template, n):

    e = EPSILON
    step = int(math.floor(n ** (1 - e)))
    minimum = float("inf")

    for i in range(0 , n , step):
        d1 = get_cloud_distance(points, template ,n , i)
        d2 = get_cloud_distance(template , points , n ,i)

        minimum = min( minimum, d1, d2)

    return minimum
def recognize(points, n = 32, templates = default_templates ):

    number_of_points = n
    points = normalize( points, n)
    score = float("inf")

    result = None

    for template in templates:
        template = normalize(points, n)

        d = greedy_cloud_match(points, template , n)

        if score > d:
            score = d
            result = template

        score = max(((2- score)//2), 0 )

        # if result == None or score == 0:
        #     return None, score
        # else:
        #     return result, score

        return result, score