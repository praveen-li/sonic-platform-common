#
# ssd_generic.py
#
# Generic implementation of the SSD health API
# SSD models supported:
#  - InnoDisk
#  - StorFly
#  - Virtium

try:
    import re
    import subprocess
    from .ssd_base import SsdBase
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

SMARTCTL = "smartctl {} -a"
INNODISK = "iSmart -d {}"
VIRTIUM  = "SmartCmd -m {}"

NOT_AVAILABLE = "N/A"


class SsdUtil(SsdBase):
    """
    Generic implementation of the SSD health API
    """
    model = NOT_AVAILABLE
    serial = NOT_AVAILABLE
    firmware = NOT_AVAILABLE
    temperature = NOT_AVAILABLE
    health = NOT_AVAILABLE
    power_on_hours = NOT_AVAILABLE
    power_cycle_count = NOT_AVAILABLE
    total_bad_block_count = NOT_AVAILABLE
    erase_count_max = NOT_AVAILABLE
    erase_count_avg = NOT_AVAILABLE

    ssd_info = NOT_AVAILABLE
    vendor_ssd_info = NOT_AVAILABLE

    def __init__(self, diskdev):
        self.vendor_ssd_utility = {
            "Generic"  : { "utility" : SMARTCTL, "parser" : self.parse_generic_ssd_info },
            "InnoDisk" : { "utility" : INNODISK, "parser" : self.parse_innodisk_info },
            "M.2"      : { "utility" : INNODISK, "parser" : self.parse_innodisk_info },
            "StorFly"  : { "utility" : VIRTIUM,  "parser" : self.parse_virtium_info },
            "Virtium"  : { "utility" : VIRTIUM,  "parser" : self.parse_virtium_info }
        }

        self.dev = diskdev
        # Generic part
        self.fetch_generic_ssd_info(diskdev)
        self.parse_generic_ssd_info()

        # Known vendor part
        if self.model:
            model_short = self.model.split()[0]
            if model_short in self.vendor_ssd_utility:
                self.fetch_vendor_ssd_info(diskdev, model_short)
                self.parse_vendor_ssd_info(model_short)
            else:
                # No handler registered for this disk model
                pass
        else:
            # Failed to get disk model
            self.model = "Unknown"

    def _execute_shell(self, cmd):
        process = subprocess.Popen(cmd.split(), universal_newlines=True, stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output

    def _parse_re(self, pattern, buffer):
        res_list = re.findall(pattern, buffer)
        return res_list[0] if res_list else NOT_AVAILABLE

    def fetch_generic_ssd_info(self, diskdev):
        self.ssd_info = self._execute_shell(self.vendor_ssd_utility["Generic"]["utility"].format(diskdev))

    def parse_generic_ssd_info(self):
        self.model = self._parse_re('Device Model:\s*(.+?)\n', self.ssd_info)
        self.serial = self._parse_re('Serial Number:\s*(.+?)\n', self.ssd_info)
        self.firmware = self._parse_re('Firmware Version:\s*(.+?)\n', self.ssd_info)

    def parse_innodisk_info(self):
        self.health = self._parse_re('Health:\s*(.+?)%', self.vendor_ssd_info)
        self.temperature = self._parse_re('Temperature\s*\[\s*(.+?)\]', self.vendor_ssd_info)
        self.power_on_hours = self._parse_re('Power On Hours\s*\[\s*(.+?)\]', self.vendor_ssd_info)
        self.power_cycle_count = self._parse_re('Power Cycle Count\s*\[\s*(.+?)\]', self.vendor_ssd_info)
        self.total_bad_block_count = self._parse_re('Total Bad Block Count\s*\[\s*(.+?)\]', self.vendor_ssd_info)
        self.erase_count_max = self._parse_re('Erase Count Max.\s*\[\s*(.+?)\]', self.vendor_ssd_info)
        self.erase_count_avg = self._parse_re('Erase Count Avg.\s*\[\s*(.+?)\]', self.vendor_ssd_info)

    def parse_virtium_info(self):
        self.temperature = self._parse_re('Temperature_Celsius\s*\d*\s*(\d+?)\s+', self.vendor_ssd_info)
        nand_endurance = self._parse_re('NAND_Endurance\s*\d*\s*(\d+?)\s+', self.vendor_ssd_info)
        avg_erase_count = self._parse_re('Average_Erase_Count\s*\d*\s*(\d+?)\s+', self.vendor_ssd_info)
        try:
            self.health = 100 - (float(avg_erase_count) * 100 / float(nand_endurance))
        except ValueError:
            pass

    def fetch_vendor_ssd_info(self, diskdev, model):
        self.vendor_ssd_info = self._execute_shell(self.vendor_ssd_utility[model]["utility"].format(diskdev))

    def parse_vendor_ssd_info(self, model):
        self.vendor_ssd_utility[model]["parser"]()

    def get_health(self):
        """
        Retrieves current disk health in percentages

        Returns:
            A float number of current ssd health
            e.g. 83.5
        """
        return self.health

    def get_temperature(self):
        """
        Retrieves current disk temperature in Celsius

        Returns:
            A float number of current temperature in Celsius
            e.g. 40.1
        """
        return self.temperature

    def get_model(self):
        """
        Retrieves model for the given disk device

        Returns:
            A string holding disk model as provided by the manufacturer
        """
        return self.model

    def get_firmware(self):
        """
        Retrieves firmware version for the given disk device

        Returns:
            A string holding disk firmware version as provided by the manufacturer
        """
        return self.firmware

    def get_serial(self):
        """
        Retrieves serial number for the given disk device

        Returns:
            A string holding disk serial number as provided by the manufacturer
        """
        return self.serial

    def get_vendor_output(self):
        """
        Retrieves vendor specific data for the given disk device

        Returns:
            A string holding some vendor specific disk information
        """
        return self.vendor_ssd_info

    def get_power_on_hours(self):
        """
        Retrieves power on hours for the given disk device

        Returns:
            An integer of power on hour
        """
        return self.power_on_hours

    def get_power_cycle_count(self):
        """
        Retrieves power cycle count for the given disk device

        Returns:
            An integer of power cycle count
        """
        return self.power_cycle_count

    def get_total_bad_block_count(self):
        """
        Retrieves total bad block count for the given disk device

        Returns:
            An integer of total bad block count
        """
        return self.total_bad_block_count

    def get_erase_count_max(self):
        """
        Retrieves erase count max for the given disk device

        Returns:
            An integer of erase count max
        """
        return self.erase_count_max

    def get_erase_count_avg(self):
        """
        Retrieves erase count avg for the given disk device

        Returns:
            An integer of erase count avg
        """
        return self.erase_count_avg
