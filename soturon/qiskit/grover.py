
#グローバーのアルゴリズム
import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

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