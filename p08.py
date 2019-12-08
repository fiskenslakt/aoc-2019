from aocd import data

x = 25 * 6
layers = []
for i in range(0, len(data), x):
    layers.append(data[i:i+x].count('0'))

smallest = layers.index(min(layers))
print(data[x*smallest:x*smallest+x].count('1')*data[x*smallest:x*smallest+x].count('2'))

layers = []
for i in range(0, len(data), x):
    layers.append(data[i:i+x+1])

line = 0
for pixel in zip(*layers):
    line += 1
    for layer in pixel:
        if layer == '0':
            print(' ',end='')
            break
        elif layer == '1':
            print('#',end='')
            break
    else:
        print(' ',end='')

    if line == 25:
        print()
        line = 0
