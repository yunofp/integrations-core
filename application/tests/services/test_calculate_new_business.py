from datetime import datetime


def test_calculate_mrr_by_year_group_by_month_no_entries(mock_date, business_service):
    business_service.contract_repository.find_many_by_type.return_value = []
    business_service.entriesRepository.find_many_by_year_by_contracts_ids.return_value = (
        []
    )

    result = business_service.calculate_mrr_by_year_group_by_month(2023, "type", 1000)

    assert result == (
        {"JAN": 0, "FEB": 0, "MAR": 0, "APR": 0},
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
        {"JAN": 0, "FEB": 0, "MAR": 0, "APR": 0},
        {"goal": 500, "actual": 0},
    )


def test_calculate_aum_estimated_by_year_group_by_month_no_contracts(business_service):
    business_service.contract_repository.find_many_by_signed_at_year.return_value = []

    result = business_service.calculate_aum_estimated_by_year_group_by_month(
        2023, "type", 2000
    )

    assert result == (
        {"JAN": 0, "FEB": 0, "MAR": 0, "APR": 0},
        {"goal": 2000, "actual": 0},
    )


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
