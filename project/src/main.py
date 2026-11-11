from typing import Any, ClassVar, List, Optional


class Product:
    """Товар."""

    name: str
    description: str
    quantity: int
    __price: float

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
        """Устанавливает новую цену.

        Цена не может быть нулевой или отрицательной. Если цена понижается,
        требуется подтверждение пользователя: только "y" считается согласием.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input("Цена понижается. Подтвердить? (y/n): ")
            if answer.strip().lower() != "y":
                return

        self.__price = new_price

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

    def __str__(self):
        price = int(self.price) if float(self.price).is_integer() else self.price
        return f"{self.name}, {price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Складывает товары одного класса: возвращает общую стоимость остатков."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return self.price * self.quantity + other.price * other.quantity


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


def _check_product(product: object) -> None:
    """Проверяет, что объект является товаром или его наследником."""
    if not isinstance(product, Product):
        raise TypeError(
            "В категорию можно добавить только объект класса Product или его наследника"
        )


class Category:
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

    def __str__(self):
        total = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."


if __name__ == "__main__":
    # твой блок с примерами без изменений
    ...