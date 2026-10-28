
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from recommend import recommend_recipes

app = FastAPI(
    title="SABI Recipe Recommendation API",
    description="API rekomendasi resep berdasarkan bahan pengguna",
    version="1.0.0"
)


class RecommendationRequest(BaseModel):
    ingredients: list[str] = Field(
        ...,
        min_length=1,
        description="Daftar bahan yang tersedia"
    )
    top_n: int = Field(default=5, ge=1, le=20)


@app.get("/")
def home():
    return {
        "message": "SABI Recipe API aktif",
        "docs": "/docs"
    }


@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    ingredients = [
        item.strip()
        for item in request.ingredients
        if item.strip()
    ]

    if not ingredients:
        raise HTTPException(
            status_code=400,
            detail="Daftar bahan tidak boleh kosong"
        )

    try:
        results = recommend_recipes(
            ingredients,
            top_n=request.top_n
        )

        return {
            "success": True,
            "input_ingredients": ingredients,
            "total": len(results),
            "recommendations": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Gagal memproses rekomendasi resep"
        ) from error
