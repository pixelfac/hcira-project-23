shapes = {
    1: "triangle",
    2: "x",
    3: "rectangle",
    4: "circle",
    5: "check",
    6: "caret",
    7: "zig-zag",
    8: "arrow",
    9: "left square bracket",
    10: "right square bracket",
    11: "v",
    12: "delete",
    13: "left curly brace",
    14: "right curly brace",
    15: "star",
    16: "pigtail"
}


def get_current_shape(shape_number):
    return shapes[shape_number]


def collect_points(user_points, point):
    user_points.append(point)
    return user_points


def add_samples(dataset, user, shape_number, samples):
    shape = get_current_shape(shape_number)
    dataset[str(user)][str(shape)] = samples

    return dataset

