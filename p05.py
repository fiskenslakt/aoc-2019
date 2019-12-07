from typing import List

from aocd import data


class InvalidIntcodeOp(Exception):
    """Unknown Intcode operation."""


class Code:
    def __init__(self, code: str, is_op: bool = False):
        self.value = int(code)
        self.is_op = is_op
        self.op = None
        self.modes = None

        if is_op:
            *modes, lead, op = f'{self.value:05}'
            self.op = int(lead + op)
            # modes are given from
            # right to left
            self.modes = modes[::-1]

    def __repr__(self):
        if self.is_op:
            return f'Code({self.value}, {self.is_op})'
        else:
            return f'Code({self.value})'

    def __add__(self, other):
        return self.value + other.value

    def __mul__(self, other):
        return self.value * other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __bool__(self):
        return bool(self.value)


class IntcodeComputer:
    def __init__(self, program: List[str]):
        self.program = program
        self.memory = program.copy()
        self.pointer = 0
        self.diagnostic_codes = []

    def _get_op(self) -> Code:
        return Code(self.memory[self.pointer], is_op=True)

    def _get_args(self, op: Code) -> List[Code]:
        args = []

        # get input paramters
        for param, mode in zip(self.memory[self.pointer+1:self.pointer+3], op.modes):
            param = Code(param)
            if mode == '0' and op.op != 3:  # positional mode
                param = Code(self.memory[param.value])
                args.append(param)
            else:  # immediate mode
                args.append(param)

            if op.op in (3, 4):
                args.append(None)
                break

        # try to get output parameter
        try:
            args.append(Code(self.memory[self.pointer+3]))
        except IndexError:
            args.append(None)

        return args

    def reset(self):
        """Reset memory and pointer to
        initial program state.
        """
        self.memory = self.program.copy()
        self.pointer = 0
        self.diagnostic_codes = []

    def add(self, left_operand: Code, right_operand: Code, output: Code):
        self.memory[output.value] = left_operand + right_operand
        self.pointer += 4

    def multiply(self, left_operand: Code, right_operand: Code, output: Code):
        self.memory[output.value] = left_operand * right_operand
        self.pointer += 4

    def jump_if_true(self, predicate: Code, new_pointer: Code):
        if predicate:
            self.pointer = new_pointer.value
        else:
            self.pointer += 3

    def jump_if_false(self, predicate: Code, new_pointer: Code):
        if not predicate:
            self.pointer = new_pointer.value
        else:
            self.pointer += 3

    def less_than(self, left_operand: Code, right_operand: Code, output: Code):
        if left_operand < right_operand:
            self.memory[output.value] = 1
        else:
            self.memory[output.value] = 0

        self.pointer += 4

    def equals(self, left_operand: Code, right_operand: Code, output: Code):
        if left_operand == right_operand:
            self.memory[output.value] = 1
        else:
            self.memory[output.value] = 0

        self.pointer += 4

    def execute(self, system_id: str):
        while (code := self._get_op()).value != 99:
            arg1, arg2, arg3 = self._get_args(code)

            if code.op == 1:
                self.add(arg1, arg2, arg3)
            elif code.op == 2:
                self.multiply(arg1, arg2, arg3)
            elif code.op == 3:
                self.memory[arg1.value] = system_id
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


if __name__ == '__main__':
    program = [code for code in data.split(',')]
    computer = IntcodeComputer(program)
    computer.execute('1')
    print('Diagnostic codes:', computer.diagnostic_codes)
    print('Part 1:', computer.diagnostic_codes[-1].value)

    computer.reset()
    computer.execute('5')
    print('Diagnostic codes:', computer.diagnostic_codes)
    print('Part 2:', computer.diagnostic_codes[-1].value)
