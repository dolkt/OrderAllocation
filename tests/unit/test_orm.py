import unittest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, clear_mappers

from src.adapters import orm
from src.domain import model

class TestDatabaseOperation(unittest.TestCase):

    def setUp(self) -> None:

        self.engine = create_engine('sqlite:///:memory:')
        orm.start_mappers()
        orm.mapper_registry.metadata.create_all(self.engine)
        

        SessionFactory = sessionmaker(self.engine)
        self.session = scoped_session(SessionFactory)

        return super().setUp()

    def tearDown(self) -> None:
        self.session.remove()
        clear_mappers()
        orm.mapper_registry.metadata.drop_all(self.engine)

    def test_orderline_mapper_can_get_orderlines_from_db(self):
        self.session.execute(
            text(
                "INSERT INTO order_lines (order_id, sku, qty) VALUES "
                '("order1", "RED-CHAIR", 12),'
                '("order2", "RED-TABLE", 13),'
                '("order3", "BLUE-LIPSTICK", 14)'
            )
        )

        expected = [
            model.OrderLine("order1", "RED-CHAIR", 12),
            model.OrderLine("order2", "RED-TABLE", 13),
            model.OrderLine("order3", "BLUE-LIPSTICK", 14)
        ]

        self.assertEqual(self.session.query(model.OrderLine).all(), expected)

    def test_orderline_mapper_can_add_orderlines_to_db_as_domain_model(self):
        new_order = model.OrderLine("order1", "PINK DESK", 15)
        self.session.add(new_order)
        self.session.commit()

        rows = list(
            self.session.execute(
                text('SELECT order_id, sku, qty FROM "order_lines"')
            )
        )

        self.assertEqual(rows, [("order1", "PINK DESK", 15)])