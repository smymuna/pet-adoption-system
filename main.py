"""
Pet Adoption & Animal Shelter Management System
Main FastAPI Application Entry Point
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import uvicorn

from backend.database.connection import get_database, close_database
from backend.api.routes import dashboard, animals, adopters, adoptions, medical, volunteers, search, charts, ml_predictions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("Starting Pet Adoption System...")
    db = get_database()
    if db is None:
        print("⚠️  Warning: Database connection failed. Some features may not work.")
    else:
        print("✅ Connected to MongoDB successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down Pet Adoption System...")
    close_database()


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Pet Adoption & Animal Shelter Management System",
    description="Full-stack pet adoption management system with ML predictions",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="frontend/templates")


# Include routers - Page routes (HTML)
app.include_router(dashboard.router, tags=["Dashboard"])

# Page routes - use /page suffix to avoid conflicts
@app.get("/animals", response_class=HTMLResponse, include_in_schema=False)
async def animals_page_route(request: Request):
    from backend.api.routes.animals import animals_page
    return await animals_page(request)

@app.get("/adopters", response_class=HTMLResponse, include_in_schema=False)
async def adopters_page_route(request: Request):
    from backend.api.routes.adopters import adopters_page
    return await adopters_page(request)

@app.get("/adoptions", response_class=HTMLResponse, include_in_schema=False)
async def adoptions_page_route(request: Request):
    from backend.api.routes.adoptions import adoptions_page
    return await adoptions_page(request)

@app.get("/medical", response_class=HTMLResponse, include_in_schema=False)
async def medical_page_route(request: Request):
    from backend.api.routes.medical import medical_page
    return await medical_page(request)

@app.get("/volunteers", response_class=HTMLResponse, include_in_schema=False)
async def volunteers_page_route(request: Request):
    from backend.api.routes.volunteers import volunteers_page
    return await volunteers_page(request)

app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(charts.router, prefix="/charts", tags=["Charts"])
app.include_router(ml_predictions.router, prefix="/ml", tags=["ML Predictions"])

# Include API routers (JSON)
app.include_router(animals.router, prefix="/api/animals", tags=["Animals API"])
app.include_router(adopters.router, prefix="/api/adopters", tags=["Adopters API"])
app.include_router(adoptions.router, prefix="/api/adoptions", tags=["Adoptions API"])
app.include_router(medical.router, prefix="/api/medical", tags=["Medical API"])
app.include_router(volunteers.router, prefix="/api/volunteers", tags=["Volunteers API"])
app.include_router(search.router, prefix="/api/search", tags=["Search API"])
app.include_router(charts.router, prefix="/api/charts", tags=["Charts API"])
app.include_router(ml_predictions.router, prefix="/api/ml", tags=["ML API"])


@app.get("/")
async def root(request: Request):
    """Root endpoint - redirects to dashboard"""
    return RedirectResponse(url="/dashboard", status_code=307)


if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5001))
    reload = os.getenv("ENV", "development") == "development"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info",
        workers=1 if reload else 4  # Multiple workers in production
    )

