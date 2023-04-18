import math
import numpy as np
# from templates import templates as default_templates
# from load_data_mmg import data_mmg_flattened

EPSILON = 0.5

def remove_stroke_id_for_unistroke(points):

    new_points = []

    for point in points :
        stroke_id = point.pop()
        new_points.append(point)
    
    return new_points
    # np_points = np.array(points)
    # np_points_2d = np_points[: , : , 0]

    # return np_points_2d.toli
    # rst()


def get_distance(points):
    #reused this method from $1 pre-processing
    """
    Utility method to get distance b/w 2 points
    :param points: array of points
    :return: dist b/w 2 points within the array
    """
    # temp = points[0]
    # print(type(temp[1]))
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
    for i in range(1, n - 1):
        curr_point = points[i]
        prev_point = points[i - 1]
        # print("curr point: " + str(len(curr_point)))
        # print(curr_point)
        # print("prev point: " + str(len(prev_point)))
        # print(prev_point)
        if curr_point[2] == prev_point[2]:
            # print(prev_point[0])
            dist = get_distance([prev_point, curr_point])
            path_length = path_length + dist

    return path_length


def scale(points):
    #reused this method from $1 pre-processing
    """
    Method to scale the points
    :param points: array of coordinates , size of the square.
    :return: new points as an array after scaling
    """
    maximum_x, maximum_y, _ = np.max(points, 0)
    minimum_x, minimum_y, _ = np.min(points, 0)

    scale = max(maximum_x - minimum_x, maximum_y - minimum_y)

    # box_width = maximum_x - minimum_x
    # box_height = maximum_y - minimum_y

    # new_points = np.zeros((1, 3))
    new_points = []

    # for point in points:
    #     q = np.array([0., 0.])
    #     q[0] = point[0] * (square_size / box_width)
    #     q[1] = point[1] * (square_size / box_height)
    #     new_points = np.append(new_points, [q], 0)
    for point in points:
        point_x = (point[0] - minimum_x) / scale
        point_y = (point[1] - minimum_y) / scale
        new_points.append([point_x, point_y, point[2]])
        # new_points = np.append(new_points, [point_x, point_y, point[2]], 0)

    return new_points


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
    # temp_points_x = temp_points[:, 0]
    sum_x_coords = np.sum(temp_points[:, 0])
    sum_y_coords = np.sum(temp_points[:, 1])

    # return sum_x / n, sum_y / n
    return sum_x_coords / n, sum_y_coords / n


def translate_to_origin(points):
    # reused this method from $1 pre-processing
    # needs to be changed
    centroid_x, centroid_y = get_centroid(np.array(points))
    # new_points = np.zeros((1, 3))
    new_points = []

    for point in points:
        # q = np.array([0., 0., 0.])
        q = []
        # q[0] = point[0] - centroid_x
        q.append(point[0] - centroid_x)
        # q[1] = point[1] - centroid_y
        q.append(point[1] - centroid_y)
        # q[2] = point[2]
        q.append(point[2])
        # print(q)
        new_points.append([q])
        # new_points = np.append(new_points, [q], 0)

    return new_points


def resample(points, n):
    # reused this method from $1 pre-processing

    """
    Method to execute 1st step of preprocessing for $1 recogniser. Resample points array to have consistent
    number of points
    :param points: All points identified from user's gesture
    :param n: Size of points array
    :return: new_points array after applying Resampling step.
    """

    # print(len(points))
    path_length = get_path_length(points)
    length = path_length / (n - 1)
    d = 0
    temp_points = list(points[:])
    new_points = [points[0]]
    i = 1
    while i < len(temp_points):
        prev_point = temp_points[i - 1]
        curr_point = temp_points[i]
        if prev_point[2] == curr_point[2]:
            # print("resample:")
            # print(prev_point)
            # print(curr_point)
            dist = get_distance([prev_point, curr_point])
            if (d + dist) >= length:
                qx = temp_points[i - 1][0] + ((length - d) / dist) * (temp_points[i][0] - temp_points[i - 1][0])
                qy = temp_points[i - 1][1] + ((length - d) / dist) * (temp_points[i][1] - temp_points[i - 1][1])
                new_points.append([qx, qy, prev_point[2]])
                temp_points.insert(i, [qx, qy, prev_point[2]])
                d = 0
            else:
                d = d + dist
        i = i + 1

    # Check if size of new array is exactly equal to required n. If not add the last point again to the array
    # print("length: " + str(len(new_points)))
    if len(new_points) < n:
        new_points.append([new_points[-1][0], new_points[-1][1], new_points[-1][2]])

    return new_points


def normalize(points, n=32):
    resampled_points = resample(points, n)
    scaled_points = scale(resampled_points)
    translated_points = translate_to_origin(scaled_points)
    # print("length: " + str(len(translated_points)))

    return translated_points


def get_cloud_distance(points, template, n, start):
    matched_array = [False] * n
    distance_sum = 0
    i = start

    
    while True:
        minimum = float("inf")
        index = None
        j = 0
        while j < n:
            # print("i" + str(points[i]))
            # print("j" + str(template[j]))
            # print("i: " + str(i))
            # print("j: " + str(j))
            if not matched_array[j]:
                d = get_distance([points[i][0], template[j][0]])
                if d < minimum:
                    minimum = d
                    index = j
            j += 1

        matched_array[index] = True
        weight = 1 - ((i - start + n) % n) / n
        distance_sum = distance_sum + weight * minimum
    
        i = (i + 1) % n
        if i == start:
            break

    return distance_sum


def greedy_cloud_match(points, template, n):
    e = EPSILON
    step = int(math.floor(n ** (1 - e)))
    minimum = float("inf")

    for i in range(0, n, step):
        d1 = get_cloud_distance(points, template, n, i)
        d2 = get_cloud_distance(template, points, n, i)

        minimum = min(minimum, d1, d2)

    return minimum


# def recognize(points, n=32, templates=default_templates):
# def recognize(points, n=32, templates=data_mmg_flattened):
def recognize(points, n, templates):
    points = normalize(points, n)
    # print("points length: " + str(len(points)))
    score = float("inf")
    result = None
    

    for template in templates:
        # template.points = normalize(template.points, n)
        # print("template points length: " + str(len(template.points)))
        d = greedy_cloud_match(points, template.points, n)

        if score > d:
            score = d
            result = template
        # scores.append([template.label, d])

        # if result == None or score == 0:
        #     return None, score
        # else:
        #     return result, score

    # # final_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    # # # for temp in final_scores:
    # # #     print(temp[0] + ", " + str(temp[1]))
    # # # return chosen_template, score
    # if len(final_scores) >= 50:
    #     final_scores = final_scores[0:50]
    # return final_scores
    # print()
    return result, score


# def recognize_with_n_best(points, n=32, templates=data_mmg_flattened):
def recognize_with_n_best(points, n, templates):
    number_of_points = n
    # points = normalize(points, n)
    # score = float("inf")
    result = []
    scores = []

    for template in templates:
        # print("normalize:" + str(template.points))
        # template.points = normalize(template.points, n)

        d = greedy_cloud_match(points, template.points, n)
        result.append([template, d])
        scores.append([template.label, d])
        # if score > d:
        #     score = d
        #     result = template

        # if result == None or score == 0:
        #     return None, score
        # else:
        #     return result, score

    final_scores = sorted(scores, key=lambda x: x[1])
    # for temp in final_scores:
    #     print(temp[0] + ", " + str(temp[1]))
    # return chosen_template, score
    if len(final_scores) >= 50:
        final_scores = final_scores[0:50]
    return final_scores

    # return sorted(result)


def preprocess_points(points):
    """
    takes in a list of Points and returns that list after
    all preprocessing steps: resample, rotate, scale, and translate
    :param points: All points itendified from user's gesture
    """
    points = resample(points, 64)
    points = scale(points)
    points = translate_to_origin(points)
    return points


# for template in data_mmg_flattened:
#     template.points = normalize(template.points)