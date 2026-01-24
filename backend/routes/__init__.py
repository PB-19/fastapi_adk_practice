from .login_routes import router as login_router
from .products_routes import router as products_router
from .suppliers_routes import router as suppliers_router
from .inventory_routes import router as inventory_router
from .orders_routes import router as orders_router
from .sales_routes import router as sales_router

__all__ = [
    "login_router",
    "products_router",
    "suppliers_router",
    "inventory_router",
    "orders_router",
    "sales_router"
]