from api.router.models import AssignmentSortField, SortChoice, SortOrder
from api.storage.models import Assignment, Tutor
from sqlalchemy.orm.decl_api import DeclarativeMeta


class SortLogic:

    # Type hint sqlalchemy query object as return type
    @staticmethod
    def apply_sorting(sort_id: str, TableClass: DeclarativeMeta) -> str:
        """
        Applies sorting to a given table class based on the sort_id.
        Returns the SQLAlchemy order_by clause as a string.
        """
        if TableClass == Tutor:
            if sort_id == "name":
                return Tutor.name.asc()
            elif sort_id == "rating":
                return Tutor.rating.desc()
            elif sort_id == "price":
                return Tutor.rate.asc()
            else:
                raise ValueError(f"Invalid sort_id for Tutor: {sort_id}")
        elif TableClass == Assignment:
            if sort_id == AssignmentSortField.created_at.value:
                return Assignment.created_at.desc()
            elif sort_id == AssignmentSortField.due_date.value:
                return Assignment.due_date.asc()
            elif sort_id == AssignmentSortField.price.value:
                return Assignment.price.asc()
            else:
                raise ValueError(f"Invalid sort_id for Assignment: {sort_id}")
        else:
            raise ValueError(f"Unsupported TableClass: {TableClass}")
        
    @staticmethod
    def get_allowed_orders(field: AssignmentSortField) -> list[SortOrder]:
        """
        Return allowed orders for the given sort field.
        """
        ASC = [SortOrder.ASC]
        DESC = [SortOrder.DESC]
        BOTH = [SortOrder.ASC, SortOrder.DESC]

        match field:
            case AssignmentSortField.CREATED_AT | AssignmentSortField.ESTIMATED_RATE | AssignmentSortField.WEEKLY_FREQUENCY | AssignmentSortField.LEVEL | AssignmentSortField.TITLE:
                return BOTH
            case AssignmentSortField.RELEVANCE:
                return DESC
            case AssignmentSortField.LOCATION:
                return ASC
        return BOTH
    
    @staticmethod
    def get_choices(field: AssignmentSortField) -> list[SortChoice]:
        """
        Returns the field IDs for the given AssignmentSortField.
        """
        choices = []
        for order in SortLogic.get_allowed_orders(field):
            id = f"{field.value}_{order.value}"
            name = f"{field.name.replace('_', ' ').capitalize()} ({order.value.capitalize()})"
            choices.append(SortChoice(id=id, name=name))
        return choices

    @staticmethod
    def get_sorts(TableClass: DeclarativeMeta) -> list[SortChoice]:
        """
        Returns a list of available sorting options for a given table class.
        """
        if TableClass == Tutor:
            return [
                SortChoice(id="name", name="Name (A-Z)"),
                SortChoice(id="rating", name="Rating (High to Low)"),
                SortChoice(id="price", name="Price (Low to High)")
            ]
        elif TableClass == Assignment:
            choices = []
            for field in AssignmentSortField:
                choices.extend(SortLogic.get_choices(field))
            return choices
        else:
            return []
