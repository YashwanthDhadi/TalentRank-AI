"""
schema_loader.py

Description:
    Loads and explores the candidate schema.
"""

from pathlib import Path
from typing import Dict, List
import json


class SchemaLoader:
    """
    Loads candidate_schema.json and provides helper methods.
    """

    def __init__(self, schema_path: str):

        self.schema_path = Path(schema_path)
        self.schema = self.load_schema()

    def load_schema(self) -> Dict:

        with self.schema_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def get_schema(self) -> Dict:

        return self.schema

    def top_level_fields(self) -> List[str]:

        return list(self.schema.keys())

    def has_field(self, field_name: str) -> bool:

        return field_name in self.schema

    def field_type(self, field_name: str):

        if field_name not in self.schema:
            return None

        field = self.schema[field_name]

        if isinstance(field, dict):
            return field.get("type")

        return type(field).__name__