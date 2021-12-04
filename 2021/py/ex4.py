f = open("ex4.txt").readlines()

numbers = list(map(int, f[0].strip().split(",")))


class Board:
    def __init__(self, numbers):
        self.numbers = numbers

    def calc_score(self, numbers):
        score = 0
        for line in self.numbers:
            for li in line:
                if li not in numbers:
                    score += li
        return score

    def __repr__(self):
        return f"Board({repr(self.numbers)})"

    def has_line(self, others):
        for l in self.numbers:
            if all(li in others for li in l):
                print("Line", l)
                return self.calc_score(others)

        # columns
        for i in range(len(self.numbers[0])):
            column = [line[i] for line in self.numbers]
            if all(li in others for li in column):
                print("Col", column)
                return self.calc_score(others)

        # diagonals
        diag1 = [self.numbers[i][i] for i in range(len(self.numbers))]
        diag2 = [
            self.numbers[i][len(self.numbers) - i - 1] for i in range(len(self.numbers))
        ]
        if False and all(li in others for li in diag1):
            print("Diag1", diag1)
            return self.calc_score(others)
        if False and all(li in others for li in diag2):
            print("Diag2", diag2)
            return self.calc_score(others)

        return None


boards = []
current_board = []
for line in f[2:]:
    line = line.strip()
    if line == "":
        boards.append(Board(current_board))
        current_board = []
    else:
        l = [int(x) for x in line.split(" ") if x.strip()]
        current_board.append(l)

if current_board != []:
    boards.append(Board(current_board))

print(numbers)
print(boards)


def ex1():
    for i in range(0, len(numbers)):
        print("Called: ", numbers[i])
        current_numbers = numbers[0 : i + 1]
        for i, board in enumerate(boards):
            unmarked_n = board.has_line(current_numbers)
            if unmarked_n is not None:
                print(i, unmarked_n, current_numbers[-1])
                print(unmarked_n * current_numbers[-1])
                return
    print("Done!")


def ex2():
    won_at = {}
    won_with = {}
    for i in range(0, len(numbers)):
        current_numbers = numbers[0 : i + 1]
        for j, board in enumerate(boards):
            if j in won_at:
                continue
            unmarked_n = board.has_line(current_numbers)
            if unmarked_n is not None:
                won_at[j] = i
                won_with[j] = unmarked_n * current_numbers[-1]

    won_at = sorted(won_at.items(), key=lambda x: -x[1])
    print(won_with[won_at[0][0]])


def main():
    ex1()
    ex2()


if __name__ == "__main__":
    main()
