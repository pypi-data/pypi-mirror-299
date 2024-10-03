import logging

from marce_fse import models
from marcel_fse.models import SIF, Average, SentenceVectors, uSIF,view
from marcel_fse.vectors import FTVectors, Vectors

from .inputs import (
    BaseIndexedList,
    CIndexedList,
    CSplitCIndexedList,
    CSplitIndexedList,
    IndexedLineDocument,
    IndexedList,
    SplitCIndexedList,
    SplitIndexedList,
)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logger = logging.getLogger("fse")
if len(logger.handlers) == 0:  # To ensure reload() doesn't add another one
    logger.addHandler(NullHandler())


__version__ = "0.2.0"
