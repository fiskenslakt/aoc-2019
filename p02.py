from aocd import data


target = 19690720
data = [int(code) for code in data.split(',')]

for noun in range(100):
    for verb in range(100):
        program = data.copy()
        program[1] = noun
        program[2] = verb

        pointer = 0

        while program[pointer] != 99:
            input_a = program[pointer+1]
            input_b = program[pointer+2]
            output = program[pointer+3]

            if program[pointer] == 1:
                program[output] = program[input_a] + program[input_b]
            elif program[pointer] == 2:
                program[output] = program[input_a] * program[input_b]

            pointer += 4

        if program[0] == target:
            print('Part 2:', 100 * noun + verb)
            raise SystemExit
        elif noun == 12 and verb == 2:
            print('Part 1:', program[0])
