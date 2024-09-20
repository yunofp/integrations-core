from datetime import datetime
from flask import current_app as app
from ..utils import date as date_utils


class IndicationsRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("indications")

    def insert_one(self, indication, mdb_session):
        # TODO: implementar validação com schema
        result = self.collection.insert_one(indication, session=mdb_session)
        return result.inserted_id

    def get_indications_count_by_month(self, date):
        converted_date = date_utils.convert_date_utc(date)
        start_date = datetime(converted_date.year, converted_date.month, 1)
        end_date = datetime(converted_date.year, converted_date.month + 1, 1)
        indications_count = self.collection.count_documents(
            {
                "inclusion_date": {"$gte": start_date, "$lt": end_date},
            }
        )
        return indications_count

    def find_many_by_year(self, year):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

        indications = self.collection.find(
            {
                "inclusion_date": {"$gte": start_date, "$lt": end_date},
            }
        )
        return list(indications)
