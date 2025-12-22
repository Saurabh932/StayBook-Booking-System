import asyncio
import random
from datetime import datetime, timezone

from sqlmodel import select

from ..models.listing import Listing, Reviews, Users   # 🔴 UPDATED
from ..db.session import init_db, async_session_maker


# ==================================================
# Review pools by sentiment
# ==================================================
GOOD_REVIEWS = [
    "Amazing stay overall — the place was spotless, well-organized, and very comfortable throughout.",
    "Fantastic location close to everything we needed, and the host was responsive and genuinely helpful.",
    "Excellent value for the price. The amenities were exactly as described and worked perfectly.",
    "The property matched the photos perfectly, with no unpleasant surprises at all.",
    "Very peaceful and relaxing stay, ideal for unwinding after a long day.",
    "Smooth check-in process, great amenities, and everything was ready when we arrived.",
]


AVERAGE_REVIEWS = [
    "Overall a decent stay, though some areas could use better maintenance.",
    "The location was convenient, but the rooms felt fairly standard and unremarkable.",
    "Fine for a short visit, but nothing really stood out compared to similar places.",
    "Facilities were acceptable for the price, though a few details could be improved.",
    "Not a bad experience overall, but it didn’t fully meet our expectations.",
]

BAD_REVIEWS = [
    "The place was not properly cleaned, and several maintenance issues were noticeable.",
    "The photos were misleading and did not accurately reflect the actual condition of the property.",
    "Check-in was problematic, and customer support took too long to resolve the issues.",
    "The rooms felt much smaller than expected and were uncomfortable for longer stays.",
    "Overall a disappointing experience, and I would not recommend this property.",
]



# ==================================================
# Helper: create rating + comment pair
# ==================================================
def generate_review():
    sentiment = random.choices(
        ["good", "average", "bad"],
        weights=[0.5, 0.3, 0.2],
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
        # --------------------------------------------------
        # 🔴 FETCH USERS (REQUIRED FOR user_id)
        # --------------------------------------------------
        users_result = await session.execute(select(Users))
        users = users_result.scalars().all()

        if not users:
            print("❌ No users found. Seed users first.")
            return

        # --------------------------------------------------
        # FETCH LISTINGS
        # --------------------------------------------------
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

                # --------------------------------------------------
                # 🔴 ASSIGN RANDOM USER AS REVIEW AUTHOR
                # --------------------------------------------------
                user = random.choice(users)

                reviews.append(
                    Reviews(
                        listing_uid=listing.uid,
                        user_id=user.uid,             # 🔴 REQUIRED
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
