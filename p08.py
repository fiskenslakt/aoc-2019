from aocd import data


WIDTH = 25
HEIGHT = 6
AREA = WIDTH * HEIGHT

zero_frequencies = []

for i in range(0, len(data), AREA):
    zero_frequencies.append(data[i:i+AREA].count('0'))

fewest_zeros = zero_frequencies.index(min(zero_frequencies))
ones = data[AREA*fewest_zeros:AREA*fewest_zeros+AREA].count('1')
twos = data[AREA*fewest_zeros:AREA*fewest_zeros+AREA].count('2')
print('Part 1:', ones*twos)

print('Part 2:')
layers = []
for i in range(0, len(data), AREA):
    layers.append(data[i:i+AREA])

for i, pixel in enumerate(zip(*layers), 1):
    for layer in pixel:
        if layer == '1':
            print('#', end='')
            break
        elif layer == '0':
            print(' ', end='')
            break

    if i % 25 == 0:
        print()
