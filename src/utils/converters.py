from datetime import datetime, date
from typing import Any, Optional

import pandas as pd


class Converters:

    @staticmethod
    def to_int(value: Any) -> Optional[int]:
        """
        Converte qualquer valor numérico para int.
        """

        if pd.isna(value):
            return None

        if value in ("", None):
            return None

        try:
            return int(value)

        except (ValueError, TypeError):
            return None

    @staticmethod
    def to_float(value: Any) -> Optional[float]:

        if pd.isna(value):
            return None

        if value in ("", None):
            return None

        try:
            return float(value)

        except (ValueError, TypeError):
            return None

    @staticmethod
    def to_str(value: Any) -> Optional[str]:

        if pd.isna(value):
            return None

        if value is None:
            return None

        texto = str(value).strip()

        if texto == "":
            return None

        return texto

    @staticmethod
    def to_bool(value: Any) -> bool:

        if isinstance(value, bool):
            return value

        if value is None:
            return False

        texto = str(value).strip().lower()

        return texto in (
            "true",
            "1",
            "yes",
            "y",
            "active",
            "ativo"
        )

    @staticmethod
    def to_date(value: Any) -> Optional[date]:

        if pd.isna(value):
            return None

        if value in ("", None):
            return None

        texto = str(value)

        try:

            return datetime.strptime(
                texto[:10],
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return None
