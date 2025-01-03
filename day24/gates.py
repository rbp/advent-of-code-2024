from collections import namedtuple
import sys

Gate = namedtuple("Gate", "w1 op w2 out".split())

op = {
    "AND": lambda w1, w2: w1 and w2,
    "OR": lambda w1, w2: w1 or w2,
    "XOR": lambda w1, w2: (w1 or w2) and not (w1 and w2),
}


def system_output(wires, gates):
    wires, gates = order_by_dependency(wires, gates)

    for g in gates:
        wires[g.out] = op[g.op](wires[g.w1], wires[g.w2])

    zwires = sorted([w for w in wires if w.startswith("z")])
    output = 0
    for i in range(1, len(zwires)):
        wire = zwires[i]
        output += wires[wire] << i

    return output


def order_by_dependency(wires, gates):
    # The order doesn't really matter...
    depends = gates[::-1]

    ordered_gates = [None] * len(gates)
    placed = set()
    gate_idx = 0
    while depends:
        g = depends.pop()
        if wires[g.w1] is not None and wires[g.w2] is not None:
            ordered_gates[gate_idx] = g
            placed |= {g.w1, g.w2, g.out}
            gate_idx += 1
            continue

        if g.w1 in placed and g.w2 in placed:
            ordered_gates[gate_idx] = g
            placed.add(g.out)
            gate_idx += 1
            continue

        # FIXME: this forces the whole list to shift. But it's fast enough for now...
        depends.insert(0, g)

    return wires, ordered_gates


def read_system(lines):
    wires = {}
    gates = []

    i = 0
    while lines[i]:
        wire, value = lines[i].split(": ")
        wires[wire] = int(value)
        i += 1

    i += 1
    while i < len(lines):
        p1, out_wire = lines[i].split(" -> ")
        w1, op, w2 = p1.split()
        gates.append(Gate(w1, op, w2, out_wire))

        for w in (w1, w2, out_wire):
            if w not in wires:
                wires[w] = None
        i += 1
    return wires, gates


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        wires, gates = read_system(f.read().splitlines())

    print(f"Part 1: {system_output(wires, gates)}")


if __name__ == "__main__":
    main()
