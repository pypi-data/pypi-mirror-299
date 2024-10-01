import json
import os
from typing import Dict, List, Optional

from httpx import Response

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.schemas import QpuTokenOut
from luna_sdk.schemas.create import QpuTokenIn
from luna_sdk.schemas.enums.qpu_token_type import QpuTokenTypeEnum


class QpuTokenRepo(IQpuTokenRepo):
    @property
    def _endpoint(self) -> str:
        return "/qpu-tokens"

    def _get_endpoint_by_type(
        self, token_type: Optional[QpuTokenTypeEnum] = None
    ) -> str:
        if token_type is None:
            return f"{self._endpoint}"
        elif token_type == QpuTokenTypeEnum.PERSONAL:
            return f"{self._endpoint}/users"
        else:
            return f"{self._endpoint}/organization"

    def _get_by_name(
        self, name: str, token_type: QpuTokenTypeEnum, **kwargs
    ) -> QpuTokenOut:
        response: Response = self._client.get(
            f"{self._get_endpoint_by_type(token_type)}/by_name/{name}", **kwargs
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def create(
        self,
        name: str,
        provider: str,
        token: str,
        token_type: QpuTokenTypeEnum,
        encryption_key: Optional[str] = None,
        **kwargs,
    ) -> QpuTokenOut:
        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        qpu_token = QpuTokenIn(
            name=name,
            provider=provider,
            token=token,
            encryption_key=encryption_key,
        )

        response: Response = self._client.post(
            self._get_endpoint_by_type(token_type),
            content=qpu_token.model_dump_json(),
            **kwargs,
        )
        response.raise_for_status()
        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def get_all(
        self,
        filter_provider: Optional[str] = None,
        name: Optional[str] = None,
        token_type: Optional[QpuTokenTypeEnum] = None,
        **kwargs,
    ) -> Dict[QpuTokenTypeEnum, List[QpuTokenOut]]:
        params = {}
        if filter_provider:
            params["filter_provider"] = filter_provider

        if name:
            params["name"] = name

        response = self._client.get(
            self._get_endpoint_by_type(), params=params, **kwargs
        )
        response.raise_for_status()

        to_return: Dict[QpuTokenTypeEnum, List[QpuTokenOut]] = {}
        for key, value in response.json().items():
            tokens = []
            for item in value:
                if token_type is None or token_type.value == key:
                    item["token_type"] = QpuTokenTypeEnum(key)
                    tokens.append(QpuTokenOut.model_validate(item))
            to_return[QpuTokenTypeEnum(key)] = tokens

        return to_return

    def get(
        self,
        name: str,
        token_type: QpuTokenTypeEnum = QpuTokenTypeEnum.PERSONAL,
        **kwargs,
    ) -> QpuTokenOut:
        qpu_token: QpuTokenOut = self._get_by_name(name, token_type, **kwargs)

        return qpu_token

    def rename(
        self, name: str, new_name: str, token_type: QpuTokenTypeEnum, **kwargs
    ) -> QpuTokenOut:
        qpu_token_update_data = {"name": new_name}

        token: QpuTokenOut = self.get(name, token_type)

        response = self._client.put(
            f"{self._get_endpoint_by_type(token_type)}/{token.id}",
            content=json.dumps(qpu_token_update_data),
            **kwargs,
        )
        response.raise_for_status()

        qpu_token_data = response.json()
        qpu_token_data["token_type"] = token_type
        return QpuTokenOut.model_validate(qpu_token_data)

    def delete(self, name: str, token_type: QpuTokenTypeEnum, **kwargs) -> None:
        token: QpuTokenOut = self.get(name, token_type)

        response = self._client.delete(
            f"{self._get_endpoint_by_type(token_type)}/{token.id}", **kwargs
        )
        response.raise_for_status()
