from typing import Type

from api.router.models import FilterChoice
from api.storage.models import Assignment, Level, Subject, Tutor, Location
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
            filter_type, _ = filter_str.split("_", 1)
            if filter_type not in parsed_filters:
                parsed_filters[filter_type] = []
            parsed_filters[filter_type].append(filter_str)
        return parsed_filters

    @staticmethod
    def get_filter(TableClass: Type[DeclarativeMeta]) -> list[FilterChoice]:
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
                FilterChoice(
                    id=getattr(row, "filter_id"),
                    name=getattr(row, "name")
                )
                for row in rows
            ]
            return items

    @staticmethod
    def get_filters(TableClass: DeclarativeMeta) -> dict[str, list[FilterChoice]]:
        """
        Returns a dictionary of available filters and their values.
        """
        if TableClass == Tutor:
            return {
                "subjects": FilterLogic.get_filter(Subject),
                "levels": FilterLogic.get_filter(Level),
            }
        elif TableClass == Assignment:
            return {
                "subjects": FilterLogic.get_filter(Subject),
                "levels": FilterLogic.get_filter(Level),
                "locations": FilterLogic.get_filter(Location),
                "courses": [],
            }
        
        return {}


