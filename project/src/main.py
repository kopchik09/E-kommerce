from abc import ABC, abstractmethod
from typing import Any, ClassVar, List, Optional

# ---------- Задание 1: абстрактный базовый класс ----------


class BaseProduct(ABC):
    """Абстрактный базовый класс товара.

    Содержит всё, что есть у каждого товара: название, описание, цену с проверками,
    количество и сложение. Создать объект этого класса нельзя.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Устанавливает новую цену. Цена не может быть нулевой или отрицательной.
        При понижении требуется подтверждение: только "y" считается согласием.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input("Цена понижается. Подтвердить? (y/n): ")
            if answer.strip().lower() != "y":
                return

        self.__price = new_price

    @property
    @abstractmethod
    def total_value(self) -> float:
        """Общая стоимость остатков товара. Каждый конкретный товар обязан её реализовать."""

    def __add__(self, other):
        """Складывает только товары одного класса: возвращает сумму их стоимостей."""
        if not isinstance(other, BaseProduct):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return self.total_value + other.total_value


# ---------- Задание 2: миксин, который печатает информацию о создании ----------


class InitLoggerMixin:
    """Миксин: при создании объекта печатает его класс и параметры."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # сначала создаём объект как обычно
        self._init_args = args
        self._init_kwargs = kwargs
        print(repr(self))

    def __repr__(self) -> str:
        params = [repr(arg) for arg in self._init_args]
        params += [f"{key}={value!r}" for key, value in self._init_kwargs.items()]
        return f"{type(self).__name__}({', '.join(params)})"


class Product(InitLoggerMixin, BaseProduct):
    """Товар. Печатает информацию о себе при создании благодаря миксину."""

    @classmethod
    def new_product(
        cls, product_data: dict[str, Any], products: Optional[List["Product"]] = None
    ) -> "Product":
        """Создаёт товар из словаря или возвращает существующий товар с тем же именем."""
        if products:
            new_name = product_data["name"].strip().lower()
            for existing in products:
                if existing.name.strip().lower() == new_name:
                    existing.quantity += product_data["quantity"]
                    if product_data["price"] > existing.price:
                        existing.price = product_data["price"]
                    return existing

        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def total_value(self) -> float:
        """Реализация абстрактного свойства: цена умножить на количество."""
        return self.price * self.quantity

    def __str__(self):
        price = int(self.price) if float(self.price).is_integer() else self.price
        return f"{self.name}, {price} руб. Остаток: {self.quantity} шт."


class Smartphone(Product):
    """Смартфон."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Газонная трава."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


# ---------- Категории и заказы ----------


def _check_product(product: object) -> None:
    """Проверяет, что объект является товаром или его наследником."""
    if not isinstance(product, Product):
        raise TypeError(
            "В категорию можно добавить только объект класса Product или его наследника"
        )


class BaseEntity(ABC):
    """Общий абстрактный класс для Category и Order."""

    @property
    @abstractmethod
    def total_quantity(self) -> int:
        """Общее количество товаров."""

    @property
    @abstractmethod
    def total_cost(self) -> float:
        """Итоговая стоимость."""


class Category(BaseEntity):
    """Категория товаров."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    name: str
    description: str
    __products: List[Product]

    def __init__(self, name: str, description: str, products: List) -> None:
        for product in products:
            _check_product(product)

        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        _check_product(product)
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает список товаров в виде строк."""
        return "\n".join(str(product) for product in self.__products)

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.__products)

    @property
    def total_cost(self) -> float:
        return sum(product.total_value for product in self.__products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."


class Order(BaseEntity):
    """Заказ: ссылка на один товар, количество и итоговая стоимость."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError(
                "В заказ можно добавить только объект класса Product или его наследника"
            )
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Количество должно быть целым положительным числом")
        if quantity > product.quantity:
            raise ValueError(f"На складе только {product.quantity} шт. товара")

        self.product = product
        self.quantity = quantity
        self.__total_cost = (
            product.price * quantity
        )  # цена фиксируется на момент заказа

    @property
    def total_quantity(self) -> int:
        return self.quantity

    @property
    def total_cost(self) -> float:
        return self.__total_cost

    def __str__(self):
        return f"Заказ: {self.product.name}, {self.quantity} шт., итого {self.total_cost} руб."
