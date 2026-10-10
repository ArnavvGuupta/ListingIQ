
from pydantic import BaseModel, Field, ConfigDict


class ListingCreate(BaseModel):
    business_name: str = Field(min_length=1, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    city: str = Field(min_length=1, max_length=100)
    address: str | None = None
    phone: str | None = Field(default=None, max_length=30)
    source: str = Field(min_length=1, max_length=50)


class BulkListingRequest(BaseModel):
    listings: list[ListingCreate] = Field(
        min_length=1,
        max_length=1000,
    )


class ListingResponse(ListingCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
