from flask import current_app as app


class GoalRepository:
    def __init__(self):
        self.config = app.config
        self.collection = app.db.get_collection("goals")

    def find_by_names(self, names):
        goals = self.collection.find({"name": {"$in": names}})
        list_goals = list(goals)
        return list_goals
