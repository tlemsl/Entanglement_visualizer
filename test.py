import unittest
import math
import numpy as np
import qubit.gates as qg
import qubit.qubit as qb


Q = qb.Qubit(2, 0)

# X0 = qg.X(2,0)
H0 = qg.H(2,0)

H1 = qg.H(2,1)

# G0 = X0
G1 = H0 * H1

print(f"H0:\n{H0}")
print(f"H1:\n{H1}")

print(len(G1*Q))
print(G1*Q)

print(f"H0*Q:{H0*Q}")

print(f"Q: {Q}")

# print(Q)
# print("len:", len(Q))
# print(G0*Q)
# print("len:", len(G0*Q))
# print(G1*G0*Q)
# print("len:", len(G1*G0*Q))