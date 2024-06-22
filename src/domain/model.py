from dataclasses import dataclass
from typing import Union, Set, List
from datetime import date

@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int

class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Union[date, None] = None) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.purchased_quantity = qty
        self._allocated_orders: Set[OrderLine] = set()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self) -> int:
        return hash(self.ref)
    
    def __gt__(self, other: object) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def available_quantity(self):
        return self.purchased_quantity - self.allocated_quantity
    
    @property
    def allocated_quantity(self):
        return sum(order.qty for order in self._allocated_orders)
    
    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocated_orders.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocated_orders:
            self._allocated_orders.remove(line)

    
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    

class OutOfStock(Exception):
    pass

def allocate_order_to_batch(line: OrderLine, batches: List[Batch]) -> str:
    
    try:
        selected_batch = next(batch for batch in sorted(batches) if batch.can_allocate(line))
        selected_batch.allocate(line)
    except StopIteration:
        raise OutOfStock(f"Out of stock for item with sku {line.sku}")

    return selected_batch.reference

