from typing import Callable, List
from collections import defaultdict


class InvalidIntcodeOp(Exception):
    """Unknown Intcode operation."""


class OpCode:
    """Code(intcode) -> new intcode op"""
    def __init__(self, intcode: int):
        self.value = intcode
        *modes, lead, op = f'{self.value:05}'
        self.op = int(lead + op)
        # modes are given from
        # right to left
        self.modes = modes[::-1]

    def __repr__(self):
        return f'Code({self.value})'

    def __eq__(self, other):
        return self.value == other


class Computer:
    """IntcodeComputer(program) -> load program into
    intcode computer.
    """
    def __init__(self, program: str):
        self.program = [int(code) for code in program.split(',')]  # initial program state
        self.memory = defaultdict(int)
        self.memory.update(dict(enumerate(self.program)))
        self.pointer = 0
        self.output = []
        self.rbase = 0  # relative base

        # valid op codes and their corresponding functions
        self.ops = {1: self._op_1, 2: self._op_2, 3: self._op_3,
                    4: self._op_4, 5: self._op_5, 6: self._op_6,
                    7: self._op_7, 8: self._op_8, 9: self._op_9}

    def _get_op_code(self) -> OpCode:
        """Return OpCode object from memory at pointer."""
        intcode = self.memory[self.pointer]
        return OpCode(intcode)

    def _get_op(self, op_code: int) -> Callable:
        """Return op code function to corresponding op code."""
        try:
            return self.ops[op_code]
        except KeyError:
            raise InvalidIntcodeOp(f'Invalid Intcode op code "{op_code}"')

    def _get_args(self, op: OpCode) -> List[int]:
        """Return list of intcodes to be
        used as arguments for an op.
        """
        arg1 = self.memory[self.pointer+1]
        arg2 = self.memory[self.pointer+2]
        arg3 = self.memory[self.pointer+3]
        return [arg1, arg2, arg3]

    def _read(self, intcode: int, mode: str) -> int:
        if mode == '0':         # positional mode
            return self.memory[intcode]
        elif mode == '1':       # immediate mode
            return intcode
        elif mode == '2':       # relative mode
            return self.memory[self.rbase + intcode]

    def _write(self, value: int, intcode: int, mode: str):
        if mode == '0':         # positional mode
            self.memory[intcode] = value
        elif mode == '1':       # immediate mode
            raise TypeError("Can't write in immediate mode")
        elif mode == '2':       # relative mode
            self.memory[self.rbase + intcode] = value

    def _op_1(self, *args: List[int], modes: List[str]):
        """Get the sum of 2 paramters
        and write result to register.
        """
        left_operand = self._read(args[0], modes[0])
        right_operand = self._read(args[1], modes[1])

        sum_ = left_operand + right_operand
        self._write(sum_, args[2], modes[2])

        self.pointer += 4

    def _op_2(self, *args: List[int], modes: List[str]):
        """Get product of 2 paramaters
        and write result to register.
        """
        left_operand = self._read(args[0], modes[0])
        right_operand = self._read(args[1], modes[1])

        product = left_operand * right_operand
        self._write(product, args[2], modes[2])

        self.pointer += 4

    def _op_3(self, *args: List[int], modes: List[str]):
        """Take input and write to register."""
        # input, register, mode
        self._write(args[3], args[0], modes[0])

        self.pointer += 2

    def _op_4(self, *args: List[int], modes: List[str]):
        """Output paramter value from register."""
        register = self._read(args[0], modes[0])
        self.output.append(register)
        self.pointer += 2

    def _op_5(self, *args: List[int], modes: List[str]):
        """Jump to new pointer if parameter
        is non-zero, otherwise move normally.
        """
        predicate = self._read(args[0], modes[0])
        new_pointer = self._read(args[1], modes[1])

        if predicate:
            self.pointer = new_pointer
        else:
            self.pointer += 3

    def _op_6(self, *args: List[int], modes: List[str]):
        """Jump to new pointer if parameter
        is zero, otherwise move normally.
        """
        predicate = self._read(args[0], modes[0])
        new_pointer = self._read(args[1], modes[1])

        if not predicate:
            self.pointer = new_pointer
        else:
            self.pointer += 3

    def _op_7(self, *args: List[int], modes: List[str]):
        """Store 1 in register if first parameter
        is less than the second, otherwise store zero.
        """
        left_operand = self._read(args[0], modes[0])
        right_operand = self._read(args[1], modes[1])

        if left_operand < right_operand:
            self._write(1, args[2], modes[2])
        else:
            self._write(0, args[2], modes[2])

        self.pointer += 4

    def _op_8(self, *args: List[int], modes: List[str]):
        """Store 1 in register if first parameter
        is equal to the second, otherwise store zero.
        """
        left_operand = self._read(args[0], modes[0])
        right_operand = self._read(args[1], modes[1])

        if left_operand == right_operand:
            self._write(1, args[2], modes[2])
        else:
            self._write(0, args[2], modes[2])

        self.pointer += 4

    def _op_9(self, *args: List[int], modes: List[str]):
        """Adjust relative base."""
        self.rbase += self._read(args[0], modes[0])
        self.pointer += 2

    def reset(self):
        """Reset memory and pointer to
        initial program state.
        """
        self.memory.clear()
        self.memory.update(dict(enumerate(self.program)))
        self.pointer = 0
        self.rbase = 0
        self.output = []

    def execute(self, input_: int):
        """Execute intcode program until it halts."""
        while (intcode := self._get_op_code()) != 99:
            args = self._get_args(intcode)
            op = self._get_op(intcode.op)
            op(*args, input_, modes=intcode.modes)
