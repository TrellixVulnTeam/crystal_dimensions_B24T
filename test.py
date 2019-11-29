lst = [1, 4, 3, 5, 7, 8]
total = 12

def solution(l, t):
    # Your code here
    subset = []
    new_list = l
                         
    while len(subset) == 0:
        new_n = 0
        x = 0
        while new_n <= t:
            if new_n == t:
                for i in range(x):
                    r_index = max(indx for indx, val in enumerate(new_list) if val == l[i])
                    subset.append(int(r_index))
                subset = [subset[0], subset[-1]]
                subset.sort()
                break
            try:
                new_n = new_n + l[x]
                x +=1
            except IndexError:
                subset = [-1, -1]
                break
        l[1:]

    return subset

def solution_2(l, t):
    # Your code here
    subset = []
    new_list = l
                         
    while len(subset) == 0:
        new_n = 0
        x = 0
        while new_n <= t:
            if new_n == t:
                for i in range(x):
                    #r_index = max(indx for indx, val in enumerate(new_list) if val == l[i])
                    subset.append(new_list.index(l[i]))
                subset = [subset[0], subset[-1]]
                break
            try:
                new_n = new_n + l[x]
                x +=1
            except IndexError:
                subset = [-1, -1]
                break
        l = l[1:]

    return subset