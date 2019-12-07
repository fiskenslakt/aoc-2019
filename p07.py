from itertools import cycle, permutations

from aocd import data

from p05 import IntcodeComputer


class Amplifier(IntcodeComputer):
    def execute(self, phase, signal):
        inputs = iter((phase, signal))
        while (code := self._get_op_code()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)
            op = self._get_op(code.op)

            if code.op == 3:
                op(arg1, next(inputs))
            else:
                op(arg1, arg2, arg3, None)

    def execute_feedback(self, amp_input):
        init = True
        while (code := self._get_op_code()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)
            op = self._get_op(code.op)

            if code.op == 3:
                op(arg1, amp_input)
                if init:
                    init = False
                    amp_input = yield
            elif code.op == 4:
                self.pointer += 2
                amp_input = yield arg1.value
            else:
                op(arg1, arg2, arg3, None)


program = [code for code in data.split(',')]
computer = Amplifier(program)
thruster_signal = 0
for sequence in permutations(range(5)):
    signal = 0
    for phase in sequence:
        computer.execute(str(phase), str(signal))
        signal = computer.diagnostic_codes[0].value
        computer.reset()
    thruster_signal = max(thruster_signal, signal)

print('Part 1:',thruster_signal)

thruster_signal = 0
for sequence in permutations(range(5, 10)):
    amplifiers = []
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
