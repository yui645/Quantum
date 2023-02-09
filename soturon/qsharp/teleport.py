import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Teleport import Teleport
from guppy import hpy

print(Teleport.simulate())
h = hpy()
print(h.heap())