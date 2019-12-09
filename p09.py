from aocd import data

from p05 import Code, IntcodeComputer


class Boost(IntcodeComputer):
    def __init__(self, program):
        self.rbase = 0
        super().__init__(program)
        self.ops.update({9: self._op_9})

    def _get_args(self, op):
        param = Code(self.memory[self.pointer+1])
        if op.op == 3:
            if op.modes[0] == '0':
                return [param, None, None]
            elif op.modes[0] == '2':
                return [Code(param.value + self.rbase), None, None]
        elif op.op in (4,9):
            if op.modes[0] == '0':
                return [Code(self.memory[param.value]), None, None]
            elif op.modes[0] == '1':
                return [Code(param.value), None, None]
            elif op.modes[0] == '2':
                return [Code(self.memory[param.value+self.rbase]), None, None]
        elif op.op in (1, 2, 7, 8):
            args = []
            for param, mode in zip(self.memory[self.pointer+1:self.pointer+3], op.modes):
                if mode == '0':
                    args.append(Code(self.memory[int(param)]))
                elif mode == '1':
                    args.append(Code(param))
                elif mode == '2':
                    args.append(Code(self.memory[int(param) + self.rbase]))

            if op.modes[2] == '0':
                args.append(Code(self.memory[self.pointer+3]))
            elif op.modes[2] == '2':
                args.append(Code(int(self.memory[self.pointer+3])+self.rbase))

            return args
        elif op.op in (5, 6):
            args = []
            for param, mode in zip(self.memory[self.pointer+1:self.pointer+3], op.modes):
                if mode == '0':
                    args.append(Code(self.memory[int(param)]))
                elif mode == '1':
                    args.append(Code(param))
                elif mode == '2':
                    args.append(Code(self.memory[int(param) + self.rbase]))

            return args + [None]

    def _op_9(self, *args):
        arg1, *_ = args
        self.rbase += arg1.value
        self.pointer += 2


# data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
# data = '1102,34915192,34915192,7,4,7,99,0'
# data = '104,1125899906842624,99'
program = [code for code in data.split(',')]
program.extend(['0']*100000)
boost = Boost(program)
boost.execute('1')
# boost.execute('2')
print(boost.diagnostic_codes)
