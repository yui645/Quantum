import math
from projectq import MainEngine
from projectq.ops import All,H, S, Rz, X, Measure
from projectq.meta import Compute, Control, Loop, Uncompute

def qft(eng, n):
    x = eng.allocate_qureg(n)
    for i in range(n):
        H | x[i]
        for j in range(i+1, n):
            Rz(2*math.pi/2**(j-i)) | x[j]
        S | x[i]
    All(Measure) | x
    eng.flush()
    return [int(qubit) for qubit in x]
if __name__ == "__main__":
    eng = MainEngine()
    print(qft(eng, 3))

