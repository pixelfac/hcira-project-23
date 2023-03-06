import os

users = os.listdir('./')
# remove this file from list
users = users[1:]
print(users)


for user in users:
    samples = os.listdir('./' + user + '/')
    for sample in samples:
        print('./' + user + '/' + sample)
        with open('./' + user + '/' + sample, 'r') as f:
            text = f.readlines()

        text[1] = text[1][:-3] + '>\n'

        # clear and rewrite
        with open('./' + user + '/' + sample, 'w') as f:
            f.writelines(text)
            