import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Microsoft.Quantum.Samples.SimpleGrover import SearchForMarkedInput
import memory_profiler as MP
import time
from guppy import hpy

nQubits = 6
print(SearchForMarkedInput.simulate(nQubits=nQubits))
h = hpy()
print(h.heap())

print(b2-b1)
print(tim)