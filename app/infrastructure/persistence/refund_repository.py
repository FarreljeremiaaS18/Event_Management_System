from uuid import UUID

from app.domain.refund.aggregate import Refund
from app.domain.refund.repository import IRefundRepository
from app.infrastructure.persistence.db import SessionLocal
from app.infrastructure.persistence.models import RefundModel
from app.infrastructure.persistence.mappers import RefundMapper


class RefundRepository(IRefundRepository):
    def find_by_id(self, id: UUID) -> Refund | None:
        with SessionLocal() as session:
            model = session.query(RefundModel).filter(RefundModel.id == str(id)).first()
            if model:
                return RefundMapper.to_domain(model)
            return None

    def find_by_booking(self, booking_id: UUID) -> Refund | None:
        with SessionLocal() as session:
            model = session.query(RefundModel).filter(RefundModel.booking_id == str(booking_id)).first()
            if model:
                return RefundMapper.to_domain(model)
            return None

    def save(self, refund: Refund) -> None:
        with SessionLocal() as session:
            model = RefundMapper.to_model(refund)
            session.merge(model)
            session.commit()    
            

   