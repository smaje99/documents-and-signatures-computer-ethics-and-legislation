# 🚀 Ejecutar FastAPI
run:
	uv run fastapi run app/app.py

# 🚀 Ejecutar FastAPI en modo de desarrollo
dev:
	uv run fastapi dev app/app.py

# 🔍 Ejecutar linters
lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

# 🛠️ Formatear el código
format:
	uv run ruff format .

# 🧪 Ejecutar pruebas
test:
	uv run pytest
