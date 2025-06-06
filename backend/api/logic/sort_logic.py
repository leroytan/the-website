from api.router.models import AssignmentSortField, SortChoice, SortOrder
from api.storage.models import Assignment, Tutor, Level
from sqlalchemy.orm.decl_api import DeclarativeMeta


class SortLogic:

    @staticmethod
    def parse_sort_id(sort_id: str) -> tuple[str, SortOrder]:
        """
        Parses the sort_id into a field and order.
        Returns a tuple of (field, order).
        """
        # Let the sort_id be empty string if no sorting is applied
        if sort_id == "":
            return "", SortOrder.DESC
        elif "_" not in sort_id:
            raise ValueError(f"Invalid sort_id format: {sort_id}")
        
        field, order_str = sort_id.rsplit("_", 1)
        order = SortOrder(order_str.lower())
        
        return field.lower(), order

    # Type hint sqlalchemy query object as return type
    @staticmethod
    def get_sorting(TableClass: DeclarativeMeta, sort_id: str) -> str:
        """
        Applies sorting to a given table class based on the sort_id.
        Returns the SQLAlchemy order_by clause as a string.
        """

        field, order = SortLogic.parse_sort_id(sort_id)

        if TableClass == Assignment:
            field = AssignmentSortField(field)
            match field:
                case AssignmentSortField.DEFAULT | AssignmentSortField.CREATED_AT:
                    return Assignment.created_at.desc() if order == SortOrder.DESC else Assignment.created_at.asc()
                case AssignmentSortField.estimated_rate_hourly:
                    return Assignment.estimated_rate_hourly.desc() if order == SortOrder.DESC else Assignment.estimated_rate_hourly.asc()
                case AssignmentSortField.WEEKLY_FREQUENCY:
                    return Assignment.weekly_frequency.desc() if order == SortOrder.DESC else Assignment.weekly_frequency.asc()
                case AssignmentSortField.LEVEL:  # Level has a explicit sort order
                    return Level.sort_order.desc() if order == SortOrder.DESC else Level.sort_order.asc()
                case AssignmentSortField.TITLE:
                    return Assignment.title.desc() if order == SortOrder.DESC else Assignment.title.asc()
                case AssignmentSortField.LOCATION:
                    raise ValueError("Location sorting is not supported yet.")
                    return Assignment.location.asc() if order == SortOrder.ASC else Assignment.location.desc()
                case AssignmentSortField.RELEVANCE:
                    raise ValueError("Relevance sorting is not supported yet.")
                    return Assignment.relevance.desc()
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
            case AssignmentSortField.CREATED_AT | AssignmentSortField.estimated_rate_hourly | AssignmentSortField.WEEKLY_FREQUENCY | AssignmentSortField.LEVEL | AssignmentSortField.TITLE:
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
