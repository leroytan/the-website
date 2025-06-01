from api.storage.models import Assignment, Tutor
from sqlalchemy.orm.decl_api import DeclarativeMeta


class SortLogic:

    @staticmethod
    def get_sorts(TableClass: DeclarativeMeta) -> list[dict[str, str]]:
        """
        Returns a list of available sorting options for a given table class.
        """
        if TableClass == Tutor:
            return [
                {"id": "name", "name": "Name"},
                {"id": "rating", "name": "Rating"},
                {"id": "price", "name": "Price"},
            ]
        elif TableClass == Assignment:
            return [
                {"id": "title", "name": "Title"},
                {"id": "due_date", "name": "Due Date"},
                {"id": "subject", "name": "Subject"},
            ]
        else:
            return []
