import os

users = os.listdir('./')
# remove this file from list
users = users[1:]
print(users)


for user in users:

    samples = os.listdir('./' + user + '/')
    for sample in samples:
        # print('./' + user + '/' + sample)
        with open('./' + user + '/' + sample, 'r') as f:
            text = f.readlines()

        line = text[1]
        first_quote = line.find('"')
        second_quote = line.find('"', first_quote+1)
        sample_name = line[first_quote+1:second_quote]

        # add 0 to single digit numbers
        if not sample_name.endswith('10'):
            sample_name = sample_name[:-1] + '0' + sample_name[-1:]
            
            line = line[:first_quote+1] + sample_name + line[second_quote:]

        text[1] = line
        # clear and rewrite
        with open('./' + user + '/' + sample, 'w') as f:
            f.writelines(text)