from aocd import data


codes = [code for code in data.split(',')]

pointer = 0
while True:
    # if pointer == 314:
    #     break
    print(pointer, codes[pointer:pointer+4])
    *params, lead, op = codes[pointer].zfill(5)
    arg1, arg2, arg3 = map(int, codes[pointer+1:pointer+4])
    if op == '3':
        # if params[-1] == '0':
        #     # codes[1] = int(codes[arg1])
        #     codes[1] = 1
        # else:
        #     # assert params[-1] == '1'
        #     # codes[1] = arg1
        #     codes[1] = 1

        # codes[arg1] = 1  # part 1
        codes[arg1] = 5  # part 2

        pointer += 2

    elif op == '4':
        if params[-1] == '0':
            print('OUTPUT:',codes[arg1])
        else:
            print('DEBUG OUTPUT:',arg1)
            assert params[-1] == '1'
            print('OUTPUT:',arg1)

        pointer += 2

    elif op == '1':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2

        if params[-3] == '0':
            # c = int(codes[arg3])
            c = arg3
        else:
            assert params[-3] == '1'
            c = arg3

        # print(params, op, codes[pointer])
        # print(arg1, codes[arg1], arg2, codes[arg2], arg3, codes[arg3])
        # print('debug', codes[c])
        codes[c] = str(a + b)
        # print('debug', codes[c])

        pointer += 4

    elif op == '2':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2

        if params[-3] == '0':
            # c = int(codes[arg3])
            c = arg3
        else:
            assert params[-3] == '1'
            c = arg3

        # print(codes[pointer:pointer+4])
        # print(params, op)
        codes[c] = str(a * b)

        pointer += 4
    elif op == '5':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2
        if a != 0:
            pointer = b
        else:
            pointer += 3
    elif op == '6':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2
        if a == 0:
            pointer = b
        else:
            pointer += 3
    elif op == '7':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2

        if a < b:
            codes[arg3] = 1
        else:
            codes[arg3] = 0

        pointer += 4
    elif op == '8':
        if params[-1] == '0':
            a = int(codes[arg1])
        else:
            assert params[-1] == '1'
            a = arg1

        if params[-2] == '0':
            b = int(codes[arg2])
        else:
            assert params[-2] == '1'
            b = arg2

        if a == b:
            codes[arg3] = 1
        else:
            codes[arg3] = 0

        pointer += 4
    else:
        raise ValueError(f'invalid op code {op}')
