from typing import List

# Longest Increasing Subsequence
'''
LIS(A[1, 2, ..., n])

1. define table entries
T[i] is LIS ending at element A[i]

2. rescurrence of table entries in terms of smaller subproblems
T[i] = max(1, T[j] + 1 if T[i] > T[j] for j=1 to i-1)

3. runtime
O(n^2)

4. space
O(n)
'''

def lis(list: List) -> int:
    length = len(list)
    table = [0] * (length)
    
    for i in range(length):
        table[i] = 1
        for j in range(i):
            if list[i] > list[j]:
                table[i] = max(table[i], table[j] + 1)
    print('lis table: ', table)
    return max(table)

# Longest Increasing Subarray
'''
LISA(A[1, 2, ..., n])

1. define table entries
T[i] is LISA ending at A[i]

2. recurrance of table entries in terms of smaller subproblem
T[i] = 1              if A[i] <= A[i-1]
T[i] = T[i-1] + 1     if A[i] > A[i-1]

3. runtime
O(n)

4. space
O(n)
'''

def lisa(list: List) -> int:
    length = len(list)
    table = [1] * length

    for i in range(1, length):
        if list[i] > list[i-1]:
            table[i] = table[i-1] + 1
    print('lisa table: ', table)
    return max(table)



def main():
    test_1 = [1, 5, 2, 3, 4]
    lis_res_1 = lis(test_1)
    print(lis_res_1)

    lisa_res_1 = lisa(test_1)
    print(lisa_res_1)

if __name__ == '__main__':
    main()