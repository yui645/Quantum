
#グローバーのアルゴリズム
import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
import memory_profiler as MP
import time

time_sta = time.perf_counter()

b1 = MP.memory_usage()[0]

def phase_oracle(circuit, register):
    circuit.cz(register[0], register[1])
def inversion_about_average(circuit, register):
    """Apply inversion about the average step of Grover's algorithm."""
    circuit.h(register)
    circuit.x(register)    
    circuit.cz(register[0], register[1])
    circuit.x(register)
    circuit.h(register)
qr = QuantumRegister(2)
cr = ClassicalRegister(2)
groverCircuit = QuantumCircuit(qr,cr)
groverCircuit.h(qr) 
phase_oracle(groverCircuit, qr)
inversion_about_average(groverCircuit, qr) 
groverCircuit.measure(qr,cr) 
groverCircuit.draw(output="mpl")

b2 = MP.memory_usage()[0]
time_end = time.perf_counter()
tim = time_end- time_sta
print(b2-b1)
print(tim)