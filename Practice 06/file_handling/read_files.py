with open('sample.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    print(data)

with open('sample.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())