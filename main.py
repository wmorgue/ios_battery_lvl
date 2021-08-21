import subprocess
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    title: str = None
    message: str = None

    cut: str = "cut -d: -f2"
    device_info: str = "ideviceinfo"
    domain: str = "com.apple.mobile.battery"
    current_capacity: str = "BatteryCurrentCapacity"

    def device_name(self) -> str:
        """Get device name, e.g. iPhone name.
        rtype: `str`.
        """
        name = subprocess.run("idevicename", capture_output=True)
        return name.stdout.decode("utf-8")

    def get_battery_lvl(self) -> int:
        """Check battery level.
        rtype: `int`.
        """
        result = subprocess.run(
            f"{self.device_info} -q {self.domain} -n | rg {self.current_capacity} | {self.cut}",
            shell=True,
            capture_output=True,
        )
        return int(result.stdout.decode("utf-8"))

    def macos_notification(self) -> None:
        """Create and display notification on macOS with current battery level.
        rtype: `None`.
        """
        command = f"""
        osascript -e 'display notification "{self.message}" with title "{self.title}"'
        """
        subprocess.call(command, shell=True)


name = DeviceInfo().device_name()
check_lvl = DeviceInfo().get_battery_lvl()

device = DeviceInfo(f"iPhone {name}", f"Battery: {check_lvl} 🔋")
device.macos_notification()
