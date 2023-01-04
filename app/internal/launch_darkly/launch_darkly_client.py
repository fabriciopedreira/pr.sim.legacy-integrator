from dataclasses import dataclass, field
from typing import Any, Dict

import ldclient
from loguru import logger

from app.domain.common.exception_base import LaunchDarklyException
from app.internal.config.settings import LAUNCH_DARKLY_SECRET_KEY

ERROR = "ERROR"


@dataclass
class LaunchDarklyClient:
    client: ldclient.LDClient = field(init=False)

    def __post_init__(self):
        config = ldclient.Config(LAUNCH_DARKLY_SECRET_KEY)
        ldclient.set_config(config)

        self.client = ldclient.get()

    def get_flag(self, flag: str, user: Dict[str, Any], default: bool = False) -> str:
        """Get feature flag for a user
        :param: flag: the unique key for the feature flag
        :param: user: a dictionary containing parameters for the end user requesting the flag
        :param: default: the default value of the flag, to be used if the value is not
          available from LaunchDarkly

        :return: string
        """
        detail = self.client.variation_detail(flag, user, default)

        if detail.reason.get("kind") != ERROR:
            logger.info("[+] feature-flag successfully obtained")
            return self.client.variation(flag, user, default)

        raise LaunchDarklyException(reason=detail.reason)

    def __del__(self):
        self.client.close()
