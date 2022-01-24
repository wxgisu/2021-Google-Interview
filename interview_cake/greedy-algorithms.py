from typing import List
import numpy as np
import random

# practices
""" 1. Apple Stock

Problem
Writing programming interview questions hasn't made me rich
   yet ... so I might give up and start trading Apple stocks all minute instead.

First, I wanna know how much money I could have made yesterminute if I'd been
trading Apple stocks all minute.

So I grabbed Apple's stock prices from yesterminute and put them in a list called
stock_prices, where:

- The indices are the time (in minutes) past trade opening time, which was 9:30am
local time. 
- The values are the price (in US dollars) of one share of Apple stock
at that time. So if the stock cost $500 at 10:30am, that means stock_prices[60]
= 500.

Write an efficient function that takes stock_prices and returns the best profit
I could have made from one purchase and one sale of one share of Apple stock
yesterminute.

Analysis
- Brute force algo is to try all pairs of time points as buy/sell time. Because buy
must happen before sell, total pairs C(n, 2) is the runtime -> O(n^2). 
- Now the question is if we can avoid trying all pairs. The key here is that buy doesn't
depend on sell, but sell does depends on buy. In other words, for any given minute, if it is
an sell minute, there must be a buy minute that already happend before it. 
- Let's consider a set of subproblems SP[1...n], n is number of minutes. SP[i] represend the max 
profit selling on minute[i]. The solution to the original problem is then max(SP[1...n]). To solve SP[i],
we need to find the optimum buy minute between minute[1] and minute[i-1] (SP[1] = NIL becuase sell require at 
least 1 minute before it to buy). We can easily see that the optimum buy minute between 1 and i-1
should be the one that has minumum value. If we iterate starting from minute[1] and keep tracking
the min value so far, then by the time we want to solve SP[i], we would already have the 
answer of optimum buy minute. It takes O(1) time to solve each subproblem.
current_min_val = min(current_min_val, price[i-1])
SP[i] = price[i] - current_min_val
- The n subproblems dont' depend on each other's solution. However subproblem i-1 can greedly provide
the choice of buy day for subproblem i, which is the smaller between price of subproblem i-1's buy minute 
and price[i-1]. 

Runtime
O(n)

Space
O(n) if saves solution of all subproblems
O(1) if saves only the max value of all subproblems
"""

def get_max_profit(stock_prices: List[int]) -> int:
    number_of_minutes = len(stock_prices)
    max_profits = [float('-inf')] * number_of_minutes
    optimal_buy_sell_minutes = [(None, None)] * number_of_minutes
    current_best_buy_minute = 0

    for sell_minute in range(1, number_of_minutes):
        new_possible_buy_minute = sell_minute - 1
        if stock_prices[new_possible_buy_minute] < stock_prices[current_best_buy_minute]:
            current_best_buy_minute = new_possible_buy_minute
        current_best_buy_price = stock_prices[current_best_buy_minute]
        max_profits[sell_minute] = stock_prices[sell_minute] - current_best_buy_price
        optimal_buy_sell_minutes[sell_minute] = (current_best_buy_minute, sell_minute)
    max_profit_index = np.argmax(max_profits)
    return (
        max_profits[max_profit_index], optimal_buy_sell_minutes[max_profit_index]
    )

""" 2. Highest Product of 3
Problem
Given a list of integers, find the highest product you can get from three of the integers.
The input list_of_ints will always have at least three integers.

Analysis
- Brute force is to try all combinations of 3 integers from input list, runtime is n * (n-1) * (n-2) / (3 * 2) = O(n^3)
- If the input list is sorted descendingly, then can we simply take the top 3 integers as the solution? O(nlogn)
- Can we do better than sorting? Without sorting, we can set the first 3 elements as our choice. Then iterate through
the rest integers one by one, when ever there's a integer that is larger than the min of the currently choosen 3 integers,
we replace the min with that integer, by the end we will have 3 max integers
- But keep tracking 3 max integers might not give the answer of max product. The optimum solution might consist of 1 max positive
integer and 2 min negative integers. In this case, the above method won't work. The question is then how to not throw away
negative integers that could contribute to the max product?
- Another observation is there are only two ways any integer can make the max_product_of_3 bigger: 
    1. the integer is positive and it times a positive max_product_of_2 is bigger than max_product_of_3
    2. the integer is negative and it times a negative min_product_of_2 is bigger than max_prodcut_of_3
Therefore at interation of integer i, max_product_of_3 = max(
    max_product_of_3,
    i * max_product_of_2,
    i * min_product_of_2
)

- This can generalize to max_product_of_k by keep tracking of an array of max_products and min_products of size k, where 
max_products[i] (1 ≤ i ≤ k) is the max product of size i, similar for min_products[i]. Iterate through each integer integers[j]
of input list, updating max_products and min_products array. When 1 ≤ j ≤ k, update 1...j; then j > k, update 1...k.


5, 3, 1, -1, -5, -9

k = 3

j = 5
max_products = [5, 45, 225]
min_products = [-9, -45, -135]

"""
def highest_product_of_k(integers: List[int], k: int) -> int:
    n = len(integers)
    if k > n:
        raise ValueError

    max_products = [None] * k
    min_products = [None] * k
    max_products[0] = min_products[0] = integers[0]
    accumulated_product = integers[0]
    
    for i in range(1, n):
        current_int = integers[i]
        if i < k:
            accumulated_product *= current_int
            max_products[i] = min_products[i] = accumulated_product
            high_index = i
        else:
            high_index = k - 1
        
        for j in range(high_index, 0, -1):
            max_products[j] = max(
                max_products[j],
                max_products[j-1] * current_int,
                min_products[j-1] * current_int
            )
            min_products[j] = min(
                min_products[j],
                min_products[j-1] * current_int,
                max_products[j-1] * current_int
            )
        max_products[0] = max(max_products[0], current_int)
        min_products[0] = min(min_products[0], current_int)
    print(max_products, min_products)
    
    return max_products[-1]

""" 4. Product of All Other Numbers
Problem
You have a list of integers, and for each index you want to find the product of every integer except the integer at that index.
Write a function get_products_of_all_ints_except_at_index() that takes a list of integers and returns a list of the products.

For example, given:

  [1, 7, 3, 4]

your function would return:

  [84, 12, 28, 21]

by calculating:

  [7 * 3 * 4,  1 * 3 * 4,  1 * 7 * 4,  1 * 7 * 3]

Analysis
1. the subproblem is to calculate product of all other numbers for one integer
2. the subproblem can be solved by product_before_integer * product_after_integer
3. if we have an array products_before_integer, we can populate the array from start to end by tracking the accumulated product, O(n) time
4. same applies to products_after_integer

Runtime
O(n)

Space
O(n)
can save space by combining products_before_integer and products_after_integer into one 
"""

def get_products_of_all_ints_except_at_index(integers: List[int]) -> List[int]:
    products_except_integer_at_index = [None] * len(integers)
    accumulated_before_product = 1
    accumulated_after_product = 1

    for i in range(len(integers)):
        products_except_integer_at_index[i] = accumulated_before_product
        accumulated_before_product *= integers[i]
        
    for j in range(len(integers) - 1, -1, -1):
        products_except_integer_at_index[j] *= accumulated_after_product
        accumulated_after_product *= integers[j]
    
    return products_except_integer_at_index

""" 5. In-Place Shuffle
Problem
Write a function for doing an in-place ↴ shuffle of a list.
The shuffle must be "uniform," meaning each item in the original list must have the same probability of ending up in each spot in the final list.
Assume that you have a function get_random(floor, ceiling) for getting a random integer that is >= floor and <= ceiling.

Analysis
1. run get_random(0, len(list)-1) twice, then swap the two integers at the choosen indexes. repeat n times
2. the chance of first selcted integer going to any location is 1/n. the chance of being selected is also 1/n,
    so the total probability of any given integer end up in a given location is 1/n * 1/n * n = 1/n
3. The above solution is overly complicating the process, actually we can just run get_random once to get a integer
    then put it the the front of the input list. Then repeat the process with the rest of integers
    get_random(0, n-1) -> x -> list[0], list[x] = list[x], list[0]
    get_random(1, n-1) -> y -> list[1], list[y] = list[y], list[1]

"""

# Fisher-Yates shuffle (aka Knuth shuffle)
def shuffle(deck: List[str]) -> List[str]:
    for i in range(len(deck)):
        choice_index = get_random(i, len(deck) - 1)
        deck[i], deck[choice_index] = deck[choice_index], deck[i]
    return deck

def get_random(start, finish):
    return random.randint(start, finish)

def main():
    # get_max_profit_test_1 = [10, 7, 5, 8, 11, 9]
    # get_max_profit_res_1 = get_max_profit(get_max_profit_test_1)
    # print(get_max_profit_res_1)
    
    # highest_product_of_k_test_1 = [5, 3, 1, -1, -5, -9]
    # highest_product_of_k_res_1 = highest_product_of_k(highest_product_of_k_test_1, 3)
    # print(highest_product_of_k_res_1)
    
    # get_products_of_all_ints_except_at_index_test_1 = [1, 7, 3, 4]
    # get_products_of_all_ints_except_at_index_res_1 = get_products_of_all_ints_except_at_index(
    #     get_products_of_all_ints_except_at_index_test_1)
    # print(get_products_of_all_ints_except_at_index_res_1)
    
    shuffle_test_1 = [1, 2, 3, 4]
    shuffle_res_1 = shuffle(shuffle_test_1)
    print(shuffle_test_1)


if __name__ == '__main__':
    main()