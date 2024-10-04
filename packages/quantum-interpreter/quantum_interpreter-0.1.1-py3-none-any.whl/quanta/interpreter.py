from qiskit import QuantumCircuit, Aer, execute

class QuantumNaturalLanguageInterpreter:
    def __init__(self):
        self.circuit = None
        self.backend = Aer.get_backend('qasm_simulator')

    def interpret(self, command):
        """Interprets the natural language command and translates to Qiskit."""
        command = command.lower()

        if "create a circuit" in command:
            self.create_circuit(command)
        elif "apply" in command and "gate" in command:
            self.apply_gate(command)
        elif "measure" in command: 
            self.measure_qubits(command)
        elif "run the circuit" in command:
            self.run_circuit(command)
        else:
            print("Command not recognized.")

    def create_circuit(self, command):
        """Create a quantum circuit based on the number of qubits."""
        num_qubits = int(command.split("with")[1].split("qubits")[0].strip())
        self.circuit = QuantumCircuit(num_qubits, num_qubits)
        print(f"Quantum circuit with {num_qubits} qubits created.")
        

    def apply_gate(self, command):
        """Apply gates like Hadamard, X, or CNOT."""
        if "hadamard" in command:
            qubit = int(command.split("to qubit")[1].strip())
            self.circuit.h(qubit)
            print(f"Hadamard gate applied to qubit {qubit}")
        elif "x gate" in command:
            qubit = int(command.split("to qubit")[1].strip())
            self.circuit.x(qubit)
            print(f"X gate applied to qubit {qubit}")
        elif "cnot gate" in command:
            control_qubit = int(command.split("from qubit")[1].split("to")[0].strip())
            target_qubit = int(command.split("to qubit")[1].strip())
            self.circuit.cx(control_qubit, target_qubit)
            print(f"CNOT gate applied from qubit {control_qubit} to qubit {target_qubit}")

    def measure_qubits(self, command):
        """Measure all or specific qubits."""
        if "all" in command:
            num_qubits = self.circuit.num_qubits
            self.circuit.measure(range(num_qubits), range(num_qubits))
            print(f"Measured all {num_qubits} qubits.")
        else:
            qubit = int(command.split("measure qubit")[1].strip())
            self.circuit.measure(qubit, qubit)
            print(f"Measured qubit {qubit}.")

    def run_circuit(self, command):
        """Run the quantum circuit on a simulator."""
        shots = int(command.split("run the circuit")[1].split("times")[0].strip())
        job = execute(self.circuit, self.backend, shots=shots)
        result = job.result()
        counts = result.get_counts(self.circuit)
        print(f"Execution result: {counts}")
