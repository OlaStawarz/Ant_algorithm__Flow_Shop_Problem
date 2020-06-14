from copy import deepcopy
import random
import sys
import numpy as np
import math

def read(filepath):
    data = []
    parameters = []
    with open(filepath) as f:
        name = f.readline()
        n, m = [int(x) for x in next(f).split()]
        data_temp = [[int(x) for x in line.split()] for line in f]
    for i in range(0, len(data_temp)):
        el = data_temp[i][1::2]
        data.append(el)
    data.pop()  # just to remove blank line at the end of file
    parameters.append(n)
    parameters.append(m)
    return name, parameters, data


W = []
S = []  #matrix - duration of job on particular machine
C = []  #matrix - end time of job on particular machines


# calculate best Cmax
def calculate(data):
    S.clear()
    C.clear()
    J = deepcopy(data)
    czas_r_tab = []
    czas_z_tab = []
    czas_z = 0
    for m in range(0, parameters[1]):
        for j in range(0, len(J)):
            if m == 0:
                czas_r = czas_z
                czas_z = czas_r + J[j][m]
            else:
                if j == 0:
                    czas_r = C[m-1][j]
                    czas_z = czas_r + J[j][m]
                else:
                    czas_r = max(C[m-1][j], czas_z)
                    czas_z = czas_r + J[j][m]
            czas_r_tab.append(czas_r)
            czas_z_tab.append(czas_z)
        S.append(czas_r_tab)
        C.append(czas_z_tab)
        czas_r_tab = []
        czas_z_tab = []
    return C[-1][-1]


def swapPositions(list, pos1, pos2):
    l = deepcopy(list)
    first_ele = l.pop(pos1)
    second_ele = l.pop(pos2-1)
    l.insert(pos1, second_ele)
    l.insert(pos2, first_ele)
    return l


def insert(list, pos1, pos2):
    l = deepcopy(list)
    first_ele = l.pop(pos1)
    l.insert(pos2, first_ele)
    return l


def reduceTemperature(T, T0):
    return 0.97 * T


T_end = 0.01
k = 1
e = 2.71828


def SA(data, choice_L, T0):
    T = T0
    pi = deepcopy(data)
    pi_prim = deepcopy(pi)
    L = choice_L
    while T > T_end:
        for w in range(k, L):
            i = random.randint(0, parameters[0]-1)
            j = random.randint(0, parameters[0]-1)
            new_pi = insert(pi, i, j-1)
            C_max = calculate(pi)
            C_max_new = calculate(new_pi)
            if C_max_new > C_max:
                r = random.random()
                delta_C_max = C_max - C_max_new
                pom = e ** (delta_C_max/T)
                if r >= pom:
                    new_pi = pi.copy()
            pi = new_pi
            if calculate(pi) < calculate(pi_prim):
                pi_prim = pi.copy()
        T = reduceTemperature(T, T0)
    return pi_prim


def ant_algorithm():
    J = deepcopy(N)
    final_array = []
    final_arrays = []
    results = []
    left_jobs = 0
    j = parameters[0] - 1
    feromones = [[1 for i in range(parameters[0])] for j in range(parameters[0])]
    for n in range(0, parameters[0]):    # implementation of ACO - we have as many ants as jobs
        for pos in range(0, len(J)):    # find jobs for first position - initialize trial
            for k in range(0, len(J)):  # count feromones of non-scheduled jobs
                if J[k] not in final_array:
                    left_jobs += feromones[pos][k]
            for i in range(0, len(J)):  # calculate probability of choosing particular job
                if J[i] not in final_array:
                    if left_jobs == 0:
                        p = 0
                    else:
                        p = feromones[pos][i] / left_jobs
                    el = J[i]
                    final_array.insert(pos, el)
                    C_best = calculate(final_array)
                    T_new = p * feromones[pos][i] + 1 / C_best
                    feromones[pos][i] = T_new
                    final_array.remove(el)
                else:
                    feromones[pos][i] = 0
            temp = np.array(feromones[pos])
            normalized = temp / temp.sum()  #normalize array so to sum of feromones eqauls 1
            feromones[pos] = normalized.tolist()
            feromones_sum = sum(normalized)
            r = random.uniform(0, feromones_sum)
            count = 0
            for i in range(0, len(feromones[pos])): #choosing the job for pos with some probability
                count += normalized[i]
                if count > r:
                    j = i
                    break
            final_array.insert(pos, J[j])
            left_jobs = 0
        result = calculate(final_array)
        results.append(result)
        final_arrays.append(deepcopy(final_array))
        final_array.clear()
    minimum = results.index(min(results))
    return final_arrays[minimum]    # return the minimum Cmax of found trials


name, parameters, data = read('ta021.txt')
N = deepcopy(data)
best_trial = ant_algorithm()
print(calculate(SA(best_trial, int(math.sqrt(parameters[0])), 100)))





