import random
from preprocess_dollar_one import recognize

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
then you have a list of all examples of that gesture by that user, where example is a Unistroke object

recognize_score is list of list of numbers, tracking the recognize score per user, per gesture
recognize_acc is list of list of numbers, tracking %correct per user, per gesture
'''
# number ot times to tests each group
iteractions = 10

for user in range(0,10):
    for num_examples in range(1,10):
        for i in range(0,iterations):
            candidates = []
            examples = []
            for gesture in data[user]: # gesture is list of all examples from that user and gesture
                pass
                # sample is random list of num_examples+1 elements randomly picked from gesture
                sample = random.sample(gesture, num_examples+1)
                # last element in sample
                candidate = sample.pop()
                candidates.append(candidate)

                if len(sample) != num_examples: # test for correctness
                    print("examples list not correct size")

                # first num_examples elements from sample
                example = sample
                examples.append(example)

            for gesture in range(0,16):
                pass
                # recognize candidate against [example][gesture] template 
                template, score = recognize(candidates[gesture], examples[gesture], 64)
                
                if template.label == candidate.label:
                    recognize_score[user][gesture] += 1
        # avg accuracy [user][gesture] = recognize score [user][gesture] / 100
        recognize_acc[user][gesture] = recognize_score[user][gesture] / 100

# output final avg acc per user
