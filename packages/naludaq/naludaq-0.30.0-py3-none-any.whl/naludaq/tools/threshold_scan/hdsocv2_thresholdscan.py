import logging


from naludaq.controllers import get_readout_controller, get_trigger_controller
from naludaq.tools.threshold_scan.hdsoc_thresholdscan import ThresholdScanHdsoc

LOGGER = logging.getLogger("naludaq.threshold_scan")


class ThresholdScanHdsocv2(ThresholdScanHdsoc):
    """Tool for sweeping over trigger thresholds and counting number of triggers.
    Can be used to determine the ideal point to set the trigger.

    """

    def __init__(
        self,
        board,
        *args,
        low_ref_value: int = None,
        high_ref_value: int = None,
        **kwargs,
    ):
        """Threshold scan for hdsoc boards.

        Args:
            board (Board): board object
            start_value (int): the start value for the scan
            stop_value (int): the stop value for the scan
            step_size (int): the step size for the scan
            low_ref_value (int): low reference value
            high_ref_value (int): high reference value
        """
        super().__init__(board, *args, **kwargs)

    def _backup_board_settings(self):
        """Back up the trigger values, readout channels, references, and tsel"""
        self._original_trigger_values = self.board.trigger_values.copy()
        rc = get_readout_controller(self.board)
        tc = get_trigger_controller(self.board)
        self._original_readout_channels = rc.get_readout_channels()
        self._original_left_references = tc.left_references
        self._original_right_references = tc.right_references

    def _restore_board_settings(self):
        """Restore the trigger values, readout channels, references, and tsel"""
        self.trigger_values = self._original_trigger_values
        self._trigger_controller.write_triggers()
        rc = get_readout_controller(self.board)
        tc = get_trigger_controller(self.board)
        rc.set_readout_channels(self._original_readout_channels)
        tc.update_reference_voltages("left", *self._original_left_references)
        tc.update_reference_voltages("right", *self._original_right_references)

    def _set_tsel_enabled(self, left: bool, right: bool):
        """Set whether tsel is enabled on each side.

        During the threshold scan, tsel must be enabled for scalars
        to read correctly.
        """
        pass
