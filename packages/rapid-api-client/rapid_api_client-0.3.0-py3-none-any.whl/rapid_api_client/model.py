from dataclasses import dataclass, field
from typing import Any, Dict

from httpx import AsyncClient
from pydantic import BaseModel

try:
    import pydantic_xml
except ImportError:  # pragma: nocover
    pydantic_xml = None  # type: ignore


@dataclass
class RapidApi:
    client: AsyncClient = field(default_factory=AsyncClient)


class RequestModifier:
    def update_headers(self, headers: Dict[str, str]) -> Dict[str, str]: ...

    def update_query(self, query_parameters: Dict[str, str]) -> Dict[str, str]: ...

    def update_path(self, path: str) -> str: ...


class CustomParameter: ...


class Path(CustomParameter): ...


@dataclass
class Query(CustomParameter):
    alias: str | None = None


@dataclass
class Header(CustomParameter):
    alias: str | None = None


class Body(CustomParameter):
    def serialize(self, body: Any) -> str | bytes:
        return body


@dataclass
class FileBody(Body):
    alias: str | None = None

    def serialize(self, body: Any) -> str | bytes:
        return body


@dataclass
class PydanticBody(Body):
    prettyprint: bool = False

    def serialize(self, body: Any) -> str | bytes:
        assert isinstance(body, BaseModel)
        return body.model_dump_json(indent=2 if self.prettyprint else None)


@dataclass
class PydanticXmlBody(Body):
    def serialize(self, body: Any) -> str | bytes:
        assert (
            pydantic_xml is not None
        ), "pydantic-xml must be installed to use PydanticXmlBody"
        assert isinstance(body, pydantic_xml.BaseXmlModel)
        return body.to_xml()
