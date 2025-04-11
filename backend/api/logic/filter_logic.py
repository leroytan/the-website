from typing import Type

from api.storage.models import Assignment, Level, Subject, Tutor
from api.storage.storage_service import StorageService
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta


class FilterLogic:
    """
    Logic class for filtering tutors based on various criteria.
    """

    @staticmethod
    def parse_filters(filters: list[str]) -> dict[str, list[str]]:
        """
        Parse a list of filter strings into a dictionary of filter types and values.
        Each filter string should be in the format "filterType_filterValue".
        """
        parsed_filters = {}
        for filter_str in filters:
            filter_type, filter_value = filter_str.split("_", 1)
            if filter_type not in parsed_filters:
                parsed_filters[filter_type] = []
            parsed_filters[filter_type].append(filter_value)
        return parsed_filters

    @staticmethod
    def get_filter(TableClass: Type[DeclarativeMeta]) -> list[dict[str, str]]:
        """
        Returns a list of available filters and their values for a given filter name.
        """
        with Session(StorageService.engine) as session:
            rows = StorageService.find(
                session=session,
                query={},
                TableClass=TableClass,
                find_one=False
            )
            items = [
                {
                    "id": getattr(row, "filterId"),
                    "name": getattr(row, "name")
                }
                for row in rows
            ]
            return items

    @staticmethod
    def get_filters(TableClass: DeclarativeMeta) -> dict[str, list[dict[str, str]]]:
        """
        Returns a dictionary of available filters and their values.
        """
        if TableClass == Tutor:
            return {
                "subject": FilterLogic.get_filter(Subject),
                "level": FilterLogic.get_filter(Level),
                "location": [],
            }
        elif TableClass == Assignment:
            return {
                "subject": FilterLogic.get_filter(Subject),
                "level": FilterLogic.get_filter(Level),
                "course": [],
            }
        
        return {}


