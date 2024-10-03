from typing import Optional, TypedDict


class AnalyzeParameter(TypedDict):
    id: int
    title: str
    format: str
    nullable: bool
    multiple: bool


class AnalyseResponseData(TypedDict):
    status: str
    error: Optional[str]
    message: Optional[str]
    analysis: dict[str, AnalyzeParameter]
