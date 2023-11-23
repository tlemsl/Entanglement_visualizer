def qubitmat2int(q_mat):
    """calculate the value from qubit matrix
    Args:
        q_mat (np.array): state matrix of qubit.
    Returns:
        v (int): qubit state value in decimal.
    """
    qubit_num, _ = q_mat.shape
    v = 0
    for i in range(qubit_num):
        if q_mat[i] == 1:
            v = i     
    return v