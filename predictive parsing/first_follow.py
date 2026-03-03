from collections import defaultdict


def read_grammar(filename):
    grammar = {}
    with open(filename, "r") as file:
        for line in file:
            left, right = line.split("->")
            left = left.strip()
            productions = [p.strip().split() for p in right.split("|")]
            grammar[left] = productions
    return grammar


def compute_first(grammar):
    first = defaultdict(set)

    def first_of(symbol):
        if symbol not in grammar:
            return {symbol}

        for production in grammar[symbol]:
            for sym in production:
                sym_first = first_of(sym)
                first[symbol].update(sym_first - {"#"})
                if "#" not in sym_first:
                    break
            else:
                first[symbol].add("#")

        return first[symbol]

    for nt in grammar:
        first_of(nt)

    return first


def compute_follow(grammar, first):
    follow = defaultdict(set)
    start_symbol = list(grammar.keys())[0]
    follow[start_symbol].add("$")

    for nt in grammar:
        for production in grammar[nt]:
            for i in range(len(production)):
                if production[i] in grammar:
                    next_symbols = production[i + 1:]
                    if next_symbols:
                        for sym in next_symbols:
                            follow[production[i]].update(first[sym] - {"#"})
                            if "#" not in first[sym]:
                                break
                        else:
                            follow[production[i]].update(follow[nt])
                    else:
                        follow[production[i]].update(follow[nt])

    return follow


if __name__ == "__main__":
    grammar = read_grammar("grammar_input.txt")

    first = compute_first(grammar)
    follow = compute_follow(grammar, first)

    print("FIRST Sets:\n")
    for nt in first:
        print(f"{nt} : {first[nt]}")

    print("\nFOLLOW Sets:\n")
    for nt in follow:
        print(f"{nt} : {follow[nt]}")
