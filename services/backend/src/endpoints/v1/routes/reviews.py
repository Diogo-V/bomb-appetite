from fastapi import APIRouter, Request

from src.db.calls import create_review, get_review
from src.endpoints.v1.schemas.reviews import *
from src.security.authenticity import sign_data
from src.utils.logger import logger

router = APIRouter()


@router.get("/{review_id}")
async def fetch_review(request: Request, review_id: int) -> GetReviewResponse:
    user_id = request.headers.get("UserId")

    logger.info(f"Fetching review {review_id}")

    review = get_review(review_id)

    signature = sign_data(review.model_dump(), user_id)
    response = GetReviewResponse(
        data=review,
        signature=signature
    )

    logger.info(f"Review info: {response}")
    return response


@router.post("/")
async def post_review(request: PostReviewRequest) -> PostReviewResponse:
    logger.info(f"Posting review for restaurant {request.restaurantId} by user {request.userId}")

    review = create_review(
        restaurant_id=request.restaurantId,
        user_id=request.userId,
        rating=request.stars,
        review=request.comment,
        signature=request.signature,
    )

    signature = sign_data(review.model_dump(), request.userId)
    response = PostReviewResponse(
        data=review,
        signature=signature
    )

    logger.info(f"Review info: {response}")
    return response
