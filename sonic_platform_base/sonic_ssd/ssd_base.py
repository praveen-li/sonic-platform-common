#
# ssd_base.py
#
# Base class for implementing common SSD health features
#


class SsdBase(object):
    """
    Base class for interfacing with a SSD
    """
    def __init__(self, diskdev):
        """
        Constructor

        Args:
            diskdev: Linux device name to get parameters for
        """
        pass

    def get_health(self):
        """
        Retrieves current disk health in percentages

        Returns:
            A float number of current ssd health
            e.g. 83.5
        """
        raise NotImplementedError

    def get_temperature(self):
        """
        Retrieves current disk temperature in Celsius

        Returns:
            A float number of current temperature in Celsius
            e.g. 40.1
        """
        raise NotImplementedError

    def get_model(self):
        """
        Retrieves model for the given disk device

        Returns:
            A string holding disk model as provided by the manufacturer
        """
        raise NotImplementedError

    def get_firmware(self):
        """
        Retrieves firmware version for the given disk device

        Returns:
            A string holding disk firmware version as provided by the manufacturer
        """
        raise NotImplementedError

    def get_serial(self):
        """
        Retrieves serial number for the given disk device

        Returns:
            A string holding disk serial number as provided by the manufacturer
        """
        raise NotImplementedError

    def get_vendor_output(self):
        """
        Retrieves vendor specific data for the given disk device

        Returns:
            A string holding some vendor specific disk information
        """
        raise NotImplementedError

    def get_power_on_hours(self):
        """
        Retrieves power on hours for the given disk device

        Returns:
            An integer of power on hour
        """
        raise NotImplementedError

    def get_power_cycle_count(self):
        """
        Retrieves power cycle count for the given disk device

        Returns:
            An integer of power cycle count
        """
        raise NotImplementedError

    def get_total_bad_block_count(self):
        """
        Retrieves total bad block count for the given disk device

        Returns:
            An integer of total bad block count
        """
        raise NotImplementedError

    def get_erase_count_max(self):
        """
        Retrieves erase count max for the given disk device

        Returns:
            An integer of erase count max
        """
        raise NotImplementedError

    def get_erase_count_avg(self):
        """
        Retrieves erase count avg for the given disk device

        Returns:
            An integer of erase count avg
        """
        raise NotImplementedError
