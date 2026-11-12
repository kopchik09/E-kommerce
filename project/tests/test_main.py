import pytest
from project.src.main import (
    BaseEntity,
    BaseProduct,
    Category,
    InitLoggerMixin,
    LawnGrass,
    Order,
    Product,
    Smartphone,
)


@pytest.fixture(autouse=True)
def reset_counters():
    """Обнуляет счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def phone1():
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def phone2():
    return Smartphone("Iphone 15", "512GB", 210000.0, 8, 98.2, "15", 512, "Gray space")


@pytest.fixture
def grass1():
    return LawnGrass(
        "Газонная трава", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый"
    )


@pytest.fixture
def grass2():
    return LawnGrass(
        "Газонная трава 2", "Выносливая", 450.0, 15, "США", "5 дней", "Темно-зеленый"
    )


# ---------- Старые тесты: Product, сеттер, new_product, Category ----------


def test_product_str():
    p = Product("Iphone 15", "512GB", 210000.0, 8)
    assert str(p) == "Iphone 15, 210000 руб. Остаток: 8 шт."


def test_price_setter_rejects_non_positive(capsys):
    p = Product("X", "d", 100.0, 1)
    p.price = 0
    assert p.price == 100.0
    assert "не должна" in capsys.readouterr().out


def test_price_decrease_confirmed(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p = Product("X", "d", 100.0, 1)
    p.price = 50.0
    assert p.price == 50.0


def test_price_decrease_rejected(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p = Product("X", "d", 100.0, 1)
    p.price = 50.0
    assert p.price == 100.0


def test_new_product_merges_duplicates():
    existing = [Product("Iphone 15", "d", 200.0, 2)]
    result = Product.new_product(
        {"name": "  iphone 15 ", "description": "d", "price": 220.0, "quantity": 3},
        existing,
    )
    assert result is existing[0]
    assert result.quantity == 5
    assert result.price == 220.0


def test_category_counters():
    Category("A", "d", [Product("X", "d", 1.0, 1)])
    assert Category.category_count == 1
    assert Category.product_count == 1


# ---------- Задание 1: абстрактные классы ----------


def test_base_product_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseProduct("X", "d", 1.0, 1)


def test_base_entity_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseEntity()


def test_subclass_without_total_value_cannot_be_created():
    class Broken(BaseProduct):
        pass

    with pytest.raises(TypeError):
        Broken("X", "d", 1.0, 1)


def test_products_are_base_products(phone1, grass1):
    assert isinstance(phone1, BaseProduct)
    assert isinstance(grass1, BaseProduct)


# ---------- Задание 2: миксин ----------


def test_product_uses_mixin():
    assert issubclass(Product, InitLoggerMixin)


def test_creation_prints_class_and_params(capsys):
    Product("Продукт1", "Описание продукта", 1200, 10)
    out = capsys.readouterr().out
    assert out.strip() == "Product('Продукт1', 'Описание продукта', 1200, 10)"


def test_repr_matches_constructor_call():
    p = Product("Продукт1", "Описание продукта", 1200, 10)
    assert repr(p) == "Product('Продукт1', 'Описание продукта', 1200, 10)"


def test_subclass_creation_prints_its_name(capsys):
    Smartphone("A", "d", 1.0, 1, 90.0, "m", 128, "c")
    assert capsys.readouterr().out.startswith("Smartphone('A', 'd', 1.0, 1)")


# ---------- Дополнительное задание: Order и BaseEntity ----------


def test_order_total_cost(phone1):
    order = Order(phone1, 2)
    assert order.total_cost == 180000.0 * 2
    assert order.total_quantity == 2


def test_order_cost_fixed_after_price_change(phone1):
    order = Order(phone1, 2)
    phone1.price = 190000.0  # повышение: input не вызывается
    assert order.total_cost == 180000.0 * 2


def test_order_rejects_non_product():
    with pytest.raises(TypeError):
        Order("не товар", 1)


def test_order_rejects_bad_quantity(phone1):
    with pytest.raises(ValueError):
        Order(phone1, 0)
    with pytest.raises(ValueError):
        Order(phone1, 100)  # на складе только 5


def test_category_and_order_are_base_entities(phone1):
    assert isinstance(Category("A", "d", []), BaseEntity)
    assert isinstance(Order(phone1, 1), BaseEntity)


def test_category_totals(phone1, phone2):
    category = Category("Смартфоны", "d", [phone1, phone2])
    assert category.total_quantity == 5 + 8
    assert category.total_cost == 180000.0 * 5 + 210000.0 * 8
