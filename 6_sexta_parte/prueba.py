from collections import Counter

def isValidSubset(subset, numbers, threshold):
    subsetSum = sum(subset)
    if subsetSum > threshold:
        return False

    subsetCount = Counter(subset)
    numbersCount = Counter(numbers)

    for num, count in subsetCount.items():
        if count > numbersCount[num]:  # Exceeds original frequency
            return False

    return True

def isMaximal(subset, numbers, threshold):
    subsetCount = Counter(subset)
    numbersCount = Counter(numbers)
    currentSum = sum(subset)

    for num in numbersCount:
        if subsetCount[num] < numbersCount[num]:
            if currentSum + num <= threshold:
                return False
    return True

def verifySolution(numbers, threshold, subsets):
    for subset in subsets:
        if not isValidSubset(subset, numbers, threshold):
            return f"Subset {subset} is invalid."

        if not isMaximal(subset, numbers, threshold):
            return f"Subset {subset} is not maximal."

    return "All subsets are valid and maximal!"

# Example usage
numbers = [1, 2, 2, 3]
threshold = 5
# Subsets from the algorithm
subsets = [[1, 2, 2], [2, 3]]

# Verify
print( verifySolution(numbers, threshold*1000000, subsets) )