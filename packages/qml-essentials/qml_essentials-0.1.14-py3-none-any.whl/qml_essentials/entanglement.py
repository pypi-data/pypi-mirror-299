from typing import Callable, Optional, Any
import pennylane as qml
import pennylane.numpy as np

import logging

log = logging.getLogger(__name__)


class Entanglement:

    @staticmethod
    def meyer_wallach(
        model: Callable,  # type: ignore
        n_samples: int,
        seed: Optional[int],
        **kwargs: Any
    ) -> float:
        """
        Calculates the entangling capacity of a given quantum circuit
        using Meyer-Wallach measure.

        Args:
            model (Callable): Function that models the quantum circuit. It must
                have a `n_qubits` attribute representing the number of qubits.
                It must accept a `params` argument representing the parameters
                of the circuit.
            n_samples (int): Number of samples per qubit.
            seed (Optional[int]): Seed for the random number generator.
            kwargs (Any): Additional keyword arguments for the model function.

        Returns:
            float: Entangling capacity of the given circuit. It is guaranteed
                to be between 0.0 and 1.0.
        """

        def _meyer_wallach(
            evaluate: Callable[[np.ndarray], np.ndarray],
            n_qubits: int,
            samples: int,
            params: np.ndarray,
        ) -> float:
            """
            Calculates the Meyer-Wallach sampling of the entangling capacity
            of a quantum circuit.

            Args:
                evaluate (Callable[[np.ndarray], np.ndarray]): Callable that
                    evaluates the quantum circuit It must accept a `params`
                    argument representing the parameters of the circuit and may
                    accept additional keyword arguments.
                n_qubits (int): Number of qubits in the circuit
                samples (int): Number of samples to be taken
                params (np.ndarray): Parameters of the instructor. Shape:
                    (samples, *model.params.shape)

            Returns:
                float: Entangling capacity of the given circuit. It is
                    guaranteed to be between 0.0 and 1.0
            """
            assert (
                params.shape[0] == samples
            ), "Number of samples does not match number of parameters"

            mw_measure = np.zeros(samples, dtype=complex)
            qb = list(range(n_qubits))

            for i in range(samples):
                # implicitly set input to none in case it's not needed
                kwargs.setdefault("inputs", None)
                # explicitly set execution type because everything else won't work
                U = evaluate(params=params[i], execution_type="density", **kwargs)

                entropy = 0

                for j in range(n_qubits):
                    density = qml.math.partial_trace(U, qb[:j] + qb[j + 1 :])
                    entropy += np.trace((density @ density).real)

                mw_measure[i] = 1 - entropy / n_qubits

            mw = 2 * np.sum(mw_measure.real) / samples

            # catch floating point errors
            return min(max(mw, 0.0), 1.0)

        if n_samples > 0:
            assert seed is not None, "Seed must be provided when samples > 0"
            # TODO: maybe switch to JAX rng
            rng = np.random.default_rng(seed)
            params = rng.uniform(0, 2 * np.pi, size=(n_samples, *model.params.shape))
        else:
            if seed is not None:
                log.warning("Seed is ignored when samples is 0")
            n_samples = 1
            params = model.params.reshape(1, *model.params.shape)

        entangling_capability = _meyer_wallach(
            evaluate=model,
            n_qubits=model.n_qubits,
            samples=n_samples,
            params=params,
        )

        return float(entangling_capability)
