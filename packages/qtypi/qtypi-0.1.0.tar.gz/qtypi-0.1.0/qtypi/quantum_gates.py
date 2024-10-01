import numpy as np
from .quantum_state import QuantumState  # Importing QuantumState

class QuantumGate:
    def __init__(self, matrix):
        """Initialize a quantum gate with a matrix."""
        self.matrix = np.array(matrix)

    def apply(self, quantum_state):
        """Apply the gate to a quantum state."""
        return QuantumState(np.dot(self.matrix, quantum_state.state_vector))

    @staticmethod
    def hadamard():
        """Return a Hadamard gate."""
        return QuantumGate([[1/np.sqrt(2), 1/np.sqrt(2)], 
                            [1/np.sqrt(2), -1/np.sqrt(2)]])

    @staticmethod
    def pauli_x():
        """Return a Pauli-X gate."""
        return QuantumGate([[0, 1], [1, 0]])

    @staticmethod
    def pauli_y():
        """Return a Pauli-Y gate."""
        return QuantumGate([[0, -1j], [1j, 0]])

    @staticmethod
    def pauli_z():
        """Return a Pauli-Z gate."""
        return QuantumGate([[1, 0], [0, -1]])

    @staticmethod
    def phase(theta):
        """Return a phase gate."""
        return QuantumGate([[1, 0], [0, np.exp(1j * theta)]])

    @staticmethod
    def cnot():
        """Return a CNOT gate for two qubits."""
        return QuantumGate([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0]])

    @staticmethod
    def custom_gate(matrix):
        """Create a custom quantum gate."""
        return QuantumGate(matrix)
