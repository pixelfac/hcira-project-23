import random
from preprocess_dollar_one import recognize
from load_data import data


'''
data is list of list of lists, accessing first by user, then by gesture,
then you have a list of all examples of that gesture by that user, where example is a Unistroke object

recognize_score is list of list of numbers, tracking the recognize score per user, per gesture

recognize_acc is list of list of numbers, tracking %correct per user, per gesture
'''
# number ot times to tests each group
iterations = 1
users = list(data.keys())
recognize_score = {}
for user_index in range(0, len(data.keys())):
    recognize_score[users[user_index]] = {}
    for gesture_index in data[users[0]].keys():
        recognize_score[users[user_index]][gesture_index] = 0.0

accuracy = []

# for user_index in range(0,len(users)):
for user_index in range(0,1):
    print("user: " + users[user_index])
    # if users[user_index] not in recognize_score.keys():
    #     recognize_score[users[user_index]] = {}
        # pass
    # else:
    #     recognize_score[users[user_index]] = {}

    for num_examples in range(1,10):
        print("num_examples: " + str(num_examples))
        for i in range(0,iterations):
            candidates = []
            examples = []
            for gesture in data[users[user_index]]: # gesture is list of all examples from that user and gesture
                # if gesture not in recognize_score[users[user_index]].keys():
                    # print("NOT IN")
                    # recognize_score[users[user_index]][gesture] = 0.0
                # pass
                # sample is random list of num_examples+1 elements randomly picked from gesture
                # print("======= length: " + str(len(data[users[user_index]][gesture])))
                sample = random.sample(data[users[user_index]][gesture], num_examples+1)
                # last element in sample
                candidate = sample.pop()
                candidates.append(candidate)

                if len(sample) != num_examples: # test for correctness
                    print("examples list not correct size")

                # first num_examples elements from sample
                # example = sample
                # examples.extend(example)
                examples.extend(sample)

            for candidate in candidates:
                template, score = recognize(candidate.points, 64, examples)
                # print(template.label + ", actual: " + candidate.label)

                if template.label == candidate.label:
                    # print("CORRECT")
                    # print(recognize_score[users[user_index]][gesture])
                    for gesture_index_temp in data[users[user_index]]:
                        recognize_score[users[user_index]][gesture_index_temp] = recognize_score[users[user_index]][gesture_index_temp] + 1.0
                    # recognize_score[users[user_index]][gesture] = recognize_score[users[user_index]][gesture] + 1.0

            # for gesture in range(0,16):
            #     pass
            #     # recognize candidate against [example][gesture] template
            #     template, score = recognize(candidates[gesture], 64, examples[gesture])
            #
            #     if template.label == candidate.label:
            #         recognize_score[user][gesture] += 1
        # avg accuracy [user][gesture] = recognize score [user][gesture] / 100
        # recognize_acc[user][gesture] = recognize_score[user][gesture] / 100
        for gesture_index_temp in data[users[user_index]]:
            recognize_score[users[user_index]][gesture_index_temp] = recognize_score[users[user_index]][gesture_index_temp] / 10.0
        # recognize_score[users[user_index]][gesture] = recognize_score[users[user_index]][gesture] / 10.0

# output final avg acc per user
# print(recognize_score[users[0]]['arrow'])
# print(recognize_score[users[0]].keys())
print(recognize_score[users[0]])

for users in data.keys():
    print(recognize_score[users])
