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