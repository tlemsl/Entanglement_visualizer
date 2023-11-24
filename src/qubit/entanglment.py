"""
Quantum Entanglement Analysis Module

This module provides functionality for analyzing quantum entanglement in quantum
computing. It includes methods for calculating the entanglement of quantum states
represented as matrices, reordering these matrices based on quantum gates, and
determining the proportional relationship between quantum states.


The module utilizes complex mathematical operations and quantum omputing 
concepts, specifically focusing on the manipulation and analysis of qubit states.
It is intended for use in quantum computing simulations and research.

Author: Minjong Kim
Email: tlemsl@dgist.ac.kr
Website: https://github.com/tlemsl/Entanglement_visualizer

Functions:
    entanglement(mat): Calculates the entanglement of 
                       a given quantum state matrix.
    split(mat, split=2, step=-1): Splits a matrix into smaller matrices.
    reorder(mat, index_set, index_status): Reorders a matrix based on index sets.
    pop(mat, n): Pops elements from a matrix.
    zero(lst): Determines if all elements in a list are approximately zero.
    proportional(vec_set): Checks if elements of 
                           two lists are proportional to each other.
"""

import math
import itertools
import numpy as np
import qubit.gates as qg

Threshold = complex(0.0001)


def entanglement(mat):
    """Calculates the entanglement of a matrix.

    Args:
        mat (numpy.ndarray): A matrix representing quantum states.

    Returns:
        list: A list of set of entangled states.
    """
    n = int(math.log2(mat.shape[0]))
    index_state = list(range(n))
    seperatable_set = set()

    for i in range(n):
        mat, index_state = reorder(mat, {i}, index_state)
        sep_vec = split(mat, step=2**(n - 1))
        if proportional(sep_vec):
            seperatable_set.add(i)

    mat, index_state = reorder(mat, seperatable_set, index_state)
    mat = pop(mat, len(seperatable_set))
    if seperatable_set:
        index_state = index_state[:-len(seperatable_set)]
    return _entanglement(mat, index_state, 2, [])


def _entanglement(mat, index_state, r, ret):
    """Helper function to calculate entanglement recursively.

    Args:
        mat (numpy.ndarray): A matrix representing quantum states.
        index_state (list): List of index states.
        r (int): Recursive depth (Collection number).
        ret (list) : Recursion output list

    Returns:
        list : A list of set of entangled states.
    """
    n = len(index_state)
    combinations = itertools.combinations(index_state, r)
    if n <= 3 or r > (n // 2):
        ret.append(set(index_state))
        return ret

    seperatable_set = set()
    for combination in combinations:
        mat, index_state = reorder(mat, set(combination), index_state)
        sep_vec = split(mat, step=2**(n - r), split=2**r)
        vec_combinations = itertools.combinations(sep_vec, 2)
        for vec_comb in vec_combinations:
            if not proportional(vec_comb):
                break
        else:
            seperatable_set = set(combination)
            break
    else:
        return _entanglement(mat, index_state, r + 1, ret)

    mat, index_state = reorder(mat, seperatable_set, index_state)
    mat = pop(mat, len(seperatable_set))
    index_state = index_state[:-len(seperatable_set)]
    ret.append(seperatable_set)
    _entanglement(mat, index_state, r, ret)
    return ret


def split(mat, split=2, step=-1):
    """Splits a matrix into smaller matrices.

    Args:
        mat (numpy.ndarray): The matrix to split.
        split (int, optional): Number of splits. Defaults to 2.
        step (int, optional): Step size for splitting. Defaults to -1.

    Returns:
        list: List of split matrices.
    """
    l = int(mat.shape[0])
    if step == -1:
        step = l // split
    ret = [[] for _ in range(split)]
    for i in range(l // step):
        for s in range(step):
            ret[i % split].append(mat[i * step + s, 0])
    return ret


def reorder(mat, index_set: set, index_status):
    """Reorders a matrix based on index sets.

    Args:
        mat (numpy.ndarray): The matrix to reorder.
        index_set (set): Set of indices to reorder.
        index_status (list): Current index status.

    Returns:
        tuple: Reordered matrix and updated index status.
    """
    ret = np.array(mat)
    n = int(math.log2(mat.shape[0]))
    selected_set_n = len(index_set)
    need_to_swap_set = index_set - set(index_status[-selected_set_n:])
    swapable_set = set(index_status[-selected_set_n:]) - index_set

    for idx in need_to_swap_set:
        other = swapable_set.pop()
        idx_idx = index_status.index(idx)
        other_idx = index_status.index(other)
        gate = qg.Swap(n, idx_idx, other_idx)
        index_status[idx_idx], index_status[other_idx] = (
            index_status[other_idx], index_status[idx_idx])
        ret = np.dot(gate.mat, ret)
    return ret, index_status


def pop(mat, n):
    """Pops elements from a matrix.

    Args:
        mat (numpy.ndarray): The matrix to pop from.
        n (int): Number of elements to pop.

    Returns:
        numpy.ndarray: The remaining elements after popping.
    """
    ret_candidates = split(mat, 2**n)
    for candidate in ret_candidates:
        if not zero(candidate):
            return np.array(candidate,
                            dtype=np.complex128).reshape(len(candidate), 1)


def zero(lst):
    """Determines if all elements in a list are approximately zero.

    Args:
        lst (list): A list of numeric values.

    Returns:
        bool: True if all elements are close to zero, False otherwise.
    """
    return all(abs(v) <= Threshold for v in lst)


def proportional(vec_set):
    """Checks if elements of two lists are proportional to each other.

    Args:
        vec_set (set): A set containing two lists of numeric values.

    Returns:
        bool: True if elements of the first list are proportional to the second list, 
              False otherwise.
    """
    list1, list2 = vec_set
    if any(zero(vec) for vec in vec_set):
        return True

    val = _calculate_proportional_value(list1, list2)
    for v1, v2 in zip(list1, list2):
        if not _is_proportional(v1, v2, val):
            return False
    return True


def _calculate_proportional_value(list1, list2):
    """Calculates the proportional value for two lists.

    Args:
        list1 (list): First list of numeric values.
        list2 (list): Second list of numeric values.

    Returns:
        complex: Proportional value or infinity if not proportional.
    """
    if abs(list2[0]) > Threshold:
        return complex(list1[0] / list2[0])
    elif abs(list1[0]) < Threshold:
        return complex(1)
    else:
        return complex(math.inf)


def _is_proportional(v1, v2, val):
    """Checks if two values are proportional to a given value.

    Args:
        v1 (numeric): First value.
        v2 (numeric): Second value.
        val (complex): Proportional value.

    Returns:
        bool: True if proportional, False otherwise.
    """
    if abs(v2) > Threshold:
        temp = complex(v1 / v2)
    elif abs(v1) < Threshold:
        temp = complex(1)
    else:
        temp = complex(math.inf)

    return abs(temp - val) <= abs(Threshold)
