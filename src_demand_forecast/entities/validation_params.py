from typing import List

from pydantic import BaseModel, Field


class SKUInfo(BaseModel):
    """
    The SKUInfo scheme for FastAPI.
    """

    sku_id: int = Field(..., description="The SKU ud.")
    stock: int = Field(0, description="The current stock level.")


class SKURequest(BaseModel):
    """
    The SKURequest scheme for FastAPI.
    """

    sku: SKUInfo = Field(..., description="The sku and stock level.")
    horizon_days: int = Field(7, description="The number of days in the horizon.")
    confidence_level: float = Field(0.1, description="The confidence level.")


class LowStockSKURequest(BaseModel):
    """
    The LowStockSKURequest scheme for FastAPI.
    """

    confidence_level: float = Field(..., description="The confidence level.")
    horizon_days: int = Field(..., description="The number of days in the horizon.")
    # dict of sku and stock
    sku_stock: List[SKUInfo] = Field(..., description="The sku and stock level.")
