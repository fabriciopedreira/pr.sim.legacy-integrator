import sentry_sdk
from ddtrace import config, patch
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.internal.config.settings import PROJECT_NAME_API, PROJECT_VERSION_API, SENTRY_SDK_DSN


def set_up_sentry_sdk() -> None:
    """
    Sentry SDK configuration (https://docs.sentry.io/platforms/python/guides/fastapi/configuration/options/).
    release: Sets the release - sync with your deploy (app version).
    send_default_pii: If this flag is enabled, certain personally identifiable information is added by active
     integrations. By default, no such data is sent.
    attach_stacktrace: stack traces are automatically attached to all messages logged. Stack traces are always
     attached to exceptions

    :return: None
    """
    sentry_sdk.init(
        dsn=SENTRY_SDK_DSN,
        integrations=[
            StarletteIntegration(transaction_style="url"),
            FastApiIntegration(transaction_style="url"),
            SqlalchemyIntegration(),
        ],
        release=PROJECT_VERSION_API,
        send_default_pii=True,
        attach_stacktrace=True,
    )


def set_up_ddtrace() -> None:
    """Add datadog integration

    :return: None
    """
    patch(fastapi=True)

    # Override service name
    config.fastapi["service_name"] = PROJECT_NAME_API + "-fastapi"

    # Override request span name
    config.fastapi["request_span_name"] = PROJECT_NAME_API + "-fastapi.request"
