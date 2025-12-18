import asyncio
import random
from datetime import datetime, timezone

from sqlmodel import select

from ..models.listing import Listing, Reviews
from ..db.session import init_db, async_session_maker


# ==================================================
# Review pools by sentiment
# ==================================================
GOOD_REVIEWS = [
    "Amazing stay, very clean and comfortable.",
    "Location was perfect and the host was helpful.",
    "Worth the price, would definitely recommend.",
    "The place matched the photos exactly.",
    "Had a peaceful and pleasant experience.",
    "Great amenities and smooth check-in.",
]

AVERAGE_REVIEWS = [
    "Decent stay, but could be better maintained.",
    "Location was good but rooms were average.",
    "Okay for a short stay, nothing special.",
    "Facilities were acceptable for the price.",
    "Not bad, but expected a bit more.",
]

BAD_REVIEWS = [
    "The place was not clean and poorly maintained.",
    "Photos were misleading, not worth the price.",
    "Had issues during check-in and support was slow.",
    "Rooms were smaller than expected.",
    "Would not recommend this stay.",
]


# ==================================================
# Helper: create rating + comment pair
# ==================================================
def generate_review():
    sentiment = random.choices(
        ["good", "average", "bad"],
        weights=[0.5, 0.3, 0.2],  # realistic distribution
        k=1,
    )[0]

    if sentiment == "good":
        return random.choice(GOOD_REVIEWS), random.randint(4, 5)

    if sentiment == "average":
        return random.choice(AVERAGE_REVIEWS), random.randint(2, 3)

    return random.choice(BAD_REVIEWS), random.randint(1, 2)


# ==================================================
# Seed Reviews
# ==================================================
async def seed_reviews():
    await init_db()

    async with async_session_maker() as session:
        result = await session.execute(select(Listing))
        listings = result.scalars().all()

        if not listings:
            print("❌ No listings found. Seed listings first.")
            return

        total_reviews = 0

        for listing in listings:
            # Skip if reviews already exist
            result = await session.execute(
                select(Reviews).where(Reviews.listing_uid == listing.uid)
            )
            if result.scalars().first():
                print(f"⚠️ Reviews already exist for: {listing.title}")
                continue

            # 3–5 reviews per listing
            num_reviews = random.randint(3, 5)
            reviews = []

            for _ in range(num_reviews):
                comment, rating = generate_review()

                reviews.append(
                    Reviews(
                        listing_uid=listing.uid,
                        comment=comment,
                        rating=rating,
                        created_at=datetime.now(timezone.utc),
                    )
                )

            session.add_all(reviews)
            await session.commit()

            total_reviews += len(reviews)
            print(f"✅ Seeded {len(reviews)} reviews for: {listing.title}")

        print(f"\n🎉 Total reviews seeded: {total_reviews}")


# ==================================================
# Entry point
# ==================================================
if __name__ == "__main__":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

    asyncio.run(seed_reviews())
