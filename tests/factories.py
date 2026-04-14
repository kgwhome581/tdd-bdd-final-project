# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category


# pylint: disable=too-few-public-methods
class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""
        model = Product

    id = factory.Sequence(lambda n: n)

    # Задание: Список имен (Hat, Pants, Shirt и т.д.)
    name = FuzzyChoice(
        choices=[
            "Hat",
            "Pants",
            "Shirt",
            "Apple",
            "Banana",
            "Pots",
            "Towels",
            "Ford",
            "Chevy",
            "Hammer",
            "Wrench"
        ]
    )

    # Задание: Фейковый текст для описания
    description = factory.Faker("text")

    # Задание: Цена от 0.5 до 2000.0 с 2 знаками после запятой
    price = FuzzyDecimal(0.5, 2000.0, 2)

    # Задание: Доступность True или False
    available = FuzzyChoice(choices=[True, False])

    # Задание: Категории из модели данных
    category = FuzzyChoice(
        choices=[
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
