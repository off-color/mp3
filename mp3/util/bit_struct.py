def unpack(string, bits):
    result = []
    counter = 0
    str_counter = 0

    while counter < len(bits):
        count = int(string[str_counter])
        offset = 2
        letter_offset = 1

        if string[str_counter + 1].isdigit():
            letter_offset = 2
            offset = 3
            count = int(string[str_counter:str_counter+2])

        t = string[str_counter + letter_offset]
        str_counter += offset
        result.append(types[t](bits[counter:counter + count]))
        counter += count
    return result


def divide_int(string):
    return (int_parse(divide(string)[0]), int_parse(divide(string)[1]))


def divide_bool(string):
    return (bool(int(divide(string)[0])), bool(int(divide(string)[1])))


def divide(string):
    if len(string) < 2:
        raise ArgumentException('Need at least 2 bits to divide')
    return (string[:len(string)//2], string[len(string)//2:])


def int_parse(string):
    return int(string, base=2)


def bool_parse(string):
    return bool(int_parse(string))


types = {'i': int_parse, 'b': bool_parse, 'n': lambda x: x, 't': divide_int,
         'r': divide_bool, 'h': divide}
