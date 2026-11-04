import pytest

from project.src.main import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> None:
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def products() -> list[Product]:
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]


def test_product_init(products: list[Product]) -> None:
    p = products[0]
    assert (p.name, p.description, p.price, p.quantity) == (
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
    )


def test_category_init(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    assert c.name == "Смартфоны"
    assert c.description == "Описание"
    assert c.products.count("\n") == len(products)


def test_counters_accumulate(products: list[Product]) -> None:
    Category("Смартфоны", "Описание", products)
    Category("Телевизоры", "Описание", [Product('55" QLED 4K', "Подсветка", 123000.0, 7)])
    assert Category.category_count == 2
    assert Category.product_count == 4


def test_counters_use_list_length_not_quantity(products: list[Product]) -> None:
    Category("Одна", "Описание", [products[0]])  # quantity = 5, но считается 1
    assert Category.product_count == 1


def test_counters_are_class_attributes(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    assert c.category_count == Category.category_count == 1
    assert "category_count" not in c.__dict__


# --- Задание 1 и 2: приватный список товаров, add_product, геттер ---


def test_products_list_is_private(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    assert not hasattr(c, "__products")
    assert "products" not in c.__dict__


def test_products_getter_format() -> None:
    c = Category("Смартфоны", "Описание", [Product("Iphone 15", "512GB", 80.0, 15)])
    assert c.products == "Iphone 15, 80.0 руб. Остаток: 15 шт.\n"


def test_products_getter_empty_category() -> None:
    assert Category("Пусто", "Описание", []).products == ""


def test_add_product(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", [products[0]])
    c.add_product(products[1])
    assert "Iphone 15, 210000.0 руб. Остаток: 8 шт." in c.products
    assert Category.product_count == 2


def test_add_product_wrong_type() -> None:
    c = Category("Смартфоны", "Описание", [])
    with pytest.raises(TypeError):
        c.add_product("не товар")  # type: ignore[arg-type]


def test_category_does_not_share_list_with_caller(products: list[Product]) -> None:
    c = Category("Смартфоны", "Описание", products)
    products.append(Product("Лишний", "Описание", 1.0, 1))
    assert "Лишний" not in c.products


# --- Задание 3: new_product ---


def test_new_product_creates_product() -> None:
    p = Product.new_product(
        {"name": "Iphone 15", "description": "512GB", "price": 210000.0, "quantity": 8}
    )
    assert isinstance(p, Product)
    assert (p.name, p.description, p.price, p.quantity) == ("Iphone 15", "512GB", 210000.0, 8)


def test_new_product_without_duplicates_in_list(products: list[Product]) -> None:
    p = Product.new_product(
        {"name": "Новый", "description": "Описание", "price": 100.0, "quantity": 1}, products
    )
    assert p not in products
    assert p.quantity == 1


def test_new_product_duplicate_sums_quantity_and_takes_higher_price(
    products: list[Product],
) -> None:
    p = Product.new_product(
        {"name": "iphone 15 ", "description": "512GB", "price": 220000.0, "quantity": 2},
        products,
    )
    assert p is products[1]
    assert p.quantity == 10
    assert p.price == 220000.0


def test_new_product_duplicate_keeps_old_price_if_higher(products: list[Product]) -> None:
    p = Product.new_product(
        {"name": "Iphone 15", "description": "512GB", "price": 100.0, "quantity": 2},
        products,
    )
    assert p.price == 210000.0
    assert p.quantity == 10


# --- Задание 4: приватная цена, геттер и сеттер ---


def test_price_is_private(products: list[Product]) -> None:
    assert "price" not in products[0].__dict__
    assert "_Product__price" in products[0].__dict__


def test_price_setter_raises_price(products: list[Product]) -> None:
    products[0].price = 200000.0
    assert products[0].price == 200000.0


@pytest.mark.parametrize("bad_price", [0, -1, -100.5])
def test_price_setter_rejects_non_positive(
    products: list[Product], bad_price: float, capsys: pytest.CaptureFixture[str]
) -> None:
    products[0].price = bad_price
    assert products[0].price == 180000.0
    assert "Цена не должна быть нулевая или отрицательная" in capsys.readouterr().out


def test_price_decrease_confirmed(products: list[Product], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "y")
    products[0].price = 150000.0
    assert products[0].price == 150000.0


@pytest.mark.parametrize("answer", ["n", "", "да", "yes"])
def test_price_decrease_cancelled(
    products: list[Product], monkeypatch: pytest.MonkeyPatch, answer: str
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: answer)
    products[0].price = 150000.0
    assert products[0].price == 180000.0


def test_price_increase_does_not_ask(products: list[Product], monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_: str) -> str:
        raise AssertionError("input не должен вызываться при повышении цены")

    monkeypatch.setattr("builtins.input", fail)
    products[0].price = 190000.0
    assert products[0].price == 190000.0
