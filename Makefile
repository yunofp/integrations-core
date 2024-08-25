flask-dev:
	@echo "Starting Flask development server..."
	@chmod +x ./init-mongodb.sh
	@./init-mongodb.sh
	ENV_FOR_DYNACONF=development flask run

pytest:
	@pytest --cov=application --cov-report=term-missing 

pytest-cov: 
	@pytest --cov=application --cov-report=html
