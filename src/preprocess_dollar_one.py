import math
import numpy as np
from numpy.linalg import linalg
from unistroke import templates


def resample_points(points, n):
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
    temp_points = points[:]
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

    # if len(new_points) < n:
    #     new_points.append([new_points[-1][0], new_points[-1][1]])

    return new_points


def rotate_to_zero(points):
    """
    Method to apply 2nd step of preprocessing. Rotate all points so that 1st point and centroid have an angle of 0.
    :param points: array of coordinates
    :return: array of coordinates after applying rotation
    """

    centroid_x, centroid_y = get_centroid(points)
    angle = math.atan2(centroid_y - points[0][1], centroid_x - points[0][0])
    new_points = rotate_by(points, -angle, [centroid_x, centroid_y])
    return new_points


def rotate_by(points, angle, centroid):
    """
    Method to rotate all points by angle
    :param points: array of coordinates
    :param angle: angle between 1st point and centroid
    :param centroid: coordinates of centroid
    :return: array of points after rotation
    """

    centroid_x = centroid[0]
    centroid_y = centroid[1]
    new_points = []
    for point in points:
        qx = (point[0] - centroid_x) * math.cos(angle) - (point[1] - centroid_y) * math.sin(angle) + centroid_x
        qy = (point[0] - centroid_x) * math.sin(angle) + (point[1] - centroid_y) * math.cos(angle) + centroid_y
        new_points.append([qx, qy])

    return new_points


def get_distance(points):
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


def get_centroid(points):
    """
    Utility method to get centroid of points
    :param points: array of coordinates
    :return: x, y coordinate of centroid
    """

    n = len(points)
    sum_x = 0
    sum_y = 0
    for point in points:
        sum_x = sum_x + point[0]
        sum_y = sum_y + point[1]

    return sum_x / n, sum_y / n


def scale_to_square(points, square_size):
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

    new_points = np.zeros((1,2))

    for point in points:
        q = np.array([0.,0.])
        q[0] = point[0] * (square_size / box_width)
        q[1] = point[1] * (square_size / box_height)
        new_points = np.append(new_points, [q], 0)
    
    return new_points[1:]


def translate_to_origin(points):
    """
    Method to translate the points to origin
    :param points: array of coordinates
    :return: new points as an array after translating to origin
    """

    centroid_x, centroid_y = get_centroid(np.array(points))
    # centroid = np.array([centroid_x,centroid_y])
    new_points = np.zeros((1, 2))

    for point in points:
        q = np.array([0.,0.])
        q[0] = point[0] - centroid_x
        q[1] = point[1] - centroid_y
        new_points = np.append(new_points, [q], 0)
    
    return new_points[1:]


def recognize(points, n, angle_range, angle_step, phi, square_size):

    """
    Method to match the set of points against the template
    :param points: array of coordinates
    :param n : number of points
    :param angle_step:
    :param angle_range:
    :param templates : all templates
    :param phi:
    :param square_size:
    :return: chosen template and score
    """ 
    number_of_points = n
    points = resample_points(list(points), number_of_points)
    points = rotate_to_zero(list(points))
    points = scale_to_square(list(points), square_size=square_size)
    points = translate_to_origin(list(points))

    b = float('inf')

    chosen_template = None

    for template in templates:
        template_points = resample_points(template.points, number_of_points)
        template_points = rotate_to_zero(template_points)
        template_points = scale_to_square(template_points, square_size=square_size)
        template_points = translate_to_origin(template_points)
        
        distance = distance_at_best_angle(points, template_points, -angle_range, angle_range, angle_step, phi)

        if distance < b:
            b = distance
            chosen_template = template
    
    score = 1 - b /(0.5 * np.sqrt(square_size**2 + square_size**2))

    return chosen_template, score


def distance_at_best_angle(points, template_pts, angle_a, angle_b, angle_step, phi):
    x1 = phi * angle_a + (1 - phi) * angle_b
    f1 = distance_at_angle(points, template_pts, x1)
    x2 = (1 - phi) * angle_a + phi * angle_b
    f2 = distance_at_angle(points, template_pts, x2)
    while np.abs(angle_b - angle_a) > angle_step:
        if f1 < f2:
            angle_b = x2
            x2 = x1
            f2 = f1
            x1 = phi * angle_a + (1 - phi) * angle_b
            f1 = distance_at_angle(points, template_pts, x1)
        else:
            angle_a = x1
            x1 = x2
            f1 = f2
            x2 = (1 - phi) * angle_a + phi * angle_b
            f2 = distance_at_angle(points, template_pts, x2)
    return min(f1, f2)


def distance_at_angle(points, template_pts, angle):
    
    x, y = get_centroid(list(points))
    
    centroid = list([x, y])

    new_points = rotate_by(points, angle, centroid)
    d = path_distance(new_points, template_pts)
    
    return d


def path_distance(path1, path2):
    # print("len path 1", len(path1))
    # print("len path 2", len(path2))
    # if len(path1) != len(path2):
    #     print("Not possible, check the paths")
    d = 0
    for p_1, p_2 in zip(path1, path2):
        d = d + get_distance([p_1, p_2])

    return d / len(path1)
