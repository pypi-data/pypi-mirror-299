from dataclasses import dataclass
from math import sqrt, pi
from typing import Optional

from respice.components.PeriodicVoltageSource import PeriodicVoltageSource


@dataclass(eq=False)
class VoltageSourceTriangular(PeriodicVoltageSource):
    """
    A triangular voltage supply.

    By default the voltage ranges between `+amplitude` and `-amplitude`.
    To make the signal from `0` to `a`, set `offset = amplitude = a / 2`.

    amplitude:
        The voltage amplitude (peak-to-peak, measured in Volts).
    offset:
        The voltage offset of the signal (measured in Volts).
    """
    amplitude: float = 1.0
    offset: float = 0.0

    @property
    def effective_amplitude(self):
        r"""
        The effective amplitude (:math:`A_{RMS}`) depends not only on the amplitude, but also on the offset and duty
        cycle.
        According to the formula for RMS (see https://en.wikipedia.org/wiki/Root_mean_square and
        https://en.wikipedia.org/wiki/RMS_amplitude)

        .. math::

             A_{RMS} &= \sqrt{\frac{1}{T} \int_{0}^{T}{f^2(t) dt}} \\
                     &= \sqrt{
                            \frac{1}{T}
                            \left (
                                \int_{0}^{T/2}{\left( \frac{4}{T} A \cdot t - A + o \right)^2 dt} +
                                \int_{T/2}^{T}{\left( -\frac{4}{T} A \cdot t + 3 A + o \right)^2 dt}
                            \right )
                        } \\
                     &= \sqrt{
                            \frac{1}{3} A^2 + o^2
                        }

        :return:
            The effective amplitude voltage (measured in Volts).
        """
        return sqrt(self.amplitude**2 / 3 + self.offset**2)

    def get_signal(self, phase: float) -> float:
        normalized_phase = 2 * phase / pi
        return (normalized_phase - 1 if normalized_phase < 2 else 3 - normalized_phase) * self.amplitude + self.offset

    def next_signal_event(self, phase1: float, phase2: float) -> Optional[float]:
        if phase1 == 0.0:
            return 0.0

        if phase1 <= pi < phase2:
            return pi

        return None
