import asyncio
from decimal import Decimal

from sqlmodel import select

from ..models.listing import Listing
from ..db.session import init_db, async_session_maker


# ==================================================
# Helper: deterministic image per listing
# ==================================================
def image_for(title: str) -> str:
    seed = title.lower().replace(" ", "-")
    return f"https://picsum.photos/seed/{seed}/800/600"


# ==================================================
# Sample Listings (25)
# ==================================================
SAMPLE_LISTINGS = [
    {
        "title": "Cozy Apartment in Bengaluru",
        "description": "2BHK near MG Road, great for short stays.",
        "image": image_for("Cozy Apartment in Bengaluru"),
        "price": Decimal("2500.00"),
        "location": "Bengaluru, Karnataka",
        "country": "India",
    },
    {
        "title": "Hill View Stay in Manali",
        "description": "Wooden cottage with mountain view.",
        "image": image_for("Hill View Stay in Manali"),
        "price": Decimal("3200.00"),
        "location": "Manali, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Beachfront Villa in Goa",
        "description": "Private villa near Baga beach with pool.",
        "image": image_for("Beachfront Villa in Goa"),
        "price": Decimal("5800.00"),
        "location": "Calangute, Goa",
        "country": "India",
    },
    {
        "title": "Luxury Studio in Mumbai",
        "description": "Sea-facing studio apartment in Bandra.",
        "image": image_for("Luxury Studio in Mumbai"),
        "price": Decimal("7500.00"),
        "location": "Bandra, Mumbai",
        "country": "India",
    },
    {
        "title": "Peaceful Stay in Rishikesh",
        "description": "River-view cottage near Lakshman Jhula.",
        "image": image_for("Peaceful Stay in Rishikesh"),
        "price": Decimal("2800.00"),
        "location": "Rishikesh, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Houseboat Stay in Kerala",
        "description": "Traditional houseboat experience.",
        "image": image_for("Houseboat Stay in Kerala"),
        "price": Decimal("6600.00"),
        "location": "Alleppey, Kerala",
        "country": "India",
    },
    {
        "title": "Heritage Haveli in Jaipur",
        "description": "Live the royal life in a restored haveli.",
        "image": image_for("Heritage Haveli in Jaipur"),
        "price": Decimal("5400.00"),
        "location": "Jaipur, Rajasthan",
        "country": "India",
    },
    {
        "title": "Cabin in Coorg",
        "description": "Coffee estate stay surrounded by misty hills.",
        "image": image_for("Cabin in Coorg"),
        "price": Decimal("3500.00"),
        "location": "Coorg, Karnataka",
        "country": "India",
    },
    {
        "title": "Snow Lodge in Kashmir",
        "description": "Warm lodge with beautiful valley view.",
        "image": image_for("Snow Lodge in Kashmir"),
        "price": Decimal("6200.00"),
        "location": "Gulmarg, Kashmir",
        "country": "India",
    },
    {
        "title": "Modern Apartment in Hyderabad",
        "description": "Luxury apartment near Hitech City.",
        "image": image_for("Modern Apartment in Hyderabad"),
        "price": Decimal("4000.00"),
        "location": "Hitech City, Hyderabad",
        "country": "India",
    },
    {
        "title": "Eco Bamboo Stay in Wayanad",
        "description": "Beautiful bamboo cottage surrounded by nature.",
        "image": image_for("Eco Bamboo Stay in Wayanad"),
        "price": Decimal("3000.00"),
        "location": "Wayanad, Kerala",
        "country": "India",
    },
    {
        "title": "Lakeside Cottage in Ooty",
        "description": "Quiet lakeside stay with bonfire nights.",
        "image": image_for("Lakeside Cottage in Ooty"),
        "price": Decimal("3700.00"),
        "location": "Ooty, Tamil Nadu",
        "country": "India",
    },
    {
        "title": "Penthouse in Chandigarh",
        "description": "City-view penthouse with modern amenities.",
        "image": image_for("Penthouse in Chandigarh"),
        "price": Decimal("6800.00"),
        "location": "Chandigarh",
        "country": "India",
    },
    {
        "title": "Jungle Resort in Jim Corbett",
        "description": "Tiger reserve stay with safari packages.",
        "image": image_for("Jungle Resort in Jim Corbett"),
        "price": Decimal("5900.00"),
        "location": "Jim Corbett, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Desert Camp in Jaisalmer",
        "description": "Camel rides, dune bashing and cultural nights.",
        "image": image_for("Desert Camp in Jaisalmer"),
        "price": Decimal("4500.00"),
        "location": "Sam Sand Dunes, Jaisalmer",
        "country": "India",
    },
    {
        "title": "Lake View Apartment in Pune",
        "description": "2BHK premium stay near Hinjawadi IT Park.",
        "image": image_for("Lake View Apartment in Pune"),
        "price": Decimal("3200.00"),
        "location": "Pune, Maharashtra",
        "country": "India",
    },
    {
        "title": "Tea Estate Bungalow in Darjeeling",
        "description": "Vintage bungalow overlooking tea gardens.",
        "image": image_for("Tea Estate Bungalow in Darjeeling"),
        "price": Decimal("4300.00"),
        "location": "Darjeeling, West Bengal",
        "country": "India",
    },
    {
        "title": "Forest Retreat in Matheran",
        "description": "Car-free hill station stay inside forest zone.",
        "image": image_for("Forest Retreat in Matheran"),
        "price": Decimal("2800.00"),
        "location": "Matheran, Maharashtra",
        "country": "India",
    },
    {
        "title": "Island Stay in Andaman",
        "description": "Beach hut with snorkeling and scuba access.",
        "image": image_for("Island Stay in Andaman"),
        "price": Decimal("7000.00"),
        "location": "Havelock Island, Andaman",
        "country": "India",
    },
    {
        "title": "Farm Stay in Nashik",
        "description": "Grape vineyard stay with wine tasting.",
        "image": image_for("Farm Stay in Nashik"),
        "price": Decimal("3100.00"),
        "location": "Nashik, Maharashtra",
        "country": "India",
    },
    {
        "title": "Artistic Loft in Kolkata",
        "description": "Stylish loft apartment in Park Street.",
        "image": image_for("Artistic Loft in Kolkata"),
        "price": Decimal("3600.00"),
        "location": "Kolkata, West Bengal",
        "country": "India",
    },
    {
        "title": "Mountain Chalet in Kodaikanal",
        "description": "Private wooden chalet with valley views.",
        "image": image_for("Mountain Chalet in Kodaikanal"),
        "price": Decimal("4800.00"),
        "location": "Kodaikanal, Tamil Nadu",
        "country": "India",
    },
    {
        "title": "Riverside Cabin in Kasol",
        "description": "Perfect stay for backpackers and trekkers.",
        "image": image_for("Riverside Cabin in Kasol"),
        "price": Decimal("2700.00"),
        "location": "Kasol, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Royal Palace Room in Udaipur",
        "description": "Live like royalty in lakeside palace suites.",
        "image": image_for("Royal Palace Room in Udaipur"),
        "price": Decimal("9300.00"),
        "location": "Udaipur City Palace, Rajasthan",
        "country": "India",
    },
]


# ==================================================
# Seed Function
# ==================================================
async def seed():
    await init_db()

    async with async_session_maker() as session:
        result = await session.execute(select(Listing))
        listing_exist = result.scalars().first()

        if listing_exist:
            print("Database already seeded! Skipping...")
            return

        session.add_all(Listing(**data) for data in SAMPLE_LISTINGS)
        await session.commit()

        print(f"Seeded database with {len(SAMPLE_LISTINGS)} listings.")


if __name__ == "__main__":
    import selectors
    import asyncio

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

    asyncio.run(seed())