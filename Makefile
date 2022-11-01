run:
	docker compose --env-file .env up --build twitter-parser redis workers

local-run:
	docker compose --env-file .development.env up --build
