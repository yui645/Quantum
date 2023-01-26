namespace Microsoft.Quantum.qft {
open Microsoft.Quantum.Intrinsic;
open Microsoft.Quantum.Math;
open Microsoft.Quantum.Measurement;
open Microsoft.Quantum.Convert;
open Microsoft.Quantum.Arrays;
open Microsoft.Quantum.Canon;

operation QFT (qs : Qubit[]) : Unit is Adj+Ctl {
    let nQubits = Length(qs);

        for i in 0 .. nQubits - 1
        {
            H(qs[i]);
            for j in i + 1 .. nQubits - 1
            {
                Controlled R1Frac([qs[j]], (1, j - i, qs[i]));
            }
        }
        Microsoft.Quantum.Canon.SwapReverseRegister(qs);
}
}