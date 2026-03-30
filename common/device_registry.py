from __future__ import annotations

from common.models import DeviceInfo


MOCK_DEVICES: tuple[DeviceInfo, ...] = (
    DeviceInfo(
        device_id="android-pixel7-01",
        platform="android",
        os_version="14",
        model="Pixel 7",
        role="main",
        tags=("wifi", "playback", "baseline"),
    ),
    DeviceInfo(
        device_id="ios-iphone14-01",
        platform="ios",
        os_version="17.4",
        model="iPhone 14",
        role="main",
        tags=("wifi", "playback", "regression"),
    ),
    DeviceInfo(
        device_id="android-galaxy-s22-aux",
        platform="android",
        os_version="13",
        model="Galaxy S22",
        role="auxiliary",
        tags=("capture", "auxiliary"),
    ),
)


def list_devices(platform: str | None = None, role: str | None = None) -> list[dict]:
    result = []
    for device in MOCK_DEVICES:
        if platform and device.platform != platform:
            continue
        if role and device.role != role:
            continue
        result.append(device.to_dict())
    return result


def select_devices(preferred_platforms: tuple[str, ...]) -> list[dict]:
    primary: list[dict] = []
    auxiliary: list[dict] = []
    for platform in preferred_platforms:
        for device in MOCK_DEVICES:
            if device.platform != platform:
                continue
            if device.role == "main" and not primary:
                primary.append(device.to_dict())
            elif device.role == "auxiliary" and not auxiliary:
                auxiliary.append(device.to_dict())
    if not primary:
        primary.append(MOCK_DEVICES[0].to_dict())
    return primary + auxiliary
