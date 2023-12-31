import sys
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable

import jwt
from async_lru import alru_cache
from loguru import logger

from app.domain.legacy_query.enums import TipoPessoa


def exc_info():
    """Get current exception information
    :return: Return current exception information: (type, value).
    """
    type_, value, _ = sys.exc_info()
    return type_, value


def latency(func: Callable):
    """Decorator to calculate endpoint latency. Print latency and response logs.
    :param: func: A callaable function

    :return: A callaable function
    """

    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)

        if result:
            message = f"[+] {result}"
            logger.log("RESPONSE", message)

        logger.log("LATENCY", f"[+] {round(time.time() - start_time, 10)} s")
        return result

    return wrapped_func


def cache(seconds: int, maxsize: int = 128):
    """Decorator to applay cache with expiration time, allows to return the response of the function
    if it was previously called. It can save time when an expensive or I/O bound function is periodically called
    with the same arguments.

    :param: seconds: expiration time in seconds
    :param: maxsize: maximum size to cache.

    :return: function response
    """

    def wrapper_cache(func):
        func = alru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return await func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def parser_person_type(person_type: str) -> int | None:
    return {TipoPessoa.PESSOA_FISICA: 1, TipoPessoa.PESSOA_JURIDICA: 2, TipoPessoa.PRODUTOR_RURAL: 3}.get(
        person_type.upper(), None
    )


def parse_ipca(cet, ipca):
    if cet.upper() == "PRE_FIXADO":
        return
    if cet.upper() == "POS_FIXADO":
        return ipca


def has_valid_cpf(cpf: str) -> bool:
    cpf_parsed = cpf.replace(".", "").replace("-", "")

    return len(cpf_parsed) == 11


def sanitize_document(document: str) -> str | int:
    document_parsed = document.replace(".", "").replace("-", "").replace("/", "")

    if not document_parsed.isdigit():
        document_parsed = ""

    return document_parsed


def format_document(size_document: int, document: str) -> str:
    if size_document == 11:  # CPF
        applied_mask = f"{document[:3]}.{document[3:6]}.{document[6:9]}-{document[9:]}"
    else:  # CNPJ
        applied_mask = f"{document[:2]}.{document[2:5]}.{document[5:8]}/{document[8:12]}-{document[12:]}"

    return applied_mask


def get_sub(token: str) -> int:
    """Get user sub from jwt token
    :param: token: jwt token
    """
    try:
        payload: dict[str, Any] = jwt.decode(token, options={"verify_signature": False})  # type: ignore
        return int(payload.get("sub", 0))
    except Exception:
        return 0


def get_month_by_number(mount_number: int) -> str:
    """Get month by number
    :param: mount_number: number of month
    """
    return {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }.get(mount_number, "Mês inválido")
