from typing import TYPE_CHECKING, Literal, Mapping, Union

from django.utils.translation import (
    gettext_lazy as _,
)
from wagtail.models import Page

if TYPE_CHECKING:
    from ..scraper import BaseSelectable, PageScraper
    from .analyzers import BaseAnalyzer

ERR_SCRAPIG_PAGE = _("Error scraping page: %(error)s")

ERR_PAGE_NO_TITLE = _("No title found")
ERR_PAGE_HEADING_NOT_H1 = _("First heading tag is not an h1")
ERR_PAGE_DUPLICATE_H1 = _("Duplicate h1 tag found")
ERR_PAGE_LOAD = _("Page took too long to load")
ERR_PAGE_4XX_STATUSCODE = _("Page returned a client error status code: %(status_code)s")
ERR_PAGE_5XX_STATUSCODE = _("Page returned a server error status code: %(status_code)s")
ERR_PAGE_NO_DESCRIPTION = _("No meta description found")
ERR_PAGE_NO_KEYWORDS = _("No meta keywords found")

ERR_IMAGE_NO_ALT = _("Image tag has no alt text")
ERR_IMAGE_NO_SRC = _("Image tag has no src")
ERR_ANCHOR_NO_TEXT = _("Anchor tag has no text")
ERR_ANCHOR_NO_HREF = _("Anchor tag has no href")

ERR_PAGES_DUPLICATE_TITLE = _("Duplicate title found: %(title)s")

class BaseError:
    def __init__(self,
            error_message: str,
            analyzer: Union["BaseAnalyzer", None] = None,
            weight: int = 0.99,
        ):
        self._analyzer = analyzer
        self.error_message = error_message
        self.weight = weight

    def to_json(self) -> dict:
        attrs = vars(self)
        return {k: v for k, v in attrs.items() if not k.startswith('_')}
    
    @property
    def analyzer(self) -> "BaseAnalyzer":
        return self._analyzer

class BasePageError(BaseError):
    def __init__(self,
            analyzer: "BaseAnalyzer",
            error_message: str,
            page: "PageScraper" = None,
            tag: "BaseSelectable" = None,
            weight: int = 0.99,
        ):
        super().__init__(
            analyzer=analyzer, error_message=error_message,
            weight=weight,
        )
        self.page = page
        self.tag = tag

class BaseMultiPageError(BaseError):
    def __init__(self,
            error_message: str,
            pages: list["PageScraper"],
            analyzer: "BaseAnalyzer" = None,
            weight: int = 0.99,
        ):
        super().__init__(
            analyzer=analyzer,
            error_message=error_message,
            weight=weight,
        )
        self.pages = pages

class PageError(BasePageError):
    pass

class PageWarning(BasePageError):
    pass

class MultiPageError(BaseMultiPageError):
    pass

class MultiPageWarning(BaseMultiPageError):
    pass
