from app.application.interfaces.external_services import (
    INotificationService
)


class NotificationService(INotificationService):
    def send_notification(
        self,
        recipient: str,
        message: str
    ) -> None:
        print(f"[NOTIFICATION] {recipient}: {message}")