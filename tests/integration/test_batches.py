from datetime import date, timedelta
from src.domain.model import Batch, OrderLine, allocate_order_to_batch, OutOfStock
import unittest


def make_batch_and_orderline(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku=sku, qty=batch_qty, eta=date.today()),
        OrderLine("order-001", sku=sku, qty=line_qty)
    )

class TestOrderAllocation(unittest.TestCase):

    def test_allocating_to_a_batch_reduces_available_qty(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=10)
        batch.allocate(orderline)
        self.assertEqual(batch.available_quantity, 10)

    def test_can_allocate_if_order_is_smaller_than_batch(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=10)
        self.assertTrue(batch.can_allocate(orderline))

    def test_can_allocate_if_order_size_is_equal_than_batch_size(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=20)
        self.assertTrue(batch.can_allocate(orderline))

    def test_cannot_allocate_if_order_is_bigger_than_batch(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=30)
        self.assertFalse(batch.can_allocate(orderline))

    def test_cannot_allocate_if_missmatch_between_skus(self):
        batch = Batch("batch-02", sku="RED LAMP 01", qty=10)
        orderline = OrderLine("order-001", sku="PINK CHAIR 05", qty=20)

        self.assertFalse(batch.can_allocate(orderline))

    def test_deallocated_orderline_restores_batch_quantity(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=10)
        batch.allocate(orderline)
        batch.deallocate(orderline)
        self.assertEqual(batch.available_quantity, 20)

    def test_deallocated_not_matching_orderline_doesnt_affect_batch_quantity(self):
        batch, orderline = make_batch_and_orderline(sku="RED LAMP 01", batch_qty=20, line_qty=10)
        batch.allocate(orderline)
        second_orderline = OrderLine("order-02", "PINK TOOTHBRUSH", 10)

        batch.deallocate(second_orderline)
        self.assertEqual(batch.available_quantity, 10)

    def test_prefers_in_stock_batch_to_coming_deliveries(self):
        tomorrow = date.today() + timedelta(days=1)
        in_stock_batch = Batch("b1", sku="RED LAMP 01", qty=10, eta=None)
        in_delivery_batch = Batch("b2", sku="RED LAMP 01", qty=10, eta=tomorrow)

        orderline = OrderLine("o1", sku="RED LAMP 01", qty=5)

        allocate_order_to_batch(orderline, [in_stock_batch, in_delivery_batch])

        self.assertEqual(in_stock_batch.available_quantity, 5)

    def test_prefers_earliest_delivered_batch(self):
        one_week_from_now = date.today() + timedelta(days=7)
        day_after_tomorrow = date.today() + timedelta(days=2)
        five_days_from_now = date.today() + timedelta(days=5)

        batch_arriving_in_seven_days = Batch("b1", sku="RED LAMP 01", qty=10, eta=one_week_from_now)
        batch_arriving_in_two_days = Batch("b2", sku="RED LAMP 01", qty=20, eta=day_after_tomorrow)
        batch_arriving_in_five_days = Batch("b3", sku="RED LAMP 01", qty=10, eta=five_days_from_now)

        orderline = OrderLine("o1", sku="RED LAMP 01", qty=5)

        allocate_order_to_batch(orderline, [batch_arriving_in_seven_days, batch_arriving_in_two_days, batch_arriving_in_five_days])

        self.assertEqual(batch_arriving_in_two_days.available_quantity, 15)


    def test_prefers_earliest_with_enough_batch_stock(self):
        one_week_from_now = date.today() + timedelta(days=7)
        day_after_tomorrow = date.today() + timedelta(days=2)
        five_days_from_now = date.today() + timedelta(days=5)

        batch_arriving_in_seven_days = Batch("b1", sku="RED LAMP 01", qty=10, eta=one_week_from_now)
        batch_arriving_in_two_days = Batch("b2", sku="RED LAMP 01", qty=5, eta=day_after_tomorrow)
        batch_arriving_in_five_days = Batch("b3", sku="RED LAMP 01", qty=3, eta=five_days_from_now)

        orderline = OrderLine("o1", sku="RED LAMP 01", qty=10)

        allocate_order_to_batch(orderline, [batch_arriving_in_seven_days, batch_arriving_in_two_days, batch_arriving_in_five_days])

        self.assertEqual(batch_arriving_in_seven_days.available_quantity, 0)

    def test_raises_out_of_stock_domain_exception(self):
        batch = Batch("b1", sku="RED LAMP 01", qty=10, eta=None)
        order_one = OrderLine("o1", sku="RED LAMP 01", qty=10)
        allocate_order_to_batch(order_one, [batch])

        order_two = OrderLine("o2", sku="RED LAMP 01", qty=10)
        with self.assertRaises(OutOfStock) as context:
            allocate_order_to_batch(order_two, [batch])
            self.assertEqual(str(context.exception), f"Out of stock for item with sku {order_two.sku}")


if __name__ == "__main__":
    unittest.main()