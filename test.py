def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def count_occurrences(seq):
    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts

# Generiert alle unterscheidbaren Permutationen eines Multisets
def distinct_permutations(seq):
    def backtrack(path, counter, length, results):
        if len(path) == length:
            results.append(path[:])
            return
        for item in counter:
            if counter[item] > 0:
                path.append(item)
                counter[item] -= 1
                backtrack(path, counter, length, results)
                counter[item] += 1
                path.pop()

    counter = count_occurrences(seq)
    results = []
    backtrack([], counter, len(seq), results)
    return results

# Beispiel: 7 Kästchen, je 6 Einträge
boxes = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6]

# Generiere alternierende 1, 2, 1, 2, ...
def alternating_sequence(n):
    result = []
    current = 1
    for _ in range(n):
        result.append(current)
        current = 2 if current == 1 else 1
    return result

# Permutationen erzeugen
all_combinations = distinct_permutations(boxes)

for combination in all_combinations:
    print(combination)