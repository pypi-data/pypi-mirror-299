import time

import numpy as np

def std_by_section_og(array: np.ndarray, num_sections: int) -> np.ndarray:
    section_length = len(array) // num_sections
    remainder = len(array) % num_sections

    slices = []
    start = 0
    for i in range(num_sections):
        if i < remainder:
            end = start + section_length + 1
        else:
            end = start + section_length
        slices.append(slice(start, end))
        start = end

    return np.array([np.std(array[slice_]) for slice_ in slices])


def std_by_section(array: np.ndarray, num_sections: int) -> np.ndarray:
    section_length = len(array) // num_sections
    remainder = len(array) % num_sections

    # Calculate indices for slicing
    indices = np.arange(0, len(array) + 1, section_length)
    if remainder:
        indices = np.hstack([indices[:-1], indices[-2:] + remainder])

    # Calculate standard deviation for each section
    return np.array([np.std(array[indices[i]:indices[i+1]]) for i in range(num_sections)])

# Example usage
array = np.random.rand(100000)
num_sections = 10
n = 100
start = time.perf_counter()
for i in range(n):
    result = None
    result = std_by_section(array, num_sections)
end = time.perf_counter()

start2 = time.perf_counter()
for i in range(n):
    result = None
    result = std_by_section_og(array, num_sections)
end2 = time.perf_counter()

print("og", (end2-start2)/n)
print("new", (end-start)/n)
print(result)