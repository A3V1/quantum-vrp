"""
Noise Models and Noisy Simulation

Implements various noise models for simulating quantum circuits
on realistic quantum hardware.
"""

from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, amplitude_damping_error


def create_noise_model(
    depolarizing_rate=0.01,
    amplitude_damping_rate=0.01
):
    """
    Create a noise model for simulation.
    
    Parameters
    ----------
    depolarizing_rate : float
        Single-qubit depolarizing error rate
    amplitude_damping_rate : float
        Amplitude damping error rate
        
    Returns
    -------
    NoiseModel
        The constructed noise model
    """
    
    noise_model = NoiseModel()
    
    # Single-qubit depolarizing error
    single_qubit_error = depolarizing_error(
        depolarizing_rate, 1
    )
    
    # Two-qubit depolarizing error
    two_qubit_error = depolarizing_error(
        depolarizing_rate, 2
    )
    
    # Amplitude damping error
    amplitude_error = amplitude_damping_error(
        amplitude_damping_rate
    )
    
    # Add errors to gates
    noise_model.add_all_qubit_quantum_error(
        single_qubit_error,
        ["rx", "ry", "rz"]
    )
    
    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx", "cz"]
    )
    
    noise_model.add_all_qubit_quantum_error(
        amplitude_error,
        ["measure"]
    )
    
    return noise_model


def create_noisy_simulator(noise_model):
    """
    Create a noisy simulator with the given noise model.
    
    Parameters
    ----------
    noise_model : NoiseModel
        The noise model to use
        
    Returns
    -------
    AerSimulator
        The noisy simulator
    """
    
    simulator = AerSimulator(
        noise_model=noise_model,
        method="statevector"
    )
    
    return simulator
