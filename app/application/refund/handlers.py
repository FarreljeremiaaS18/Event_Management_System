from app.domain.refund.aggregate import Refund
from app.application.interfaces.external_services import IRefundPaymentService
from app.domain.refund.repository import IRefundRepository
from app.application.refund.commands import MarkRefundPaidOutCommand


class MarkRefundPaidOutCommandHandler:
    def __init__(self, repository: IRefundRepository, payout_service: IRefundPaymentService):
        self.repository = repository
        self.payout_service = payout_service

    def execute(self, command: MarkRefundPaidOutCommand):
        refund = self.repository.find_by_id(command.refund_id)
        
        ref_number = self.payout_service.process_payout(
            account_number="dummy_account", 
            amount=150000.0 
        )
        
        refund.mark_as_paid_out(payment_reference=command.payment_reference or ref_number)
        self.repository.save(refund)