from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Awaitable,
    Callable,
    Literal,
    Mapping,
    NewType,
    Optional,
    TypedDict,
    Union,
)
from typing_extensions import NotRequired

from emcie.common.types.common import JSONSerializable


ToolId = NewType("ToolId", str)

ToolParameterType = Literal[
    "string",
    "number",
    "integer",
    "boolean",
]


class ToolParameter(TypedDict):
    type: ToolParameterType
    description: NotRequired[str]
    enum: NotRequired[list[Union[str, int, float, bool]]]


_SessionStatus = Literal["typing", "processing", "ready"]


class ToolContext:
    def __init__(
        self,
        session_id: str,
        emit_message: Optional[Callable[[str], Awaitable[None]]] = None,
        emit_status: Optional[
            Callable[
                [_SessionStatus, JSONSerializable],
                Awaitable[None],
            ]
        ] = None,
    ) -> None:
        self.session_id = session_id
        self._emit_message = emit_message
        self._emit_status = emit_status

    async def emit_message(self, message: str) -> None:
        assert self._emit_message
        await self._emit_message(message)

    async def emit_status(
        self,
        status: _SessionStatus,
        data: JSONSerializable,
    ) -> None:
        assert self._emit_status
        await self._emit_status(status, data)


@dataclass(frozen=True)
class ToolResult:
    data: JSONSerializable
    metadata: Mapping[str, JSONSerializable] = field(default_factory=dict)


@dataclass(frozen=True)
class Tool:
    id: ToolId
    creation_utc: datetime
    name: str
    description: str
    parameters: dict[str, ToolParameter]
    required: list[str]
    consequential: bool

    def __hash__(self) -> int:
        return hash(self.id)
