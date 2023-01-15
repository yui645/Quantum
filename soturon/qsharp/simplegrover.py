import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Microsoft.Quantum.Samples.SimpleGrover import SearchForMarkedInput


nQubits = 6
print(SearchForMarkedInput.simulate(nQubits=nQubits))