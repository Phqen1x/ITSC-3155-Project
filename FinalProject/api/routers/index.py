<<<<<<< Updated upstream
from . import orders, order_details, resources
=======
from . import (orders, order_details, resources, promotions, categories,
               recipes, menu_item)
>>>>>>> Stashed changes


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(resources.router)
<<<<<<< Updated upstream
=======
    app.include_router(promotions.router)
    app.include_router(categories.router)
    app.include_router(recipes.router)
    app.include_router(menu_item.router)
>>>>>>> Stashed changes
