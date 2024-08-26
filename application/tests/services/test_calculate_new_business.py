from datetime import datetime
from bson import ObjectId


def test_calculate_mrr_by_year_group_by_month_no_entries(business_service):
    business_service.contract_repository.find_many_by_type.return_value = []
    business_service.entriesRepository.find_many_by_year_by_contracts_ids.return_value = (
        []
    )

    result = business_service.calculate_mrr_by_year_group_by_month(2023, "type", 1000)

    assert result == (
        {
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
        },
        {"goal": 1000, "actual": 0},
    )


def test_calculate_mrr_by_year_group_by_month_when_has_many_entries(business_service):
    contracts_ids = [ObjectId(), ObjectId()]
    business_service.contract_repository.find_many_by_type.return_value = [
        {
            "_id": contracts_ids[0],
            "type": "type",
            "signed_at": "2018-01-01T02:00:00.000Z",
        },
        {
            "_id": contracts_ids[1],
            "type": "type",
            "signed_at": "2018-02-01T02:00:00.000Z",
        },
    ]
    business_service.entriesRepository.find_many_by_year_by_contracts_ids.return_value = [
        {
            "_id": ObjectId(),
            "contract_id": ObjectId(),
            "code": 110001,
            "payer": {"name": "IZA CHOZE", "cpf": "35520574120"},
            "planners": [{"name": "DESCONHECIDO"}],
            "aum": {"actual": 0},
            "due_date": "2018-02-01T02:00:00.000Z",
            "payment_date": "2018-02-01T02:00:00.000Z",
            "value": 1000,
            "implemented_payment": 0,
            "status": "pending",
            "currency": "BRL",
            "created_at": "2024-07-20T18:59:48.371Z",
            "payment_method": "CARTÃO",
            "income": "",
            "budget_profile": "",
            "cancel_day": "INATIVO",
        },
        {
            "_id": ObjectId(),
            "contract_id": ObjectId(),
            "code": 110001,
            "payer": {"name": "IZA CHOZE", "cpf": "35520574120"},
            "planners": [{"name": "DESCONHECIDO"}],
            "aum": {"actual": 0},
            "due_date": "2018-03-01T02:00:00.000Z",
            "payment_date": "2018-03-01T02:00:00.000Z",
            "value": 500,
            "implemented_payment": 0,
            "status": "pending",
            "currency": "BRL",
            "created_at": "2024-08-20T18:59:48.371Z",
            "payment_method": "CARTÃO",
            "income": "",
            "budget_profile": "",
            "cancel_day": "INATIVO",
        },
    ]

    result = business_service.calculate_mrr_by_year_group_by_month(2023, "type", 1000)
    assert result == (
        {
            "JAN": 0,
            "FEB": 1000,
            "MAR": 500,
            "APR": 0,
            "MAY": 0,
            "JUN": 0,
            "JUL": 0,
            "AUG": 0,
            "SEP": 0,
            "OCT": 0,
            "NOV": 0,
            "DEC": 0,
        },
        {"goal": 1000, "actual": 0},
    )


def test_calculate_implantation_by_year_group_by_month_no_contracts(business_service):
    business_service.contract_repository.find_many_by_first_implantation_payment_date_year.return_value = (
        []
    )

    result = business_service.calculate_implantation_by_year_group_by_month(
        2023, "type", 500
    )

    assert result == (
        {
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
        },
        {"goal": 500, "actual": 0},
    )


def test_calculate_implantation_by_year_group_by_month_with_contracts(business_service):
    business_service.contract_repository.find_many_by_first_implantation_payment_date_year.return_value = [
        {
            "_id": "60d5f8a7c8b4d2c8f8f8f8f8",
            "first_implantation_payment_date": "2023-01-15",
            "implantation": 200,
        },
        {
            "_id": "60d5f8a7c8b4d2c8f8f8f8f9",
            "first_implantation_payment_date": "2023-03-20",
            "implantation": 300,
        },
        {
            "_id": "60d5f8a7c8b4d2c8f8f8f8fa",
            "first_implantation_payment_date": "2023-05-25",
            "implantation": 500,
        },
    ]

    result = business_service.calculate_implantation_by_year_group_by_month(
        2023, "type", 1000
    )

    expected_result = (
        {
            "JAN": 200,
            "FEB": 0,
            "MAR": 300,
            "APR": 0,
            "MAY": 500,
            "JUN": 0,
            "JUL": 0,
            "AUG": 0,
            "SEP": 0,
            "OCT": 0,
            "NOV": 0,
            "DEC": 0,
        },
        {"goal": 1000, "actual": 1000},
    )

    assert result == expected_result


def test_calculate_aum_estimated_by_year_group_by_month_no_contracts(business_service):
    business_service.contract_repository.find_many_by_signed_at_year.return_value = []

    result = business_service.calculate_aum_estimated_by_year_group_by_month(
        2023, "type", 2000
    )
    assert result == (
        {
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
        },
        {"goal": 2000, "actual": 0},
    )


def test_calculate_aum_estimated_by_year_group_by_month_with_contracts(
    business_service,
):
    business_service.contract_repository.find_many_by_signed_at_year.return_value = [
        {
            "_id": ObjectId(),
            "signed_at": "2023-01-15T00:00:00.000Z",
            "aum": {"estimated": 1000},
        },
        {
            "_id": ObjectId(),
            "signed_at": "2023-03-20T00:00:00.000Z",
            "aum": {"estimated": 1500},
        },
        {
            "_id": ObjectId(),
            "signed_at": "2023-05-10T00:00:00.000Z",
            "aum": {"estimated": 500},
        },
    ]

    result = business_service.calculate_aum_estimated_by_year_group_by_month(
        2023, "type", 2000
    )

    expected_result = (
        {
            "JAN": 1000,
            "FEB": 0,
            "MAR": 1500,
            "APR": 0,
            "MAY": 500,
            "JUN": 0,
            "JUL": 0,
            "AUG": 0,
            "SEP": 0,
            "OCT": 0,
            "NOV": 0,
            "DEC": 0,
        },
        {"goal": 2000, "actual": 3000},
    )

    assert result == expected_result


def test_get_new_clients_count_by_month(business_service):
    business_service.contract_repository.get_new_clients_count_by_month.return_value = 5

    result = business_service.get_new_clients_count_by_month("JAN")

    assert result == 5


def test_get_indications_count_by_month(business_service):
    business_service.indicationsRepository.get_indications_count_by_month.return_value = (
        3
    )

    result = business_service.get_indications_count_by_month(datetime.now())

    assert result == 3


def test_get_new_business_values_with_missing_year(business_service):
    result = business_service.get_new_business_values()

    assert result == {"error": "year not defined", "result": {}}


def test_get_new_business_values_with_all_values(business_service):
    # Configurar mocks para contratos e metas
    business_service.contract_repository.find_many_by_type.return_value = [
        {"_id": ObjectId(), "type": "GROW"}
    ]

    business_service.entriesRepository.find_many_by_year_by_contracts_ids.return_value = [
        {"payment_date": "2023-01-15T00:00:00.000Z", "value": 1000},
        {"payment_date": "2023-03-20T00:00:00.000Z", "value": 1500},
        {"payment_date": "2023-05-10T00:00:00.000Z", "value": 500},
    ]

    business_service.contract_repository.find_many_by_first_implantation_payment_date_year.return_value = [
        {
            "first_implantation_payment_date": "2023-02-10T00:00:00.000Z",
            "implantation": 2000,
        },
        {
            "first_implantation_payment_date": "2023-04-15T00:00:00.000Z",
            "implantation": 1500,
        },
    ]

    business_service.contract_repository.find_many_by_signed_at_year.return_value = [
        {
            "_id": ObjectId(),
            "signed_at": "2023-01-15T00:00:00.000Z",
            "aum": {"estimated": 1000},
        },
        {
            "_id": ObjectId(),
            "signed_at": "2023-03-20T00:00:00.000Z",
            "aum": {"estimated": 1500},
        },
        {
            "_id": ObjectId(),
            "signed_at": "2023-05-10T00:00:00.000Z",
            "aum": {"estimated": 500},
        },
    ]

    business_service.goals_repository.find_by_names.return_value = [
        {"name": "NOVO MRR", "value": 3000},
        {"name": "NOVO IMP", "value": 3500},
        {"name": "NOVO AUM", "value": 2000},
    ]

    business_service.indicationsRepository.get_indications_count_by_month.return_value = (
        5
    )
    business_service.contract_repository.get_new_clients_count_by_month.return_value = (
        10
    )

    now = datetime.now()

    result = business_service.get_new_business_values(year=2023, type="GROW")

    expected_result = {
        "mrr": {
            "label": "Novo MRR",
            "year": 2023,
            "months": {
                "JAN": 1000,
                "FEB": 0,
                "MAR": 1500,
                "APR": 0,
                "MAY": 500,
                "JUN": 0,
                "JUL": 0,
                "AUG": 0,
                "SEP": 0,
                "OCT": 0,
                "NOV": 0,
                "DEC": 0,
            },
            "goal": {"goal": 3000, "actual": 0},
        },
        "imp": {
            "label": "Novo IMP",
            "year": 2023,
            "months": {
                "JAN": 0,
                "FEB": 2000,
                "MAR": 0,
                "APR": 1500,
                "MAY": 0,
                "JUN": 0,
                "JUL": 0,
                "AUG": 0,
                "SEP": 0,
                "OCT": 0,
                "NOV": 0,
                "DEC": 0,
            },
            "goal": {"goal": 3500, "actual": 3500},
        },
        "aum": {
            "label": "Novo AUM",
            "year": 2023,
            "months": {
                "JAN": 1000,
                "FEB": 0,
                "MAR": 1500,
                "APR": 0,
                "MAY": 500,
                "JUN": 0,
                "JUL": 0,
                "AUG": 0,
                "SEP": 0,
                "OCT": 0,
                "NOV": 0,
                "DEC": 0,
            },
            "goal": {"goal": 2000, "actual": 3000},
        },
        "current_month": {
            "new_clients": {"label": "Novos Clientes", "value": 10},
            "indications": {"label": "Indicações", "value": 5},
        },
    }

    assert result == expected_result
