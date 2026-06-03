from uuid import uuid4

from app.application.interfaces.external_services import (
    IRefundPaymentService
)


class RefundPaymentService(IRefundPaymentService):
    def refund_payment(
        self,
        account_number: str,
        amount: float
    ) -> str:
        return f"REFUND-{uuid4()}"