#! /usr/bin/env python
"""PDFGetInterface: ScidbPdfGet"""
import os
import re
from pathlib import Path

import colrev.ops.pdf_get  # type: ignore[import-not-found]
import colrev.package_manager.package_settings  # type: ignore[import-not-found]
import pymupdf  # type: ignore[import-not-found]
import requests  # type: ignore[import]
from colrev.constants import Fields  # type: ignore[import-not-found]
from colrev.package_manager.interfaces import PDFGetInterface  # type: ignore[import-not-found]
from colrev.record.record import Record  # type: ignore[import-not-found]
from tenacity import retry  # type: ignore[import-not-found]
from tenacity import stop_after_attempt  # type: ignore[import-not-found]
from tenacity import wait_exponential  # type: ignore[import-not-found]
from zope.interface import implementer  # type: ignore[import-not-found]


@implementer(PDFGetInterface)
class ScidbPdfGet:
    settings_class = colrev.package_manager.package_settings.DefaultSettings

    def __init__(
        self,
        *,
        pdf_get_operation: colrev.ops.pdf_get.PDFGet,
        settings: dict,
    ) -> None:
        self.settings = self.settings_class.load_settings(data=settings)
        self.review_manager = pdf_get_operation.review_manager
        self.pdf_get_operation = pdf_get_operation

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1))
    def get_pdf(self, record: Record) -> Record:
        """Run the pdf-get operation"""

        if Fields.DOI not in record.data:
            return record

        pdf_filepath = self.pdf_get_operation.get_target_filepath(record)

        url = f"https://sci-hub.ru/{record.data[Fields.DOI]}"

        res = requests.get(
            url,
            timeout=30,
        )
        if 200 == res.status_code:
            pdf_embed = r'<embed type="application\/pdf" src="(.+?)"'
            search = re.search(pdf_embed, res.text)
            if search:
                pdf_url = search.group(1)
            else:
                return record
            if pdf_url.startswith("//"):
                pdf_url = f"https:{pdf_url}"
            else:
                pdf_url = f"https://sci-hub.ru{pdf_url}"
            pdf_res = requests.get(pdf_url, stream=True, timeout=30)
            if 200 == pdf_res.status_code:
                pdf_filepath.parents[0].mkdir(exist_ok=True, parents=True)
                with open(pdf_filepath, "wb") as file:
                    file.write(pdf_res.content)
                if self._is_pdf(path_to_file=pdf_filepath):
                    self.review_manager.report_logger.debug(
                        "Retrieved pdf (scidb):" f" {pdf_filepath.name}"
                    )
                    source = f"https://sci-hub.ru/{record.data[Fields.DOI]}"
                    record.update_field(
                        key=Fields.FILE, value=str(pdf_filepath), source=source
                    )
                    self.pdf_get_operation.import_pdf(record)
                else:
                    os.remove(pdf_filepath)
        else:
            if self.review_manager.verbose_mode:
                self.review_manager.logger.info(
                    "SciDB retrieval error " f"{res.status_code} - {url}"
                )

        return record

    def _is_pdf(self, *, path_to_file: Path) -> bool:
        try:
            with pymupdf.open(path_to_file) as doc:
                doc.load_page(0).get_text()
            return True
        except pymupdf.FileDataError:
            return False
