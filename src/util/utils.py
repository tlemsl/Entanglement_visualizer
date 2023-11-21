def qubitmat2int(q_mat):
    """calculate the value from qubit matrix
    Args:
        q_mat (np.array): state matrix of qubit.
    Returns:
        v (int): qubit state value in decimal.
    """
    qubit_num, _ = q_mat.shape
    v = 0
    for i in range(1, qubit_num+1): 
        v += q_mat[-i][0].real * (2**(qubit_num-i))        
    v = int(v)
    
    return v