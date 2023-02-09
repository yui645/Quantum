import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Microsoft.Quantum.shor2 import QuantumPeriodFinding
from guppy import hpy

N=15
a=7
print(QuantumPeriodFinding.simulate(num=N,a=a))
h = hpy()
print(h.heap())
