"""Schemas for API Responses."""

from typing import Optional, TypeVar
from pydantic import AnyUrl, BaseModel, Field
from starlette.datastructures import URL

T = TypeVar("T")

__all__ = ["PagingMixin", "PagingLinks", "Paging"]


class PagingMixin(BaseModel):
    limit: Optional[int] = Field(25, ge=0, le=1000)
    offset: Optional[int] = None


class PagingModelFormatter:

    @staticmethod
    def _format_model(model: BaseModel) -> dict:
        return model.model_dump(exclude={"offset"}, exclude_none=True)

    @staticmethod
    def format_first(url, model):
        return url.include_query_params(
            offset=0, **PagingModelFormatter._format_model(model)
        )

    @staticmethod
    def format_previous(url, model) -> Optional[AnyUrl]:
        return url.include_query_params(
            offset=model.offset - model.limit,
            **PagingModelFormatter._format_model(model)
        )

    @staticmethod
    def format_next(url, model) -> Optional[AnyUrl]:
        return url.include_query_params(
            offset=model.offset + model.limit,
            **PagingModelFormatter._format_model(model)
        )

    @staticmethod
    def format_last(url, model, total=None) -> Optional[AnyUrl]:
        if total:
            return url.include_query_params(
                offset=(total - 1) * model.limit,
                **PagingModelFormatter._format_model(model)
            )


class PagingLinks(BaseModel, PagingModelFormatter):
    """Schema for holding paging links."""

    first: Optional[AnyUrl] = None
    previous: Optional[AnyUrl] = None
    next: Optional[AnyUrl] = None
    last: Optional[AnyUrl] = None

    def __init__(
        self,
        model: Optional[BaseModel] = None,
        url: Optional[URL] = None,
        total: Optional[int] = None,
        *args,
        **kwargs
    ) -> None:
        if model and url:
            kwargs["first"] = self.format_first(url, model)
            kwargs["previous"] = self.format_previous(url, model)
            kwargs["next"] = self.format_next(url, model)
        if total is not None:
            kwargs["last"] = self.format_last(url, model, total)
        super().__init__(**kwargs)


class Paging(BaseModel):
    """Schema for paging information."""

    page: Optional[int] = None
    items: Optional[int] = None
    total_pages: Optional[int] = None
    total_items: Optional[int] = None
    links: Optional[PagingLinks] = None

    def __init__(
        self,
        model: Optional[BaseModel] = None,
        url: Optional[URL] = None,
        total: Optional[int] = None,
        **kwargs
    ) -> None:
        if model and url:
            kwargs["page"] = model.offset // model.limit + 1
            kwargs["items"] = model.limit if "items" not in kwargs else kwargs["items"]
            kwargs["total_pages"] = total // model.limit + 1 if total else None
            kwargs["total_items"] = total
            kwargs["links"] = PagingLinks(model, url, total)
        super().__init__(**kwargs)
