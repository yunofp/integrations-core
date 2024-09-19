def test_process_all_indications_by_year_no_data(
    performance_service, mock_indications_repository
):
    mock_indications_repository.find_many_by_year.return_value = []

    result = performance_service.process_all_indications_by_year(2023)

    assert result == {"message": "No indications found for this year"}


def test_process_all_indications_by_year_with_data(
    performance_service, mock_indications_repository, mock_goals_repository
):

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

    mock_indications_repository.find_many_by_year.return_value = indications
    mock_goals_repository.find_by_names_year_ordered_by_month.side_effect = (
        lambda name, year: {
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
    )

    result = performance_service.process_all_indications_by_year(2023)
    print(result)
    # assert "funnel_indications" in result
    # assert "indications_ordered_by_months" in result
    # assert "new_mrr_by_month" in result
    # assert "progress_indications" in result
    # assert "five_main_places_indications" in result
    # assert len(result["five_main_places_indications"]) <= 3


# def test_calculate_mrr_by_month(service):
#     indications = [
#         {"closing_date": "2023-01-15", "minimum_fee": 1000},
#         {"closing_date": "2023-02-10", "minimum_fee": 2000},
#         {"closing_date": "2023-03-05", "minimum_fee": 3000},
#     ]

#     result = service.calculate_mrr_by_month(indications)

#     expected = {
#         "JAN": 1000,
#         "FEB": 2000,
#         "MAR": 3000,
#         "APR": 0,
#         "MAY": 0,
#         "JUN": 0,
#         "JUL": 0,
#         "AUG": 0,
#         "SEP": 0,
#         "OCT": 0,
#         "NOV": 0,
#         "DEC": 0,
#     }

#     assert result == expected


# def test_calculate_indications_type_by_year_group_by_month(service):
#     indications = [
#         {
#             "inclusion_date": "2023-01-01",
#             "rd_date": "2023-02-01",
#             "closing_date": "2023-03-01",
#             "status": "FECHADA",
#         },
#         {
#             "inclusion_date": "2023-02-01",
#             "rd_date": "2023-03-01",
#             "closing_date": "2023-04-01",
#             "status": "FECHADA",
#         },
#     ]

#     result = service.calculate_indications_type_by_year_group_by_month(indications)

#     assert "is_lead" in result
#     assert "is_rd" in result
#     assert "is_client" in result


# def test_calculate_progress_indications_type_by_year_group_by_month(
#     service, mock_goals_repository
# ):
#     indications_processed = {
#         "is_lead": {"JAN": 10, "FEB": 20, "MAR": 30},
#         "is_rd": {"JAN": 5, "FEB": 15, "MAR": 25},
#         "is_client": {"JAN": 2, "FEB": 12, "MAR": 22},
#     }

#     mock_goals_repository.find_by_names_year_ordered_by_month.side_effect = [
#         {"JAN": 10, "FEB": 15, "MAR": 20},  # Leads goal
#         {"JAN": 5, "FEB": 10, "MAR": 15},  # RDs goal
#         {"JAN": 2, "FEB": 5, "MAR": 8},  # Clients goal
#     ]

#     result = service.calculate_progress_indications_type_by_year_group_by_month(
#         indications_processed, 2023
#     )

#     assert result["leads"]["actual"] == 30
#     assert result["rds"]["goal"] == 15
#     assert result["clients"]["previous"] is not None


# def test_calculate_main_places_indications(service):
#     indications = [
#         {"origin": "Referral"},
#         {"origin": "Online"},
#         {"origin": "Referral"},
#     ]

#     result = service.calculate_main_places_indications(indications)

#     assert len(result) > 0
#     assert result[0]["origin"] == "Referral"


# def test_calculate_main_places_indications_by_mrr(service):
#     indications = [
#         {"origin": "Referral", "minimum_fee": 1000},
#         {"origin": "Online", "minimum_fee": 2000},
#         {"origin": "Referral", "minimum_fee": 1500},
#     ]

#     result = service.calculate_main_places_indications_by_mrr(indications)

#     assert len(result) > 0
#     assert result[0]["mrr"] == 2500
