import asyncio
import selectors
from decimal import Decimal

from sqlmodel import select

from ..models.listing import Listing
from ..db.session import init_db, async_session_maker


SAMPLE_LISTINGS = [
    {
        "title": "Cozy Apartment in Bengaluru",
        "description": "2BHK near MG Road, great for short stays.",
        "image": "https://example.com/img1.jpg",
        "price": Decimal("2500.00"),
        "location": "Bengaluru, Karnataka",
        "country": "India",
    },
    {
        "title": "Hill View Stay in Manali",
        "description": "Wooden cottage with mountain view.",
        "image": "https://example.com/img2.jpg",
        "price": Decimal("3200.00"),
        "location": "Manali, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Beachfront Villa in Goa",
        "description": "Private villa near Baga beach with pool.",
        "image": "https://example.com/img3.jpg",
        "price": Decimal("5800.00"),
        "location": "Calangute, Goa",
        "country": "India",
    },
    {
        "title": "Luxury Studio in Mumbai",
        "description": "Sea-facing studio apartment in Bandra.",
        "image": "https://example.com/img4.jpg",
        "price": Decimal("7500.00"),
        "location": "Bandra, Mumbai",
        "country": "India",
    },
    {
        "title": "Peaceful Stay in Rishikesh",
        "description": "River-view cottage near Lakshman Jhula.",
        "image": "https://example.com/img5.jpg",
        "price": Decimal("2800.00"),
        "location": "Rishikesh, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Business Hotel Room in Delhi",
        "description": "Premium stay with easy metro access.",
        "image": "https://example.com/img6.jpg",
        "price": Decimal("4200.00"),
        "location": "Connaught Place, Delhi",
        "country": "India",
    },
    {
        "title": "Houseboat Stay in Kerala",
        "description": "Traditional houseboat experience.",
        "image": "https://example.com/img7.jpg",
        "price": Decimal("6600.00"),
        "location": "Alleppey, Kerala",
        "country": "India",
    },
    {
        "title": "Heritage Haveli in Jaipur",
        "description": "Live the royal life in a restored haveli.",
        "image": "https://example.com/img8.jpg",
        "price": Decimal("5400.00"),
        "location": "Jaipur, Rajasthan",
        "country": "India",
    },
    {
        "title": "Cabin in Coorg",
        "description": "Coffee estate stay surrounded by misty hills.",
        "image": "https://example.com/img9.jpg",
        "price": Decimal("3500.00"),
        "location": "Coorg, Karnataka",
        "country": "India",
    },
    {
        "title": "Snow Lodge in Kashmir",
        "description": "Warm lodge with beautiful valley view.",
        "image": "https://example.com/img10.jpg",
        "price": Decimal("6200.00"),
        "location": "Gulmarg, Kashmir",
        "country": "India",
    },
]



async def seed():
    await init_db()
    
    async with async_session_maker() as session:
        ''' Checking if already seeded '''
        result = await session.execute(select(Listing))
        listing_exist = result.scalars().first()
        
        if listing_exist:
            print("Database already seeded! Skipping...")
            return
            
            
        # Insert sample listing 
        new_listings = [Listing(**data) for data in SAMPLE_LISTINGS]
        session.add_all(new_listings)
        await session.commit()
        
        print("Seeded database with sample data.")
        
        
if __name__=="__main__":
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

    asyncio.run(seed())