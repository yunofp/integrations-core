import pandas
from application.blueprints.utils import date as date_utils


class PerformanceService:
    def __init__(self, indications_repository):
        self.indications_repository = indications_repository

    def calculate_indications_type_by_year_group_by_month(self, year):
        indications = self.indications_repository.find_many_by_year(year)
        indications_dataframe = pandas.DataFrame(indications)

        months_list = date_utils.get_months_list()

        indications_dataframe["month"] = (
            indications_dataframe["inclusion_date"].dt.strftime("%b").str.upper()
        )
        indications_dataframe["month"] = pandas.Categorical(
            indications_dataframe["month"], categories=months_list, ordered=True
        )

        indications_by_month = (
            indications_dataframe.groupby("month", observed=False)["inclusion_date"]
            .count()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )
        print(indications_by_month)
