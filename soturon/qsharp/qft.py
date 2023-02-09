import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Microsoft.Quantum.qft import QFT
from guppy import hpy

qs=3
print(QFT.simulate(qs=qs))
h = hpy()
print(h.heap())