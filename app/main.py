from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings
from app.core.logging import get_logger, setup_logging
from app.services.search_service import SearchService

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Furniture Search Engine",
    description="A furniture search engine built with Azure AI services",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize settings and search service
settings = Settings()
search_service = SearchService()


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Furniture Search API"}


@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


@app.post("/search")
async def search_furniture(
    query: str,
    category: Optional[str] = None,
    style: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    color: Optional[str] = None,
    materials: Optional[List[str]] = None,
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    try:
        logger.info(
            "Starting search",
            query=query,
            category=category,
            style=style,
            min_price=min_price,
            max_price=max_price,
            color=color,
            materials=materials,
            page=page,
            page_size=page_size,
        )

        # Construct filter expression
        filters = []
        if category:
            filters.append(f"category eq '{category}'")
        if style:
            filters.append(f"style eq '{style}'")
        if min_price is not None:
            filters.append(f"price ge {min_price}")
        if max_price is not None:
            filters.append(f"price le {max_price}")
        if color is not None:
            filters.append(f"color eq '{color}'")
        if materials:
            material_filters = [
                f"materials/any(m: m eq '{material}')" for material in materials
            ]
            filters.append(f"({' and '.join(material_filters)})")

        filter_expression = " and ".join(filters) if filters else None
        logger.debug("Constructed filter expression", filter=filter_expression)

        # Perform search
        results = await search_service.search(query=query)
        logger.info("Search completed", result_count=len(results))

        response = {
            "query": query,
            "filters": filter_expression,
            "results": results,
            "total": len(results),
        }
        return response
    except Exception as e:
        logger.error(
            "Error performing search",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail=f"Error performing search: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
