from abc import ABC, abstractmethod

class IPaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, booking_id: str, amount: float) -> bool:
        pass

class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient: str, message: str) -> None:
        pass

class IRefundPaymentService(ABC):
    @abstractmethod
    def refund_payment(self, account_number: str, amount: float) -> str:
        pass