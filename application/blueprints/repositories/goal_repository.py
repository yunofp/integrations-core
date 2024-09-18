from flask import current_app as app

from ..utils import date as date_utils


class GoalRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("goals")

    def find_by_names(self, names):

        goals = self.collection.find({"name": {"$in": names}})
        list_goals = list(goals)
        return list_goals

    def find_by_names_year_ordered_by_month(self, name, year):
        goals = self.collection.find({"name": name, "year": year})
        list_goals = list(goals)

        months_dict, month_map = date_utils.get_months_dict_and_map()

        for goal in list_goals:
            month = goal.get("month")
            value = goal.get("value", 0)
            if month in month_map:
                months_dict[month_map[month]] += value

        return months_dict
