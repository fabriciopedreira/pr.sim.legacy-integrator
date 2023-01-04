import pytest

from app.dependencies import get_session_db
from app.domain.common.exception_base import UniqueException
from app.domain.patner_example.exceptions import NotFoundException, UnauthorizedException
from app.domain.patner_example.schemas import PatnerCreate, PatnerUpdate
from app.domain.patner_example.service import Service

_LAUNCH_DARKLY_CLIENT = "app.internal.launch_darkly.launch_darkly_client.LaunchDarklyClient.get_flag"


@pytest.fixture
def get_db():
    return next(get_session_db())


@pytest.fixture
def service(get_db):
    return Service(session_db=get_db)


@pytest.fixture
def patner_schema():
    return PatnerCreate(name="Test Unit Patner", document="674.194.620-97", active=True)


@pytest.fixture()
@pytest.mark.asyncio
async def create_patner(service, patner_schema):
    try:
        return await service.get_patner_by_document(patner_schema.document)
    except NotFoundException:
        return await service.create_patner(patner_schema)


@pytest.fixture()
@pytest.mark.asyncio
async def remove_patner(service):
    try:
        await service.delete_patner(1)
    except NotFoundException:
        pass


@pytest.fixture
@pytest.mark.usefixtures("create_tables_db")
def init_db(create_tables_db):
    pass


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
async def test_get_patner_by_id_raise_not_found_exception(init_db, service, cap_logger):
    patner_id = 1

    with pytest.raises(NotFoundException), cap_logger.at_level(20):
        await service.get_patner_by_id(patner_id)

        assert "[-] patner_example not found - Status=[404]" in cap_logger.records[0].message
        assert "INFO" == cap_logger.records[0].levelname


@pytest.mark.asyncio
async def test_get_patner_by_id_return_parner(init_db, service, create_patner):
    new_patner = await create_patner
    patner = await service.get_patner_by_id(new_patner.id)

    assert patner.name == new_patner.name
    assert patner.document == new_patner.document
    assert patner.active == new_patner.active


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
async def test_get_patner_by_document_raise_not_found_exception(init_db, service, cap_logger):
    document = "674.194.620-97"

    with pytest.raises(NotFoundException), cap_logger.at_level(20):
        await service.get_patner_by_document(document)

        assert "[-] patner_example not found - Status=[404]" in cap_logger.records[0].message
        assert "INFO" == cap_logger.records[0].levelname


@pytest.mark.asyncio
async def test_get_patner_by_document_return_parner(init_db, service, create_patner):
    new_patner = await create_patner
    patner = await service.get_patner_by_document(new_patner.document)

    assert patner.name == new_patner.name
    assert patner.document == new_patner.document
    assert patner.active == new_patner.active


@pytest.mark.asyncio
async def test_get_all_patner_return_parners(init_db, service, create_patner):
    new_patner = await create_patner
    patners = await service.get_all_patner()

    assert len(patners) > 0
    assert patners[0].name == new_patner.name
    assert patners[0].document == new_patner.document
    assert patners[0].active == new_patner.active


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
async def test_create_patner_raise_unique_exception(init_db, service, create_patner, patner_schema, cap_logger):
    await create_patner

    with pytest.raises(UniqueException), cap_logger.at_level(30):
        await service.create_patner(patner_schema)

        assert "[-] Unique constraint - the value already exists in the database" in cap_logger.records[0].message
        assert "WARNING" == cap_logger.records[0].levelname


@pytest.mark.asyncio
async def test_create_patner_return_patner(init_db, service):
    patner_name = "Patner Test Unit"
    patner_document = "916.638.390-00"
    patner = await service.create_patner(PatnerCreate(name=patner_name, document=patner_document, active=True))

    assert patner.name == patner_name
    assert patner.document == "91663839000"
    assert patner.active is True


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
async def test_update_patner_raise_unauthorized_exception_when_flag_is_off(
    init_db, service, patner_schema, mocker, cap_logger
):
    patner = PatnerUpdate(id=1, name=patner_schema.name, document=patner_schema.document, active=patner_schema.active)

    with pytest.raises(UnauthorizedException), cap_logger.at_level(20):
        mocker.patch(_LAUNCH_DARKLY_CLIENT, return_value=False)
        await service.update_patner(patner)

        assert "[-] Unauthorized user for feature-flag - Status=[401]" in cap_logger.records[0].message
        assert "INFO" == cap_logger.records[0].levelname


@pytest.mark.asyncio
@pytest.mark.usefixtures("cap_logger")
async def test_update_patner_return_patner_when_flag_is_on(init_db, service, patner_schema, create_patner, mocker):
    await create_patner
    patner_name = "Update Patner Name"
    patner_object = PatnerUpdate(id=1, name=patner_name, document=patner_schema.document, active=False)

    mocker.patch(_LAUNCH_DARKLY_CLIENT, return_value=True)
    patner = await service.update_patner(patner_object)

    assert patner is not None
    assert patner.name == patner_name
    assert patner.active is False
