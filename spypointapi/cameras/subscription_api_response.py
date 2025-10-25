from dataclasses import dataclass
from typing import Any


@dataclass()
class SubscriptionApiResponse:
    photoCount: int | None
    photoLimit: int | None
    hdPhotoCount: int | None
    hdPhotoLimit: int | None

    @classmethod
    def subscription_from_json(cls, subscriptions: list[dict[str, Any]] | None):
        subscription = subscriptions[0] if subscriptions else {}
        return SubscriptionApiResponse(
            subscription.get('photoCount'),
            subscription.get('photoLimit'),
            subscription.get('hdPhotoCount'),
            subscription.get('hdPhotoLimit')
        )