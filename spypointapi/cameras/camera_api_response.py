from datetime import datetime
from typing import Dict, Any, List

from .. import Camera
from .camera import Coordinates, TransmitTime


class CameraApiResponse:

    @classmethod
    def from_json(cls, data: List[Dict[str, Any]]) -> List[Camera]:
        return [CameraApiResponse.camera_from_json(d) for d in data]

    @classmethod
    def camera_from_json(cls, data: Dict[str, Any]) -> Camera:
        config = data.get('config', {})
        status = data.get('status', {})
        return Camera(
            id=data['id'],
            name=config['name'],
            model=status['model'],
            modem_firmware=status.get('modemFirmware', ''),
            camera_firmware=status.get('version', ''),
            last_update_time=datetime.fromisoformat(status['lastUpdate'][:-1]).replace(tzinfo=datetime.now().astimezone().tzinfo),
            signal=status.get('signal', {}).get('processed', {}).get('percentage', None),
            temperature=CameraApiResponse.temperature_from_json(status.get('temperature', None)),
            battery=CameraApiResponse.battery_from_json(status.get('batteries', None)),
            battery_type=status.get('batteryType', None),
            memory=CameraApiResponse.memory_from_json(status.get('memory', None)),
            notifications=CameraApiResponse.notifications_from_json(status.get('notifications', None)),
            owner=CameraApiResponse.owner_from_json(data),
            coordinates=CameraApiResponse.coordinates_from_json(status.get('coordinates', None)),
            activation_date=CameraApiResponse.datetime_from_json(data.get('activationDate')),
            creation_date=CameraApiResponse.datetime_from_json(data.get('creationDate')),
            is_cellular=data.get('isCellular', data.get('cellular', None)),
            capture_mode=config.get('captureMode', None),
            delay=config.get('delay', None),
            multi_shot=config.get('multiShot', None),
            quality=config.get('quality', None),
            operation_mode=config.get('operationMode', None),
            sensibility=config.get('sensibility', {}).get('level', None),
            transmit_auto=config.get('transmitAuto', None),
            transmit_format=config.get('transmitFormat', None),
            transmit_freq=config.get('transmitFreq', None),
            transmit_time=CameraApiResponse.transmit_time_from_json(config.get('transmitTime', None)),
            trigger_speed=config.get('triggerSpeed', None),
        )

    @classmethod
    def temperature_from_json(cls, temperature: Dict[str, Any] | None) -> int | None:
        if not temperature or None in (temperature.get('unit'), temperature.get('value')):
            return None

        unit = temperature['unit']
        value = temperature['value']
        return value if unit == 'C' else int((value - 32) * 5 / 9)

    @classmethod
    def battery_from_json(cls, batteries: Dict[str, Any] | None) -> str | None:
        if not batteries:
            return None
        return max(batteries)

    @classmethod
    def memory_from_json(cls, memory: Dict[str, Any] | None) -> float | None:
        if not memory:
            return None
        if memory.get('size', 0) == 0:
            return None
        return round(memory.get('used') / memory.get('size') * 100, 2)

    @classmethod
    def transmit_time_from_json(cls, transmit_time: Dict[str, Any] | None) -> TransmitTime | None:
        if not transmit_time or None in (transmit_time.get('hour'), transmit_time.get('minute')):
            return None
        return TransmitTime(hour=transmit_time['hour'], minute=transmit_time['minute'])

    @classmethod
    def notifications_from_json(cls, notifications: Dict[str, Any] | None) -> List[str] | None:
        if notifications is None:
            return None
        return [str(notification) for notification in notifications]

    @classmethod
    def owner_from_json(cls, data):
        owner = data.get('ownerFirstName', None)
        if owner is None:
            return None
        return owner.strip()

    @classmethod
    def coordinates_from_json(cls, coordinates: List[Any] | None) -> Coordinates | None:
        if (coordinates is None
                or len(coordinates) < 1
                or coordinates[0].get('position', {}).get('type', '') != 'Point'
                or len(coordinates[0].get('position', {}).get('coordinates', [])) != 2):
            return None
        lat_lon = coordinates[0]['position']['coordinates']
        return Coordinates(latitude=lat_lon[1], longitude=lat_lon[0])

    @classmethod
    def datetime_from_json(cls, date_str: str | None) -> datetime | None:
        if not date_str:
            return None
        current_timezone = datetime.now().astimezone().tzinfo
        return datetime.fromisoformat(date_str.rstrip('Z')).replace(tzinfo=current_timezone)
