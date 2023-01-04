
#ショアのアルゴリズム
import matplotlib.pyplot as plt
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram
import memory_profiler as MP
import time

time_sta = time.perf_counter()

b1 = MP.memory_usage()[0]

def superposition (circuit, num_qubits):
    for i in range (num_qubits): 
        circuit.h(i)
    return circuit

def c_amodN (a, power, n_qubits):
    U = QuantumCircuit (4)
    for iteration in range(power):
        if a %2 != 0:
            for q in range (n_qubits//2):
                U.x (q)
    U=U.to_gate()
    U.name = "%i^%i mod N" % (a, power)
    c_U = U.control()
    return c_U

def controlled_U(circuit, num_qubit, a):
    for q in range(num_qubit):
        cir = c_amodN (a, 2**q, num_qubit) 
        circuit.append(cir, [q] + [i+num_qubit for i in range (num_qubit//2)]) 
    return circuit

def psi(circuit, num_qubit, a):
    circuit.x(-1)
    circuit.barrier()
    circuit =controlled_U(circuit, num_qubit, a)
    return circuit

def qft_dagger(circuit, num_qubits):
    qc = QuantumCircuit(num_qubits)
    for qubit in range(num_qubits//2):
        qc.swap(qubit, num_qubits-qubit-1)
    for j in range(num_qubits):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name= "QFT+"
    circuit.append(qc, range(num_qubits))
    return circuit

def qpf(circuit, num_qubits, a):
    circuit = superposition (circuit, num_qubits)
    circuit = psi (circuit, num_qubits, a)
    circuit.barrier()
    circuit = qft_dagger (circuit, num_qubits)
    circuit.barrier()
    for n in range (num_qubits): 
        circuit.measure (n, n)
    return circuit

from math import gcd
import numpy as np

def value_a(N):
    found = False
    while not found:
        a = np.random.randint(2, N)
        if gcd(a, N) == 1:
            found = True
    return a

from fractions import Fraction
def process_measurement (circuit, n_qubits, N):
    #Simulate Results
    aer_sim = Aer.get_backend ('aer_simulator')
    #Setting memory=True below allows us to see a list of each sequential reading
    t_circuit = transpile(circuit, aer_sim) 
    qobj = assemble (t_circuit, shots=1)
    result = aer_sim.run(qobj, memory=True).result()
    readings = result.get_memory()
    print("Register Reading:" + readings[0])
    phase = int (readings[0],2)/(2**n_qubits) 
    print("Corresponding Phase: %f" % phase)
    f = Fraction.from_float(phase).limit_denominator(N)
    q, r = f.numerator, f.denominator
    return r, phase

factor_found = False
attempt = 0
while not factor_found:
    attempt += 1
    print("\nAttempt %i:" % attempt)
    N = 15
    n_qubits = 2 * int(np.ceil(np.log(2 * N))) #2 times N^2
    data = QuantumRegister (n_qubits, name="data")
    target = QuantumRegister (n_qubits//2, name="target")
    classical = ClassicalRegister (n_qubits, "classical")
    circuit = QuantumCircuit (data, target, classical)
    circuit = qpf (circuit, n_qubits, value_a(N))
    circuit.draw(fold=-1)
    r, phase = process_measurement (circuit, n_qubits, N) 
    print("Result: r = %i" % r)
    if phase != 0:
        guesses = [value_a(N)**gcd((r//2)-1, N), gcd((value_a(N)**r//2)+1, N)] 
        print("Guessed Factors: %i and %i" % (guesses [0], guesses[1]))
    #Guesses for factors are gcd (7/2} +1, 15)
        for guess in guesses:
            if guess not in [1,N] and (N % guess) == 0: 
                print("*** Non-trivial factor found: %i ***" % guess)
                factor_found = True
                print("*** Non-trivial factors found: %s and %s ***" % (guess, N//guess)) 

b2 = MP.memory_usage()[0]
time_end = time.perf_counter()
tim = time_end- time_sta
print(b2-b1)
print(tim)