from sqlalchemy import Table, Column, String, Integer, Date
from sqlalchemy.orm import registry
from src.domain import model

mapper_registry = registry()

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(255)),
)

# TODO - Improvement.
# Check - if foreign key to order lines can be used
# Check - if the @properties can / should be used in the database.
# batches = Table(
#     "batches",
#     mapper_registry.metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("reference", String(255)),
#     Column("sku", String(255)),
#     Column("eta", Date),
#     Column("purchased_quantity", Integer)
# )

def start_mappers():
    mapper_registry.map_imperatively(model.OrderLine, order_lines)