namespace GroversTutorial {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Preparation;

    @EntryPoint()
    operation FactorizeWithGrovers2(number : Int) : Int {

    let markingOracle = MarkDivisor(number, _, _);
    let phaseOracle = ApplyMarkingOracleAsPhaseOracle(markingOracle, _);
    let size = BitSizeI(number);
    let nSolutions = 4;
    let nIterations = Round(PI() / 4.0 * Sqrt(IntAsDouble(size) / IntAsDouble(nSolutions)));

    use register = Qubit[size] {
        RunGroversSearch(register, phaseOracle, nIterations);
        let res = MultiM(register);
        return ResultArrayAsInt(res);
        // Verify whether the result is correct.
    }

}

    operation MarkDivisor (
        dividend : Int,
        divisorRegister : Qubit[],
        target : Qubit
    ) : Unit is Adj+Ctl {
        let size = BitSizeI(dividend);
        use (dividendQubits, resultQubits) = (Qubit[size], Qubit[size]);
        let xs = LittleEndian(dividendQubits);
        let ys = LittleEndian(divisorRegister);
        let result = LittleEndian(resultQubits);
        within{
            ApplyXorInPlace(dividend, xs);
            DivideI(xs, ys, result);
            ApplyToEachA(X, xs!);
        }
        apply{
            Controlled X(xs!, target);
        }
    }

    operation PrepareUniformSuperpositionOverDigits(digitReg : Qubit[]) : Unit is Adj + Ctl {
        PrepareArbitraryStateCP(ConstantArray(10, ComplexPolar(1.0, 0.0)), LittleEndian(digitReg));
    }

    operation ApplyMarkingOracleAsPhaseOracle(
        markingOracle : (Qubit[], Qubit) => Unit is Adj,
        register : Qubit[]
    ) : Unit is Adj {
        use target = Qubit();
        within {
            X(target);
            H(target);
        } apply {
            markingOracle(register, target);
        }
    }

    operation RunGroversSearch(register : Qubit[], phaseOracle : ((Qubit[]) => Unit is Adj), iterations : Int) : Unit {
        ApplyToEach(H, register);
        for _ in 1 .. iterations {
            phaseOracle(register);
            ReflectAboutUniform(register);
        }
    }

    operation ReflectAboutUniform(inputQubits : Qubit[]) : Unit {
        within {
            ApplyToEachA(H, inputQubits);
            ApplyToEachA(X, inputQubits);
        } apply {
            Controlled Z(Most(inputQubits), Tail(inputQubits));
        }
    }
}