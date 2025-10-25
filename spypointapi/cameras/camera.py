from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TypeAlias, List

Percentage: TypeAlias = float
Celsius: TypeAlias = int
Degrees: TypeAlias = float


@dataclass()
class Coordinates:
    latitude: Degrees
    longitude: Degrees


@dataclass()
class TransmitTime:
    hour: int
    minute: int


@dataclass()
class Camera:
    id: str
    name: str
    model: str
    modem_firmware: str
    camera_firmware: str
    last_update_time: datetime
    signal: Percentage | None = None
    temperature: Celsius | None = None
    battery: Percentage | None = None
    battery_type: str | None = None
    memory: Percentage | None = None
    notifications: List[str] | None = None
    owner: str | None = None
    coordinates: Coordinates | None = None
    activation_date: datetime | None = None
    creation_date: datetime | None = None
    is_cellular: bool | None = None
    capture_mode: str | None = None
    delay: int | None = None
    multi_shot: int | None = None
    quality: str | None = None
    operation_mode: str | None = None
    sensibility: str | None = None
    transmit_auto: bool | None = None
    transmit_format: str | None = None
    transmit_freq: int | None = None
    transmit_time: TransmitTime | None = None
    trigger_speed: str | None = None
    photo_count: int | None = None
    photo_limit: int | None = None
    hd_photo_count: int | None = None
    hd_photo_limit: int | None = None

    @property
    def is_online(self) -> bool:
        now = datetime.now().astimezone()
        diff = now - self.last_update_time
        return diff <= timedelta(hours=24)

    def __str__(self) -> str:
        return (
            f"Camera(id={self.id}, name={self.name}, model={self.model}, "
            f"modem_firmware={self.modem_firmware}, camera_firmware={self.camera_firmware}, "
            f"last_update_time={self.last_update_time}, signal={self.signal}, "
            f"temperature={self.temperature}, battery={self.battery}, battery_type={self.battery_type}, "
            f"memory={self.memory}, notifications={self.notifications}, "
            f"online={self.is_online}), owner={self.owner}, coordinates={self.coordinates}, "
            f"activation_date={self.activation_date}, creation_date={self.creation_date}, "
            f"is_cellular={self.is_cellular}, capture_mode={self.capture_mode}, "
            f"delay={self.delay}, multi_shot={self.multi_shot}, quality={self.quality}, "
            f"operation_mode={self.operation_mode}, sensibility={self.sensibility}, "
            f"transmit_auto={self.transmit_auto}, transmit_format={self.transmit_format}, "
            f"transmit_freq={self.transmit_freq}, transmit_time={self.transmit_time}, "
            f"trigger_speed={self.trigger_speed}), "
            f"photo_count={self.photo_count}, photo_limit={self.photo_limit}, "
            f"hd_photo_count={self.hd_photo_count}, hd_photo_limit={self.hd_photo_limit})"
        )
