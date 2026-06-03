from app.application.interfaces.external_services import IPaymentGateway


class PaymentGateway(IPaymentGateway):
    def process_payment(
        self,
        booking_id: str,
        amount: float
    ) -> bool:
        return True