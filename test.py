import unittest
import math
import numpy as np
import qubit.gates as qg
import qubit.qubit as qb


Q = qb.Qubit(2, 0)
X0 = qg.X(2,0)
Z1 = qg.Z(2,1)
H0 = qb.H(2,0)

G1 = X0 * Z1
G2 = H0 * Z1
G3 = H0

print(G1 * Q)
print(G2 * G1 * Q)
print(G3* G2 * G1 * Q)
