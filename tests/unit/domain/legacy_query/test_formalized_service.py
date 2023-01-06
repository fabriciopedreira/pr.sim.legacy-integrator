import pytest

from app.domain.common.exception_base import NotFoundException
from app.domain.legacy_query.repository.formalized import FormalizedRepository
from app.domain.legacy_query.service.formalized import FormalizedService


@pytest.fixture
@pytest.mark.usefixtures("session_db")
def formalized_repository(session_db):
    return FormalizedRepository(session=session_db)


@pytest.fixture
def formalized_service(formalized_repository):
    return FormalizedService(repository=formalized_repository)


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
@pytest.mark.usefixtures("create_tables_db")
async def test_find_formalizations_by_cessao_date_and_product_slug__raise_not_found_exception(
    formalized_service, cap_logger, create_tables_db
):
    with pytest.raises(NotFoundException), cap_logger.at_level(20):
        await formalized_service.formalizations_by_cessao_date_and_product_slug(
            cessao_date="2023-01-06", product_slug="fidc_v"
        )

        assert "[-] Values not found - Status=[204]" in cap_logger.records[0].message
        assert "INFO" == cap_logger.records[0].levelname
