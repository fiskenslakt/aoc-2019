from itertools import cycle, permutations

from aocd import data
from p05 import IntcodeComputer


class Amplifier(IntcodeComputer):
    def execute(self, phase, signal):
        inputs = iter((phase, signal))
        while (code := self._get_op()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)

            if code.op == 1:
                self.add(arg1, arg2, arg3)
            elif code.op == 2:
                self.multiply(arg1, arg2, arg3)
            elif code.op == 3:
                self.memory[arg1.value] = next(inputs)
                self.pointer += 2
            elif code.op == 4:
                self.diagnostic_codes.append(arg1)
                self.pointer += 2
            elif code.op == 5:
                self.jump_if_true(arg1, arg2)
            elif code.op == 6:
                self.jump_if_false(arg1, arg2)
            elif code.op == 7:
                self.less_than(arg1, arg2, arg3)
            elif code.op == 8:
                self.equals(arg1, arg2, arg3)
            else:
                raise InvalidIntcodeOp(f'Invalid Intcode op "{code.op}"')

    def execute_feedback(self, amp_input):
        init = True
        while (code := self._get_op()).value != 99:
            # print(amp_input, type(amp_input))
            arg1, arg2, arg3 = self._get_args(code)
            # print(arg1, type(arg1))

            if code.op == 1:
                self.add(arg1, arg2, arg3)
            elif code.op == 2:
                self.multiply(arg1, arg2, arg3)
            elif code.op == 3:
                self.memory[arg1.value] = amp_input
                self.pointer += 2
                if init:
                    init = False
                    amp_input = yield
            elif code.op == 4:
                self.diagnostic_codes.append(arg1.value)
                self.pointer += 2
                # print('about to yield')
                amp_input = yield arg1.value
            elif code.op == 5:
                self.jump_if_true(arg1, arg2)
            elif code.op == 6:
                self.jump_if_false(arg1, arg2)
            elif code.op == 7:
                self.less_than(arg1, arg2, arg3)
            elif code.op == 8:
                self.equals(arg1, arg2, arg3)
            else:
                raise InvalidIntcodeOp(f'Invalid Intcode op "{code.op}"')


# data = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
# data = '''3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'''
# data = '''3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
# -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
# 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'''
program = [code for code in data.split(',')]
computer = Amplifier(program)
thruster_signal = 0
for sequence in permutations(range(5)):
    signal = 0
    for phase in sequence:
        # amp_inputs = iter((str(phase), str(signal)))
        computer.execute(str(phase), str(signal))
        # computer.execute(next(amp_inputs))
        signal = computer.diagnostic_codes[0].value
        computer.reset()
    thruster_signal = max(thruster_signal, signal)

print('Part 1:',thruster_signal)

thruster_signal = 0
for sequence in permutations(range(5, 10)):
    # if sequence != (9, 8, 7, 6, 5):
    #     continue
    # if sequence != (9, 7, 8, 5, 6):
    #     continue
    amplifiers = []
    # print(sequence)
    signal = '0'
    for phase in sequence:
        amplifiers.append((Amplifier(program).execute_feedback(phase)))

    # initialize amplifiers
    for amplifier in amplifiers:
        amplifier.send(None)

    for amplifier in cycle(amplifiers):
        try:
            signal = amplifier.send(str(signal))
            thruster_signal = max(thruster_signal, signal)
        except StopIteration:
            break

print('Part 2:', thruster_signal)
