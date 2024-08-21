from datetime import datetime
from flask import current_app as app

class IndicationsService:

  def __init__(self, indicationsRepository = None):
    self.indicationsRepository = indicationsRepository
  
  def get_indications_count_by_month(self):
    current_date = datetime.now()
    return self.indicationsRepository.get_indications_count_by_month(current_date)