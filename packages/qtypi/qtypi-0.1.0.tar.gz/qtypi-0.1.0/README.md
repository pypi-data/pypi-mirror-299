
# qtypi

`qtypi` is a Python library for performing quantum computations using linear algebra. It provides tools to create and manipulate quantum states and apply quantum gates.

## Table of Contents
- [Installation](#installation)
- [Creating Quantum States](#creating-quantum-states)
- [Applying Quantum Gates](#applying-quantum-gates)
- [Available Quantum Gates](#available-quantum-gates)
- [Example Usage](#example-usage)
  - [Creating and Applying Gates](#creating-and-applying-gates)
  - [Custom Quantum Gates](#custom-quantum-gates)
  - [Creating the |+> State](#creating-the-plus-state)
- [License](#license)

## Installation

You can install `qtypi` using pip:

```bash
pip install qtypi
```

## Creating Quantum States

To create a quantum state, instantiate the `QuantumState` class by passing a state vector (as a list or numpy array).

```python
from qtypi.quantum_state import QuantumState

# Create the |0> state
state_zero = QuantumState([1, 0])

# Create the |1> state
state_one = QuantumState([0, 1])
```

## Applying Quantum Gates

Quantum gates can be applied to quantum states using the `apply_gate` method of the `QuantumState` class. The library includes commonly used gates, such as Hadamard, Pauli-X, Pauli-Y, Pauli-Z, Phase, and CNOT gates.

```python
from qtypi.quantum_gates import QuantumGate

# Create a Hadamard gate
hadamard_gate = QuantumGate.hadamard()

# Apply the Hadamard gate to the |0> state
new_state = state_zero.apply_gate(hadamard_gate)

print(new_state)
```

## Available Quantum Gates

The following gates are available as static methods in the `QuantumGate` class:

- **Hadamard Gate**: `QuantumGate.hadamard()`
- **Pauli-X Gate**: `QuantumGate.pauli_x()`
- **Pauli-Y Gate**: `QuantumGate.pauli_y()`
- **Pauli-Z Gate**: `QuantumGate.pauli_z()`
- **Phase Gate**: `QuantumGate.phase(theta)`
- **CNOT Gate**: `QuantumGate.cnot()`
- **Custom Gate**: `QuantumGate.custom_gate(matrix)`

## Example Usage

### Creating and Applying Gates

Here’s a complete example of creating a quantum state, applying a Hadamard gate, and printing the result:

```python
from qtypi.quantum_state import QuantumState
from qtypi.quantum_gates import QuantumGate

# Initialize the |0> state
state = QuantumState([1, 0])

# Create a Hadamard gate
hadamard_gate = QuantumGate.hadamard()

# Apply the Hadamard gate to the |0> state
new_state = state.apply_gate(hadamard_gate)

# Print the resulting quantum state
print("New State after applying Hadamard:", new_state)
```

### Custom Quantum Gates

You can create and apply custom quantum gates using a matrix of your choice. For example:

```python
import numpy as np
from qtypi.quantum_state import QuantumState
from qtypi.quantum_gates import QuantumGate

# Define a custom matrix
custom_matrix = np.array([[0, 1], [1, 0]])  # Equivalent to Pauli-X gate

# Create the custom gate
custom_gate = QuantumGate.custom_gate(custom_matrix)

# Apply it to a |0> state
state = QuantumState([1, 0])
new_state = state.apply_gate(custom_gate)

print("New State after applying custom gate:", new_state)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.