import subprocess


def device_name() -> str:
    name = subprocess.run("idevicename", capture_output=True)
    return name.stdout.decode("utf-8")


def get_battery_lvl() -> int:
    cut: str = "cut -d: -f2"
    domain: str = "com.apple.mobile.battery"
    current_capacity: str = "BatteryCurrentCapacity"

    result = subprocess.run(
        f"ideviceinfo -q {domain} -n | rg {current_capacity} | {cut}",
        shell=True,
        capture_output=True,
    )
    return int(result.stdout.decode("utf-8"))


def notification(title: str = None, msg: str = None) -> None:
    command = f"""
    osascript -e 'display notification "{msg}" with title "{title}"'
    """
    subprocess.call(command, shell=True)


lvl: int = get_battery_lvl()
name: str = device_name()
title: str = f"iPhone {name}"
msg: str = f"Battery is {lvl}%"

notification(title, msg)
