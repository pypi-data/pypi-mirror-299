import numpy as np

def entropy_logarithm(p):
    return (-1) * p * np.log2(p) if p != 0 else 0

def entropy(p):
    return np.sum([entropy_logarithm(prob) for prob in p])

# @param[in]    y       pandas.Series
def information(y):
    class_counts = y.value_counts(normalize=True)
    return entropy(class_counts)

def calculate_midpoints(numbers):
    sorted_numbers = np.sort(numbers)
    return (sorted_numbers[:-1] + sorted_numbers[1:]) / 2

def minimum_information_gain(N, E, E1, E2, k, k1, k2):
    return (np.log2(N - 1) / N) + ((np.log2(3**k - 2) - k * E + k1 * E1 + k2 * E2)/N)

def find_pivots(z):
    feature = z.columns[0]
    target = z.columns[1]
    information_upper_bound = np.log2(len(z[target].unique())) + 1
    pivots = []
    stack = [z]
    while len(stack) > 0:
        z = stack.pop()
        N = len(z)
        unique_values = z[feature].unique()
        pivot_candidates = calculate_midpoints(unique_values)
        if len(pivot_candidates) == 0:
            continue

        best_pivot = None
        smallest_information_value = information_upper_bound
        for pivot in pivot_candidates:
            z1 = z[z[feature] > pivot]
            z2 = z[z[feature] <= pivot]
            n1 = len(z1)
            n2 = len(z2)

            information_value = (n1 / N) * information(z1[target]) + (n2 / N) * information(z2[target])
            if information_value <= smallest_information_value:
                best_pivot = pivot
                smallest_information_value = information_value

        E = information(z[target])
        k = len(z[target].unique())
        z1 = z[z[feature] > best_pivot]
        z2 = z[z[feature] <= best_pivot]
        E1 = information(z1[target])
        E2 = information(z2[target])
        k1 = len(z1[target].unique())
        k2 = len(z2[target].unique())

        min_inf_gain = minimum_information_gain(N, E, E1, E2, k, k1, k2)
        if (E - min_inf_gain) > smallest_information_value:
            pivots.append(best_pivot)
            stack.append(z1)
            stack.append(z2)

    return pivots