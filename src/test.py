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

gestures = []

for user in range(1,10):
    for example in range(1,9):
        for i in range(1,100):
            for gesture in gestures:
                pass
                # choose e templates randomly from data[user][gesture]
                # choose 1 candidate randomly from data[user][gesture] that's not 
            for candidate in range(1,gesture):
                pass
                # recognize candidate against [example][gesture] template   
                # if recognized:
                    # recognize score for [user][gesture] += 1
        # avg accuracy [user][gesture] = recognize score [user][gesture] / 100
# output final avg acc per user