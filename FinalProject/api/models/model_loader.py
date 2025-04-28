from . import orders, order_details, recipes, MenuItem, resources, customers, payment_information, promotions, \
     recipes_resources,categories

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    MenuItem.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    customers.Base.metadata.create_all(engine)
    payment_information.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    recipes_resources.Base.metadata.create_all(engine)
    categories.Base.metadata.create_all(engine)
