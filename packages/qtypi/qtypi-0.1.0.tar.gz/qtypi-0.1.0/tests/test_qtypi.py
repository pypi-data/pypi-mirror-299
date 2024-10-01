import unittest
import numpy as np
from qtypi.quantum_state import QuantumState
from qtypi.quantum_gates import QuantumGate

class TestQuantumState(unittest.TestCase):

    def test_quantum_state_initialization(self):
        """Test that QuantumState initializes with the correct state vector."""
        state = QuantumState([1, 0])
        np.testing.assert_array_equal(state.state_vector, np.array([1, 0]))

    def test_apply_hadamard_gate(self):
        """Test applying Hadamard gate to a quantum state."""
        state = QuantumState([1, 0])
        gate = QuantumGate.hadamard()
        new_state = state.apply_gate(gate)
        expected_state = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        np.testing.assert_almost_equal(new_state.state_vector, expected_state)

    def test_apply_pauli_x_gate(self):
        """Test applying Pauli-X gate to a quantum state."""
        state = QuantumState([1, 0])
        gate = QuantumGate.pauli_x()
        new_state = state.apply_gate(gate)
        expected_state = np.array([0, 1])
        np.testing.assert_array_equal(new_state.state_vector, expected_state)

    def test_apply_pauli_y_gate(self):
        """Test applying Pauli-Y gate to a quantum state."""
        state = QuantumState([1, 0])
        gate = QuantumGate.pauli_y()
        new_state = state.apply_gate(gate)
        expected_state = np.array([0, 1j])
        np.testing.assert_array_equal(new_state.state_vector, expected_state)

    def test_apply_pauli_z_gate(self):
        """Test applying Pauli-Z gate to a quantum state."""
        state = QuantumState([1, 0])
        gate = QuantumGate.pauli_z()
        new_state = state.apply_gate(gate)
        expected_state = np.array([1, 0])
        np.testing.assert_array_equal(new_state.state_vector, expected_state)

    def test_custom_gate(self):
        """Test applying a custom quantum gate."""
        custom_matrix = [[0, 1], [1, 0]]  # Equivalent to Pauli-X
        state = QuantumState([1, 0])
        gate = QuantumGate.custom_gate(custom_matrix)
        new_state = state.apply_gate(gate)
        expected_state = np.array([0, 1])
        np.testing.assert_array_equal(new_state.state_vector, expected_state)

if __name__ == '__main__':
    unittest.main()
