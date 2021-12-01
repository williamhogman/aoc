from fastcore.all import L, AttrDict


Instructions = AttrDict({
    "nop": 0,
    "jmp": 1,
    "acc": 2,
})

advances_ic = {
    Instructions.nop,
    Instructions.acc
}

def cpu_transform(xs):
    return [
        (Instructions[instr], int(operand))
        for (instr, operand) in xs.t
    ]

class CPU:
    def __init__(self, instrs, track_visited=True, break_on_visited=True):
        self.instrs = instrs
        self.reg = AttrDict({ "ic": 0, "acc": 0})
        self.track_visited = track_visited
        self.break_on_visited = break_on_visited
        self.broke_on_visited = False
        self.visited = set([])

    def may_run(self):
        return self.reg.ic < len(self.instrs)

    def get_instr(self):
        current = self.instrs[self.reg.ic]
        return current

    def run(self):
        while self.may_run():
            old_ic = self.reg.ic
            instr = self.get_instr()
            if self.break_on_visited and old_ic in self.visited:
                self.broke_on_visited = True
                break
            yield instr
            if self.track_visited:
                self.visited.add(old_ic)
            if instr[0] in advances_ic:
                self.reg.ic += 1

    def visited_before(self):
        return self.reg.ic in self.visited
