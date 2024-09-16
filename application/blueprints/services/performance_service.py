import pandas
from application.blueprints.utils import date as date_utils


class PerformanceService:
    def __init__(self, indications_repository):
        self.indications_repository = indications_repository

    def calculate_indications_type_by_year_group_by_month(self, year):
        indications = self.indications_repository.find_many_by_year(year)

        if not indications:
            return {"message": "No indications found for this year"}

        indications_dataframe = pandas.DataFrame(indications)

        months_list = date_utils.get_months_list()

        indications_dataframe["month"] = (
            indications_dataframe["inclusion_date"].dt.strftime("%b").str.upper()
        )
        indications_dataframe["month"] = pandas.Categorical(
            indications_dataframe["month"], categories=months_list, ordered=True
        )

        indications_dataframe["is_lead"] = (
            (indications_dataframe["status"] == "ANDAMENTO")
            & (indications_dataframe["closing_date"].isna())
            & (indications_dataframe["implantation_date"].isna())
        )

        indications_dataframe["is_rd"] = (
            indications_dataframe["rd_date"].notna()
            & (indications_dataframe["status"] == "ANDAMENTO")
            & (indications_dataframe["closing_date"].isna())
            & (indications_dataframe["implantation_date"].isna())
        )

        indications_dataframe["is_client"] = (
            indications_dataframe["closing_date"].notna()
            & indications_dataframe["implantation_date"].notna()
        )

        list = ["is_lead", "is_rd", "is_client"]
        indications_processed = {}
        for i in list:
            indications_by_month = (
                indications_dataframe.groupby("month", observed=False)[i]
                .sum()
                .reindex(months_list, fill_value=0)
                .to_dict()
            )
            indications_processed[i] = indications_by_month

        print(indications_processed)
