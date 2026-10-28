
import os
import json
import joblib
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vectorizer = joblib.load(
    os.path.join(BASE_DIR, "recipe_vectorizer.joblib")
)

recipe_matrix = load_npz(
    os.path.join(BASE_DIR, "recipe_matrix.npz")
)

with open(
    os.path.join(BASE_DIR, "recipes.json"),
    "r",
    encoding="utf-8"
) as f:
    recipes = json.load(f)


ALIASES = {
    "eggs": "egg",
    "tomatoes": "tomato",
    "potatoes": "potato",
    "onions": "onion",
    "parmesan cheese": "parmesan",
    "parmesan": "parmesan",
    "cheddar cheese": "cheddar",
}


def normalize_ingredient(item):
    item = str(item).lower().strip()
    return ALIASES.get(item, item)


def recommend_recipes(user_ingredients, top_n=5):
    ingredients = list(dict.fromkeys(
        normalize_ingredient(item)
        for item in user_ingredients
        if str(item).strip()
    ))

    if not ingredients:
        return []

    user_vector = vectorizer.transform(
        [" ".join(ingredients)]
    )

    similarities = cosine_similarity(
        user_vector, recipe_matrix
    ).ravel()

    available = set(ingredients)
    results = []

    for i, recipe in enumerate(recipes):
        required = set(recipe["normalized_ingredients"])

        matched = sorted(required & available)
        missing = sorted(required - available)

        if not matched:
            continue

        coverage = len(matched) / len(required) if required else 0
        score = 0.4 * similarities[i] + 0.6 * coverage

        results.append({
            "name": recipe["name"],
            "score": round(float(score), 4),
            "coverage": round(coverage * 100, 1),
            "matched_ingredients": matched,
            "missing_ingredients": missing,
            "steps": recipe["steps"]
        })

    results.sort(
        key=lambda x: (
            x["coverage"] == 100,
            x["score"],
            x["coverage"]
        ),
        reverse=True
    )

    return results[:top_n]
