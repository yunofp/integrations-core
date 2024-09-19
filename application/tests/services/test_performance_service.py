from datetime import datetime
from application.tests.populate.indications import generate_indication_data

indications = [
    {
        "_id": "66e840019ee36cc719e4a5f7",
        "indicated_client_name": "João da Silva",
        "client_email": "joao.silva@example.com",
        "client_phone": "+55 11 98765-4321",
        "inclusion_date": "2024-09-15T00:00:00.000Z",
        "rd_date": "2024-09-16T00:00:00.000Z",
        "status": "ANDAMENTO",
        "closing_date": None,
        "minimum_fee": 1500,
        "implantation_date": None,
        "aum_estimated": 500000,
        "projected_fee": 2000,
        "channel": "MKT",
        "origin": "Campanha de marketing",
        "closer": "Maria Souza",
        "contract_type": "GROW",
        "decline_reason": None,
    }
]

months_values = lambda name, year: {
    "JAN": 0,
    "FEB": 0,
    "MAR": 0,
    "APR": 0,
    "MAY": 0,
    "JUN": 0,
    "JUL": 0,
    "AUG": 0,
    "SEP": 0,
    "OCT": 0,
    "NOV": 0,
    "DEC": 0,
}


def test_process_all_indications_by_year_no_data(
    performance_service, mock_indications_repository
):
    mock_indications_repository.find_many_by_year.return_value = []

    result = performance_service.process_all_indications_by_year(2023)

    assert result == {"message": "No indications found for this year"}


def test_process_all_indications_by_year_with_data(
    performance_service, mock_indications_repository, mock_goals_repository
):

    mock_indications_repository.find_many_by_year.return_value = indications
    mock_goals_repository.find_by_names_year_ordered_by_month.side_effect = (
        months_values
    )

    result = performance_service.process_all_indications_by_year(2023)

    assert "funnel_indications" in result
    assert "indications_ordered_by_months" in result
    assert "new_mrr_by_month" in result
    assert "progress_indications" in result
    assert "five_main_places_indications" in result
    assert len(result["five_main_places_indications"]) <= 1


def test_calculate_indications_type_by_year_group_by_month(
    performance_service, mock_indications_repository, mock_goals_repository
):
    mock_indications_repository.find_many_by_year.return_value = indications
    mock_goals_repository.find_by_names_year_ordered_by_month.side_effect = (
        months_values
    )
    indications_list = []
    seven_month = datetime(2024, 7, 15).isoformat() + "Z"
    eight_month = datetime(2024, 8, 15).isoformat() + "Z"
    nine_month = datetime(2024, 9, 15).isoformat() + "Z"
    ten_month = datetime(2024, 10, 15).isoformat() + "Z"

    indications_list.append(
        generate_indication_data(
            id="66e840019ee36cc719e4a5f7", inclusion_date=seven_month
        )
    )
    indications_list.append(
        generate_indication_data(
            id="76e840019ee36cc719e4a5f7", inclusion_date=eight_month
        )
    )
    indications_list.append(
        generate_indication_data(
            id="86e840019ee36cc719e4a5f7", inclusion_date=nine_month
        )
    )

    indications_list.append(
        generate_indication_data(
            id="86e840019ee36cc719e4a5f7", inclusion_date=nine_month
        )
    )

    indications_list[2]["status"] = "REALIZADA"
    indications_list[3]["closing_date"] = ten_month
    indications_list[3]["status"] = "FECHADA"

    result = performance_service.calculate_indications_type_by_year_group_by_month(
        indications_list
    )

    assert len(result) == 3
    assert result["is_lead"]["JUL"] == 1
    assert result["is_lead"]["AUG"] == 1
    assert result["is_lead"]["SEP"] == 2

    assert result["is_rd"]["JUL"] == 0
    assert result["is_rd"]["AUG"] == 0
    assert result["is_rd"]["SEP"] == 1
    assert result["is_rd"]["OCT"] == 0

    assert result["is_client"]["JUL"] == 0
    assert result["is_client"]["AUG"] == 0
    assert result["is_client"]["SEP"] == 0
    assert result["is_client"]["OCT"] == 1


def test_indications_ordered_by_months(
    performance_service, mock_indications_repository, mock_goals_repository
):

    indications_list = []
    seven_month = datetime(2024, 1, 15).isoformat() + "Z"
    eight_month = datetime(2024, 2, 15).isoformat() + "Z"
    nine_month = datetime(2024, 3, 15).isoformat() + "Z"
    ten_month = datetime(2024, 3, 20).isoformat() + "Z"

    indications_list.append(
        generate_indication_data(
            id="66e840019ee36cc719e4a5f7",
            inclusion_date=seven_month,
            rd_date=seven_month,
        )
    )
    indications_list.append(
        generate_indication_data(
            id="76e840019ee36cc719e4a5f7",
            inclusion_date=eight_month,
            rd_date=eight_month,
        )
    )
    indications_list.append(
        generate_indication_data(
            id="86e840019ee36cc719e4a5f7",
            inclusion_date=nine_month,
            rd_date=nine_month,
            status="FECHADA",
        )
    )

    indications_list.append(
        generate_indication_data(
            id="86e840019ee36cc719e4a5f7",
            inclusion_date=nine_month,
            rd_date=ten_month,
            status="ANDAMENTO",
        )
    )

    mock_indications_repository.find_many_by_year.return_value = indications_list

    mock_goals_repository.find_by_names_year_ordered_by_month.return_value = {
        "JAN": 10,
        "FEB": 15,
        "MAR": 20,
    }

    result = performance_service.process_all_indications_by_year(2024)

    assert "indications_ordered_by_months" in result

    actual_data = result["indications_ordered_by_months"]["actual"]
    goal_data = result["indications_ordered_by_months"]["goal"]

    assert actual_data["JAN"] == 1
    assert actual_data["FEB"] == 1
    assert actual_data["MAR"] == 2

    assert goal_data["JAN"] == 10
    assert goal_data["FEB"] == 15
    assert goal_data["MAR"] == 20


def test_calculate_mrr_by_month(performance_service, mock_indications_repository):
    indications_list = []
    seven_month = datetime(2024, 7, 15).isoformat() + "Z"
    eight_month = datetime(2024, 8, 15).isoformat() + "Z"
    nine_month = datetime(2024, 9, 15).isoformat() + "Z"

    indications_list.append(
        generate_indication_data(
            id="66e840019ee36cc719e4a5f7",
            inclusion_date=seven_month,
            minimum_fee=1000,
            closing_date=seven_month,
        )
    )
    indications_list.append(
        generate_indication_data(
            id="76e840019ee36cc719e4a5f7",
            inclusion_date=eight_month,
            minimum_fee=2000,
            closing_date=eight_month,
        )
    )
    indications_list.append(
        generate_indication_data(
            id="86e840019ee36cc719e4a5f7",
            inclusion_date=nine_month,
            minimum_fee=3000,
            closing_date=nine_month,
        )
    )

    mock_indications_repository.find_many_by_year.return_value = indications_list

    result = performance_service.calculate_mrr_by_month(indications_list)

    assert len(result) == 12

    assert result["JUL"] == 1000
    assert result["AUG"] == 2000
    assert result["SEP"] == 3000


# TODO: Corrigir posicoes de indicacoes e implementar mais alguns testes
