import pandas
from application.blueprints.utils import date as date_utils
from datetime import datetime
from application.blueprints.utils.number import format_percentage


class PerformanceService:
    def __init__(self, indications_repository, goals_repository):
        self.indications_repository = indications_repository
        self.goals_repository = goals_repository

    def process_all_indications_by_year(self, year):
        indications = self.indications_repository.find_many_by_year(year)
        if not indications:
            return {"message": "No indications found for this year"}

        indications_by_type_ordered_by_month = (
            self.calculate_indications_type_by_year_group_by_month(indications)
        )
        calculate_progress_indications_type_by_year_group_by_month = (
            self.calculate_progress_indications_type_by_year_group_by_month(
                indications_by_type_ordered_by_month
            )
        )
        print(calculate_progress_indications_type_by_year_group_by_month)

    def calculate_indications_type_by_year_group_by_month(self, indications):

        indications_dataframe = pandas.DataFrame(indications)

        indications_dataframe["inclusion_date"] = pandas.to_datetime(
            indications_dataframe["inclusion_date"], errors="coerce"
        )
        indications_dataframe["rd_date"] = pandas.to_datetime(
            indications_dataframe["rd_date"], errors="coerce"
        )
        indications_dataframe["closing_date"] = pandas.to_datetime(
            indications_dataframe["closing_date"], errors="coerce"
        )

        months_list = date_utils.get_months_list()

        indications_dataframe["lead_month"] = (
            indications_dataframe["inclusion_date"].dt.strftime("%b").str.upper()
        )
        indications_dataframe["rd_month"] = (
            indications_dataframe["rd_date"].dt.strftime("%b").str.upper()
        )
        indications_dataframe["client_month"] = (
            indications_dataframe["closing_date"].dt.strftime("%b").str.upper()
        )

        indications_dataframe["lead_month"] = pandas.Categorical(
            indications_dataframe["lead_month"], categories=months_list, ordered=True
        )
        indications_dataframe["rd_month"] = pandas.Categorical(
            indications_dataframe["rd_month"], categories=months_list, ordered=True
        )
        indications_dataframe["client_month"] = pandas.Categorical(
            indications_dataframe["client_month"], categories=months_list, ordered=True
        )

        indications_dataframe["is_lead"] = indications_dataframe[
            "inclusion_date"
        ].notna()

        indications_dataframe["is_rd"] = indications_dataframe["rd_date"].notna() & (
            indications_dataframe["status"] == "REALIZADA"
        )

        indications_dataframe["is_client"] = indications_dataframe[
            "closing_date"
        ].notna() & (indications_dataframe["status"] == "FECHADA")

        indications_processed = {}

        indications_processed["is_lead"] = (
            indications_dataframe.groupby("lead_month", observed=False)["is_lead"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )

        indications_processed["is_rd"] = (
            indications_dataframe.groupby("rd_month", observed=False)["is_rd"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )

        indications_processed["is_client"] = (
            indications_dataframe.groupby("client_month", observed=False)["is_client"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )
        return indications_processed

    def calculate_progress_indications_type_by_year_group_by_month(
        self, indications_processed
    ):
        current_month = datetime.now().strftime("%b").upper()
        previous_month = (
            datetime.now()
            .replace(month=datetime.now().month - 1)
            .strftime("%b")
            .upper()
        )

        leads = indications_processed["is_lead"][current_month]
        rd = indications_processed["is_rd"][current_month]
        clients = indications_processed["is_client"][current_month]

        goals = self.goals_repository.find_by_names(["LEADS", "RD", "CLIENTS"])

        leads_goal = next(
            (goal for goal in goals if goal["name"] == "LEADS"),
            {"name": "LEADS", "value": 0},
        )

        rd_goal = next(
            (goal for goal in goals if goal["name"] == "RD"),
            {"name": "RD", "value": 0},
        )

        clients_goal = next(
            (goal for goal in goals if goal["name"] == "CLIENTS"),
            {"name": "CLIENTS", "value": 0},
        )
        progress = {}
        progress["leads_goal"] = leads_goal["value"]
        progress["rd_goal"] = rd_goal["value"]
        progress["clients_goal"] = clients_goal["value"]

        leads_previous_month_percentage = (
            leads - indications_processed["is_lead"][previous_month] / 100
        )
        rd_previous_month_percentage = (
            rd - indications_processed["is_rd"][previous_month] / 100
        )
        clients_previous_month_percentage = (
            clients - indications_processed["is_client"][previous_month] / 100
        )
        progress = {
            "leads": {
                "actual": leads,
                "goal": leads_goal["value"],
                "previous": format_percentage(leads_previous_month_percentage),
            },
            "rds": {
                "actual": rd,
                "goal": rd_goal["value"],
                "previous": format_percentage(rd_previous_month_percentage),
            },
            "clients": {
                "actual": clients,
                "goal": clients_goal["value"],
                "previous": format_percentage(clients_previous_month_percentage),
            },
        }

        return progress
