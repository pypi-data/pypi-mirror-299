"""
"""
from naludaq.controllers.trigger.hdsoc import TriggerControllerHdsoc
from naludaq.communication import AnalogRegisters

# {TIA_en, TIA_DC_adj[0:6], tsel, ch_en, scv_legacy, tsgn}
TSEL_BIT = 3
TSGN_BIT = 0


class TriggerControllerHdsocv2(TriggerControllerHdsoc):
    def _set_tsel_enabled(self):
        """Enables TSEL (Trigger Select) for all channels on the board.

        This method creates a dictionary where each channel on the board is set to True,
        indicating that TSEL is enabled for that channel. It then calls the `enable_tsel`
        method with this dictionary to apply the settings.
        """
        channels = {i: True for i in range(self.board.channels)}
        self.enable_tsel(channels)

    def set_trigger_edge(self, channels: dict[int, bool]):
        """Set trigger edge per channel, either rising=True, or rising=False

        Args:
            channels (dict[int, bool]): keys are channel numbers,
                                        value are True (rising)
                                        or false (falling).

        Raises:
            TypeError if channels is not a dict.
        """
        if not isinstance(channels, dict):
            raise TypeError("channels must be a dict")

        self._update_fwd_regs(channels, TSGN_BIT)

    def enable_tsel(self, channels: dict[int, bool]):
        """Enable or disable TSEL for specified channels.

        Args:
            channels (dict[int, bool]): keys are channel numbers,
                                        values are True (enable)
                                        or False (disable).

        Raises:
            TypeError: If the channels argument is not a dictionary.
        """
        if not isinstance(channels, dict):
            raise TypeError("channels must be a dict")

        self._update_fwd_regs(channels, TSEL_BIT)

    def _update_fwd_regs(self, channels: dict[int, bool], bitpos: int):
        """Updates the forward registers for the specified channels.

        This method iterates over the provided channels dictionary, retrieves the
        corresponding register name for each channel, and sets a single bit at the
        specified bit position in the register based on the boolean value.

        Args:
            channels (dict[int, bool]): A dictionary where the keys are channel
                                        numbers and the values are
                                        booleans indicating the state.
            bitpos (int): The bit position to update in the register.
        """
        for ch, val in channels.items():
            reg = self._get_fwd_reg_name(ch)
            self._set_addr_single_bit(reg, bitpos, val)

    def _get_fwd_reg_name(self, ch: int) -> int:
        """Generate the forward register name for a given channel.

        Args:
            ch (int): The channel number.

        Returns:
            int: The formatted forward register name as a string.
        """
        regname = "ch_fwd_{}"
        reg = regname.format(ch)
        return reg

    def _set_addr_single_bit(self, reg: str, bitpos: int, bitval: bool):
        """Sets a single bit in a specified analog register.

        Will only send the write command if the bit value is different from the current value.

        Args:
            reg (str): The name of the register to modify.
            bitpos (int): The position of the bit to set.
            bitval (bool): The value to set the bit to (True for 1, False for 0).

        Returns:
            None
        """
        regval = self.board.registers["analog_registers"][reg]["value"]
        if isinstance(regval, list):
            regval = regval[0]
        rval = bit_replace(regval, bitpos, bitval)
        if rval != regval:
            self._write_analog_register(reg, rval)

    def _write_analog_register(self, reg: str, val: int):
        AnalogRegisters(self.board).write(reg, val)


def bit_replace(num: int, pos: int, val: int) -> int:
    """Replaces the bit at a specified position in an integer with a given value.

    Args:
        num (int): The original integer.
        pos (int): The position of the bit to replace (0-indexed from the right).
        val (int): The new value for the bit (0 or 1).

    Returns:
        int: The modified integer with the bit at the specified position replaced by the given value.
    """
    mask = ~(1 << pos)
    num &= mask
    num |= val << pos
    return num
