from fastapi import FastAPI

import routes


app = FastAPI(
    title='ViennaRNA API',
    description='REST API for ViennaRNA (RNALib) functions'
)
app.include_router(routes.default_router)
