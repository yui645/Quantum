namespace Microsoft.Quantum.Samples.SimpleGrover {
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;

    /// # Summary
    /// This operation applies Grover's algorithm to search all possible inputs
    /// to an operation to find a particular marked state.
    @EntryPoint()
    operation SearchForMarkedInput(nQubits : Int) : Result[] {
        use qubits = Qubit[nQubits];
        // Initialize a uniform superposition over all possible inputs.
        PrepareUniform(qubits);
        // The search itself consists of repeatedly reflecting about the
        // marked state and our start state, which we can write out in Q#
        // as a for loop.
        for idxIteration in 0..NIterations(nQubits) - 1 {
            ReflectAboutMarked(qubits);
            ReflectAboutUniform(qubits);
        }
        // Measure and return the answer.
        return ForEach(MResetZ, qubits);
    }

    operation ReflectAboutUniform(inputQubits : Qubit[]) : Unit {
        within {
            // Transform the uniform superposition to all-zero.
            Adjoint PrepareUniform(inputQubits);
            // Transform the all-zero state to all-ones
            PrepareAllOnes(inputQubits);
        } apply {
            // Now that we've transformed the uniform superposition to the
            // all-ones state, reflect about the all-ones state, then let
            // the within/apply block transform us back.
            ReflectAboutAllOnes(inputQubits);
        }
    }

    operation ReflectAboutAllOnes(inputQubits : Qubit[]) : Unit {
        Controlled Z(Most(inputQubits), Tail(inputQubits));
    }

    operation PrepareAllOnes(inputQubits : Qubit[]) : Unit is Adj + Ctl {
        ApplyToEachCA(X, inputQubits);
    }

    operation PrepareUniform(inputQubits : Qubit[]) : Unit is Adj + Ctl {
        ApplyToEachCA(H, inputQubits);
    }


    operation ReflectAboutMarked(inputQubits : Qubit[]) : Unit {
        Message("Reflecting about marked state...");
        use outputQubit = Qubit();
        within {
            // We initialize the outputQubit to (|0⟩ - |1⟩) / √2,
            // so that toggling it results in a (-1) phase.
            X(outputQubit);
            H(outputQubit);
            // Flip the outputQubit for marked states.
            // Here, we get the state with alternating 0s and 1s by using
            // the X instruction on every other qubit.
            ApplyToEachA(X, inputQubits[...2...]);
        } apply {
            Controlled X(inputQubits, outputQubit);
        }
    }

    /// # Summary
    /// Returns the number of Grover iterations needed to find a single marked
    /// item, given the number of qubits in a register.
    function NIterations(nQubits : Int) : Int {
        let nItems = 1 <<< nQubits; // 2^numQubits
        // compute number of iterations:
        let angle = ArcSin(1. / Sqrt(IntAsDouble(nItems)));
        let nIterations = Round(0.25 * PI() / angle - 0.5);
        return nIterations;
    }

}
