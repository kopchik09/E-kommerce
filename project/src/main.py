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
        """Создаёт товар из словаря.

        Если передан список products и в нём уже есть товар с таким же именем,
        то количество складывается, а цена берётся более высокая.
        В этом случае возвращается уже существующий товар.
        """
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
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """Категория товаров."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    name: str
    description: str
    __products: List[Product]

    def __init__(self, name: str, description: str, products: List) -> None:
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавить только объект класса Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает список товаров в виде строк:
        'Название, 80 руб. Остаток: 15 шт.'
        """
        return "\n".join(str(product) for product in self.__products)

    def __str__(self):
        total = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."


# if __name__ == "__main__":
#     product1 = Product(
#         "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
#     )
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2],
#     )
#     print(category1.products)
#
#     category1.add_product(product3)
#     print(category1.products)
#     print(Category.product_count)
#
#     product4 = Product.new_product(
#         {
#             "name": '55" QLED 4K',
#             "description": "Фоновая подсветка",
#             "price": 123000.0,
#             "quantity": 7,
#         }
#     )
#     category2 = Category(
#         "Телевизоры",
#         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
#         [product4],
#     )
#     print(category2.products)
#
#     # Дубликат: количество складывается, цена берётся большая
#     duplicate = Product.new_product(
#         {
#             "name": "Iphone 15",
#             "description": "512GB, Gray space",
#             "price": 220000.0,
#             "quantity": 2,
#         },
#         [product1, product2, product3],
#     )
#     print(duplicate is product2, duplicate.quantity, duplicate.price)
#
#     # Проверка сеттера цены
#     product1.price = 0
#     product1.price = 190000.0
#     print(product1.price)
#
#     print(Category.category_count)
#     print(Category.product_count)

if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
