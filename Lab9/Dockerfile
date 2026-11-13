FROM python:3.11-slim

WORKDIR /app

COPY *.py inventory.json products.csv ./
COPY tests/ ./tests/

CMD ["python", "inventory_managerOOPv1.py"]
