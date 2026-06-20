from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.presentation.request.refund_requests import MarkPaidOutRequest
from app.application.refund.commands import MarkRefundPaidOutCommand
from app.application.refund.handlers import MarkRefundPaidOutCommandHandler
from app.presentation.dependencies import get_mark_refund_paid_out_handler

router = APIRouter(prefix="/refunds", tags=["Refunds"])

@router.post("/{refund_id}/pay")
def mark_refund_paid_out(
    refund_id: UUID,
    request: MarkPaidOutRequest,
    handler: MarkRefundPaidOutCommandHandler = Depends(get_mark_refund_paid_out_handler)
):
    try:
        command = MarkRefundPaidOutCommand(
            refund_id=refund_id,
            payment_reference=request.payment_reference
        )
        handler.execute(command)
        return {"message": "Refund paid out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))