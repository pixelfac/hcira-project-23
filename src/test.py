import random

'''
for each user U = 1 to 10 
  for each example E = 1 to 9 
    for i = 1 to 100 
      for each gesture type G 
        choose E templates from U,G set 
        choose 1 candidate from U,G set 
      for each candidate T from 1 to G 
        recognize T w/ E,G chosen templates 
        if reco correct 
          reco score for each U,G += 1 
    reco score for each U,G /= 100 
report final average per-user accuracy
'''

'''
data is list of list of lists, accessing first by user, then by gesture,
then you have a list of all examples of that gesture by that user
'''

for user in range(0,10):
    for num_examples in range(0,9):
        for i in range(0,10):
            candidate = []
            examples = []
            for gesture in data[user]: # gesture is list of all examples from that user and gesture
                pass
                # sample is random list of num_examples+1 elements randomly picked from gesture
                sample = random.sample(gesture, num_examples+1)
                # last element in sample
                candidate = sample.pop()
                # first num_examples elements from sample
                if len(sample) != num_examples:
                    print("examples list not correct size")
                examples = sample
                # examples num_examples templates randomly from data[user][gesture]
                # choose 1 candidate randomly from data[user][gesture] that's not in examples
            for gesture in range(0,16):
                pass
                # recognize candidate against [example][gesture] template   
                # if recognized:
                    # recognize score for [user][gesture] += 1
        # avg accuracy [user][gesture] = recognize score [user][gesture] / 100
# output final avg acc per user