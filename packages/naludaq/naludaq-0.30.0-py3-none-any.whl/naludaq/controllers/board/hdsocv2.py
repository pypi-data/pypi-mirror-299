from logging import getLogger

from naludaq.communication import DigitalRegisters, AnalogRegisters, ControlRegisters
from naludaq.controllers.board.default import BoardController
from naludaq.helpers.semiton import SemitonABC

from typing import Iterable
import time


LOGGER = getLogger("naludaq.hdsocv2_trigger_controller")

BROADCAST = 64


class HDSoCv2BoardController(BoardController, SemitonABC):
    """Board controller for HDSoCv2.

    Only one instance of this class per board object is allowed.
    """

    @property
    def active_channels(self) -> list[int]:
        return self.board.params.get("active_channels", list())

    @active_channels.setter
    def active_channels(self, chans: list[int]):
        if not isinstance(chans, list):
            raise TypeError(f"active_channels must be a list, got {type(chans)}")
        if not all([isinstance(x, int) for x in chans]):
            raise TypeError("All channel numbers must be int")
        if not all(0 <= x < self.board.channels for x in chans):
            raise ValueError(
                f"all channels must be between 0 - {self.board.channels - 1}"
            )
        self.board.params["active_channels"] = chans

    def stop_readout(self):
        """Toggles the "stopacq" signal on the readout module.

        It's equivalent of asking it nicely to stop reading.
        """
        self.is_reading_out = False
        super().stop_readout()
        self.clear_buffer()

    def activate_channels(self, channels: list[int], dac_en_val: int = 1000):
        """Activate channels by powering the DACs and biases.

        Channels not specified will de diabled.

        Args:
            channels: list of channels to activate
            dac_en_val: value to set biases
        """
        dr = DigitalRegisters(self.board)
        ar = AnalogRegisters(self.board)
        prev_chan = self.active_channels
        for channel in range(self.board.channels):
            dr.write("selectchannel", channel)
            if (channel in channels) and (channel in prev_chan):
                continue
            elif channel in channels:
                active = True
            elif channel in prev_chan:
                active = False
            else:
                continue
            side = "left" if channel < 32 else "right"
            ar.write(f"channel_dac_bias_{side}", dac_en_val if active else 0)
            ar.write(f"channel_dac_bias_bias_{side}", dac_en_val if active else 0)
            ar.write(f"ch_fwd_{channel}", 6 if active else 2)
            ar.write(f"ch_rear_{channel}", 0x35 if active else 0x15)

        self.active_channels = channels
        dr.write("selectchannel", BROADCAST)

    def clear_buffer(self):
        """Clears the UART buffer on both CPU and FPGA side."""
        self._clear_fpga_buffer()
        super().clear_buffer()

    def _clear_fpga_buffer(self):
        """Resets the FPGA FIFO"""
        ControlRegisters(self.board).write("wave_fifo_rst", True)
        ControlRegisters(self.board).write("wave_fifo_rst", False)
        self.digital_reset()

    def set_loopback_enabled(self, enabled: bool):
        """Set whether serial loopback is enabled.

        Loopback can safely be disabled during most of the operations with the board.
        Loopback **must** be disabled when communicating over the serial interface.
        If serial communication with the ASIC is intended then this should run during startup and only be enabled as needed.

        Args:
            enabled (bool): True to enable loopback.

        Raises:
            TypeError if enabled is not a bool.
        """
        if not isinstance(enabled, bool):
            raise TypeError("Argument must be bool")
        OFF = "B0900002"
        ON = "B0900003"
        cmd = ON if enabled else OFF
        self._send_command(cmd)

    def read_scalers(self, channels: Iterable[int] | None = None) -> dict[int, int]:
        """Reads and returns all the digital scalar registers.

        The scalar registers are in two locations, one is the scal{ch} where the lower bits are
        stored, once that register is read, the scalhigh register is populated with the high bits.

        Args:
            channels (list[int]): list of channels to read scalars for.
                If not provided, scalars for all channels are read.

        Returns:
            list[int]: list of register read results for the channels selected.
                The list will not include values for disabled channels.

        Raises:
            ValueError: if a channel number in the list is invalid.
            TypeError: if channels is not a list or channel number is not an integer.
        """
        total_channels = self._get_total_channels()

        if channels is None:
            channels = range(total_channels)
        self._validate_channels_or_raise(channels)
        if self.is_reading_out:
            self.stop_readout()

        result = self._read_scalers(channels)
        return result

    def _read_scalers(self, channels: Iterable[int]) -> dict[int, int]:
        """Reads the scalars for the given channels, returns 0 for channels not selected."""
        result = {}
        for chan in channels:
            scalar = self.read_scalar(chan)
            result[chan] = scalar
        return result

    def read_scalar(self, channel: int, pause=0.001) -> int:
        # Select channel
        self._write_digital_register("selectchannel", channel)
        time.sleep(pause)
        # read bottom bits
        try:
            scal = self._read_digital_register("scal")
        except (KeyError, AttributeError) as e:
            LOGGER.warning("Can't read digital register scal due to: %s", e)
            scal = 0
        time.sleep(pause)
        # read top bits
        try:
            scalhigh = self._read_digital_register("scalhigh")
        except (KeyError, AttributeError) as e:
            LOGGER.warning("Can't read digital register scalhigh due to: %s", e)
            scalhigh = 0
        time.sleep(pause)
        # shift top bits up and add
        shift_amt = DigitalRegisters(self.board).registers["scal"]["bitwidth"]
        scal += scalhigh << shift_amt

        return scal
