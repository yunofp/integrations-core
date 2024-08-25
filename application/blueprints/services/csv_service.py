import io
import pandas as pd
from datetime import datetime


class CsvService:
    def save_new_business_to_csv(self, new_business):
        data = []
        for metric_key, metric_value in new_business.items():
            if 'months' in metric_value:
                actual_value = metric_value['goal']['actual']
                goal_value = metric_value['goal']['goal']
                year = metric_value['year']
                for month_key, month_value in metric_value['months'].items():
                    data.append({
                        'Indicadores': metric_key.upper(),
                        'Meta': goal_value,
                        'Progresso': actual_value,
                        'Mês': month_key,
                        'Valor': month_value,
                        'Ano': year
                    })
            elif metric_key == "current_month":
                for _, sub_metric_value in metric_value.items():
                    data.append({
                        'Indicadores': sub_metric_value['label'].upper(),
                        'Meta': None,
                        'Progresso': sub_metric_value['value'],
                        'Mês': datetime.now().strftime('%b').upper(),
                        'Valor': sub_metric_value['value'],
                        'Ano': datetime.now().year
                    })
        df = pd.DataFrame(data)
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        return buffer.getvalue()
