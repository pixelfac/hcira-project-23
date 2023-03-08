import os

users = os.listdir('./')
# remove this file from list
users = users[1:4]
print(users)


for user in users:

    samples = os.listdir('./' + user + '/')
    for sample in samples:
        print('./' + user + '/' + sample)
        with open('./' + user + '/' + sample, 'r') as f:
            text = f.readlines()

        for i in range(2, len(text)-1):
            text[i] = text[i][:-3] + f'T="{i}" />\n'

        # clear and rewrite
        with open('./' + user + '/' + sample, 'w') as f:
            f.writelines(text)