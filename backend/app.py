from litestar import Litestar
from litestar.di import Provide
from methods import lifespan, provide_db_session
from methods import home

app = Litestar(
    route_handlers=[home],
    dependencies={"db_session": Provide(provide_db_session)},
    lifespan=[lifespan],
)
