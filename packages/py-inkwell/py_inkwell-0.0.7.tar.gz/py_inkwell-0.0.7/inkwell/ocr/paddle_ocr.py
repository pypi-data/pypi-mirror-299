# pylint: disable=duplicate-code

from typing import List

import numpy as np

from inkwell.ocr.base import BaseOCR

try:
    from paddleocr import PPStructure
except ImportError as ex:
    raise ImportError(
        "paddleocr is not available. Please install it first."
    ) from ex


class PaddleOCR(BaseOCR):
    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._load_engine()

    def _load_engine(self):
        self._engine = PPStructure(
            layout=True,
            table=False,
            ocr=True,
            show_log=False,
            return_ocr_result_in_table=True,
        )

    def _detect(self, image: np.ndarray) -> List[str]:
        text_results = []
        results = self._engine(image)
        for result in results:
            for text_box in result["res"]:
                text = text_box["text"]
                text_results.append(text)
        return text_results

    def process(self, image: np.ndarray) -> str:
        results = self._detect(image)
        return "\n".join(results)
