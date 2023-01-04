from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import access_validation, get_session_db
from app.domain.common.legacy_model import Emprestimo, Contrato, Financiamento, Bancarizadora, Cliente, \
    ProdutoFinanceiro
from app.domain.legacy_query.schemas import FormalizedFinancingResponse
from app.internal.utils import latency

router = APIRouter(dependencies=[Depends(access_validation)])


@router.get("/financing/{product_slug}", summary="Consult data on formalized financing.", response_model=FormalizedFinancingResponse, status_code=200)
@latency
async def read_patner_by_document(product_slug: str, session_db: Session = Depends(get_session_db)):
    """Get patner by document
    * **param**: product_slug: Slug from financing-product
    * **param**: session_db: Session of sql database

    **return**: BaseModel
    """

    fields = ('numero_ccb', 'nome', 'cpf', 'nome_completo', 'slug')

    session_db.query(
        Financiamento, *fields
    ).join(
        Contrato
    ).join(
        Emprestimo
    ).join(
        Bancarizadora
    ).join(
        Cliente
    ).join(
        ProdutoFinanceiro
    ).filter(
        ProdutoFinanceiro.slug == product_slug
    ).all()

    return FormalizedFinancingResponse()
