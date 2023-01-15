import qsharp
qsharp.packages.add("Microsoft.Quantum.Numerics")
qsharp.reload()
from Teleport import Teleport
import memory_profiler as MP
import time

time_sta = time.perf_counter()

b1 = MP.memory_usage()[0]

print(Teleport.simulate())

b2 = MP.memory_usage()[0]
time_end = time.perf_counter()
tim = time_end- time_sta
print(b2-b1)
print(tim)