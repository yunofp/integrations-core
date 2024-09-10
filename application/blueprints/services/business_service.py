from application.blueprints.utils import date
from bson.objectid import ObjectId
import pandas as pd
from datetime import datetime


class BusinessService:

    def __init__(
        self,
        contract_repository,
        entries_repository,
        goals_repository,
        indicationsRepository,
    ):
        self.contract_repository = contract_repository
        self.entriesRepository = entries_repository
        self.goals_repository = goals_repository
        self.indicationsRepository = indicationsRepository

    def calculate_mrr_by_year_group_by_month(self, year, type, goal):
        months_list = date.get_months_list()
        contracts_ids = self.contract_repository.find_many_by_type(type, only_ids=True)
        contracts_ids_objects_id = [ObjectId(item["_id"]) for item in contracts_ids]

        entries = self.entriesRepository.find_many_by_year_by_contracts_ids(
            year, contracts_ids_objects_id
        )
        entries_data_frame = pd.DataFrame(entries)

        if entries_data_frame.empty:
            return {month: 0 for month in months_list}, {"goal": goal, "actual": 0}

        entries_data_frame["payment_date"] = pd.to_datetime(
            entries_data_frame["payment_date"]
        )
        entries_data_frame["month"] = (
            entries_data_frame["payment_date"].dt.strftime("%b").str.upper()
        )
        entries_data_frame["month"] = pd.Categorical(
            entries_data_frame["month"], categories=months_list, ordered=True
        )

        months_mrr = (
            entries_data_frame.groupby("month", observed=False)["value"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )

        current_month = datetime.now().strftime("%b").upper()
        actual_mrr = months_mrr.get(current_month)

        return months_mrr, {"goal": goal, "actual": actual_mrr}

    def calculate_implantation_by_year_group_by_month(self, year, type, goal):
        months_list = date.get_months_list()

        contracts = (
            self.contract_repository.find_many_by_first_implantation_payment_date_year(
                year
            )
        )

        contracts_data_frame = pd.DataFrame(contracts)

        if contracts_data_frame.empty:
            return {month: 0 for month in months_list}, {"goal": goal, "actual": 0}

        contracts_data_frame["first_implantation_payment_date"] = pd.to_datetime(
            contracts_data_frame["first_implantation_payment_date"]
        )
        contracts_data_frame["month"] = (
            contracts_data_frame["first_implantation_payment_date"]
            .dt.strftime("%b")
            .str.upper()
        )
        contracts_data_frame["month"] = pd.Categorical(
            contracts_data_frame["month"], categories=months_list, ordered=True
        )

        months_mrr = (
            contracts_data_frame.groupby("month", observed=False)["implantation"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )

        total = sum(months_mrr.values())
        return months_mrr, {"goal": goal, "actual": total}

    def calculate_aum_estimated_by_year_group_by_month(self, year, type, goal):
        months_list = date.get_months_list()

        contracts = self.contract_repository.find_many_by_signed_at_year(year)

        contracts_data_frame = pd.DataFrame(contracts)
        if contracts_data_frame.empty:
            return {month: 0 for month in months_list}, {"goal": goal, "actual": 0}

        contracts_data_frame["signed_at"] = pd.to_datetime(
            contracts_data_frame["signed_at"]
        )
        contracts_data_frame["month"] = (
            contracts_data_frame["signed_at"].dt.strftime("%b").str.upper()
        )
        contracts_data_frame["month"] = pd.Categorical(
            contracts_data_frame["month"], categories=months_list, ordered=True
        )

        contracts_data_frame["estimated"] = contracts_data_frame["aum"].apply(
            lambda x: x.get("estimated", 0)
        )

        months_mrr = (
            contracts_data_frame.groupby("month", observed=False)["estimated"]
            .sum()
            .reindex(months_list, fill_value=0)
            .to_dict()
        )
        total = sum(months_mrr.values())
        return months_mrr, {"goal": goal, "actual": total}

    def get_new_clients_count_by_month(self, month) -> int:
        if not month:
            return 0
        return self.contract_repository.get_new_clients_count_by_month(month)

    def get_indications_count_by_month(self, current_date):
        if not current_date:
            return 0
        return self.indicationsRepository.get_indications_count_by_month(current_date)

    def get_new_business_values(self, year=None, type="GROW") -> dict:
        if not year:
            return {"error": "year not defined", "result": {}}

        new_business = {"current_month": {}}
        goals = self.goals_repository.find_by_names(
            ["NOVO MRR", "NOVO IMP", "NOVO AUM"]
        )
        mrr_goal = next(
            (goal for goal in goals if goal["name"] == "NOVO MRR"),
            {"name": "NOVO MRR", "value": 0},
        )
        imp_goal = next(
            (goal for goal in goals if goal["name"] == "NOVO IMP"),
            {"name": "NOVO IMP", "value": 0},
        )
        aum_goal = next(
            (goal for goal in goals if goal["name"] == "NOVO AUM"),
            {"name": "NOVO AUM", "value": 0},
        )

        mrr_by_months, mrr_actual = self.calculate_mrr_by_year_group_by_month(
            year, type, mrr_goal["value"]
        )
        complete_mrr_data = {"months": mrr_by_months, "goal": mrr_actual}
        new_business["mrr"] = {"label": "Novo MRR", "year": year, **complete_mrr_data}

        implantation_by_months, implantation_actual = (
            self.calculate_implantation_by_year_group_by_month(
                year, type, imp_goal["value"]
            )
        )
        complete_implantation_data = {
            "months": implantation_by_months,
            "goal": implantation_actual,
        }
        new_business["imp"] = {
            "label": "Novo IMP",
            "year": year,
            **complete_implantation_data,
        }

        implantation_by_months, implantation_actual = (
            self.calculate_aum_estimated_by_year_group_by_month(
                year, type, imp_goal["value"]
            )
        )

        aum_by_months, aum_actual = self.calculate_aum_estimated_by_year_group_by_month(
            year, type, aum_goal["value"]
        )
        complete_aum_data = {"months": aum_by_months, "goal": aum_actual}
        new_business["aum"] = {"label": "Novo AUM", "year": year, **complete_aum_data}

        now = datetime.now()
        new_business["current_month"]["new_clients"] = {
            "label": "Novos Clientes",
            "value": self.get_new_clients_count_by_month(now),
        }
        new_business["current_month"]["indications"] = {
            "label": "Indicações",
            "value": self.get_indications_count_by_month(now),
        }

        return new_business
