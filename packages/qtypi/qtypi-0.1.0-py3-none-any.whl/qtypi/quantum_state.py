import numpy as np

class QuantumState:
    def __init__(self, state_vector):
        """Initialize a quantum state with a state vector."""
        self.state_vector = np.array(state_vector)

    def apply_gate(self, gate):
        """
        Apply a quantum gate (instance of QuantumGate) to the current state.

        Parameters:
        - gate (QuantumGate): The quantum gate to be applied.

        Returns:
        - QuantumState: The new quantum state after applying the gate.
        """
        from .quantum_gates import QuantumGate
        if isinstance(gate, QuantumGate):
            new_state_vector = np.dot(gate.matrix, self.state_vector)
            return QuantumState(new_state_vector)
        else:
            raise ValueError("Input must be an instance of QuantumGate.")
    
    def __repr__(self):
        return f"QuantumState({self.state_vector})"
