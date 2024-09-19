from datetime import datetime


def generate_indication_data(**kwargs):
    indication = {
        "_id": kwargs.get("id", "66e840019ee36cc719e4a5f7"),
        "indicated_client_name": kwargs.get("indicated_client_name", "João da Silva"),
        "client_email": kwargs.get("client_email", "joao.silva@example.com"),
        "client_phone": kwargs.get("client_phone", "+55 11 98765-4321"),
        "inclusion_date": kwargs.get(
            "inclusion_date", datetime(2024, 9, 15).isoformat() + "Z"
        ),
        "rd_date": kwargs.get("rd_date", datetime(2024, 9, 16).isoformat() + "Z"),
        "status": kwargs.get("status", "ANDAMENTO"),
        "closing_date": kwargs.get("closing_date"),
        "minimum_fee": kwargs.get("minimum_fee", 1500),
        "implantation_date": kwargs.get("implantation_date"),
        "aum_estimated": kwargs.get("aum_estimated", 500000),
        "projected_fee": kwargs.get("projected_fee", 2000),
        "channel": kwargs.get("channel", "MKT"),
        "origin": kwargs.get("origin", "Campanha de marketing"),
        "closer": kwargs.get("closer", "Maria Souza"),
        "contract_type": kwargs.get("contract_type", "GROW"),
        "decline_reason": kwargs.get("decline_reason"),
    }

    return indication
