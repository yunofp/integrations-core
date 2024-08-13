flask-dev:
	@echo "Starting Flask development server..."
	@chmod +x ./init-mongodb.sh
	@./init-mongodb.sh
	ENV_FOR_DYNACONF=development flask run
