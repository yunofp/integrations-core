flask dev:
	@echo "Starting Flask development server..."
	@docker-compose -f docker-compose.development.yml up -d && ENV_FOR_DYNACONF=development flask run 