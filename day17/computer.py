import sys


class Computer:
    def __init__(self, a, b, c, instructions):
        self.a = a
        self.b = b
        self.c = c
        self.instructions = instructions
        self._pointer = 0

    def run(self):
        output = []
        self._pointer = 0
        while self._pointer < len(self.instructions):
            out, move = self.exec(
                self.instructions[self._pointer], self.instructions[self._pointer + 1]
            )
            output.append(out)
            if move:
                self._pointer += 2
        return output

    def exec(self, opcode, value):
        out = ""
        move = True
        match opcode:
            # adv
            case 0:
                self.a = int(self.a / (2 ** self.combo(value)))
            # bxl
            case 1:
                self.b = self.b ^ value
            # bst
            case 2:
                self.b = self.combo(value) % 8
            # jnz
            case 3:
                if self.a != 0:
                    self._pointer = value
                    move = False
            # bxc
            case 4:
                self.b = self.b ^ self.c
            # out
            case 5:
                out = str(self.combo(value) % 8)
            # bdv
            case 6:
                self.b = int(self.a / (2 ** self.combo(value)))
            # cdv
            case 7:
                self.c = int(self.a / (2 ** self.combo(value)))
            case _:
                raise ValueError(f"Invalue opcode: {opcode}")
        return out, move

    def combo(self, value):
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid operand for combo: {value}")


def output(computer):
    return ",".join(out for out in computer.run() if out)


def read_program(s):
    a = int(s[0].split(": ")[1].strip())
    b = int(s[1].split(": ")[1].strip())
    c = int(s[2].split(": ")[1].strip())
    instructions = [int(i) for i in s[4].split(": ")[1].strip().split(",")]
    return Computer(a, b, c, instructions)


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        input_text = f.read().splitlines()

    print(f"Part 1: {output(read_program(input_text))}")


if __name__ == "__main__":
    main()
