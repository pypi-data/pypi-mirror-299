from django.utils.module_loading import (
    import_string,
)
from django.utils.translation import (
    gettext_lazy as _,
)

from wagtail.models import (
    Page, PageQuerySet,
)

from ..scraper import (
    PageScraper,
)
from .analyzers import (
    BaseAnalyzer,
    DEFAULT_ANALYZERS,
)
from .errors import (
    BaseError,
    MultiPageError,
    MultiPageWarning,
    PageError,
    PageWarning,
    ERR_SCRAPIG_PAGE,
)

class Analysis:
    def __init__(self,
            multi_page_errors: list[MultiPageError],
            multi_page_warnings: list[MultiPageWarning],
            single_page_errors: list[PageError],
            single_page_warnings: list[PageWarning],
            scraped_pages: list[PageScraper],
        ):
        self.multi_page_errors = multi_page_errors
        self.multi_page_warnings = multi_page_warnings
        self.single_page_errors = single_page_errors
        self.single_page_warnings = single_page_warnings
        self.scraped_pages = scraped_pages

    def to_json(self) -> dict:
        return {
            'multi_page_errors': [
                error.to_json() for error in self.multi_page_errors
            ],
            'multi_page_warnings': [
                warning.to_json() for warning in self.multi_page_warnings
            ],
            'single_page_errors': [
                error.to_json() for error in self.single_page_errors
            ],
            'single_page_warnings': [
                warning.to_json() for warning in self.single_page_warnings
            ],
            'pages': [
                page.to_json_expanded() for page in self.scraped_pages
            ],
        }
