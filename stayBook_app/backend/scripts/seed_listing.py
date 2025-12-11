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

    # -------------------------------
    # 🔥 EXTRA LISTINGS (15 more)
    # -------------------------------

    {
        "title": "Modern Apartment in Hyderabad",
        "description": "Luxury apartment near Hitech City.",
        "image": "https://example.com/img11.jpg",
        "price": Decimal("4000.00"),
        "location": "Hitech City, Hyderabad",
        "country": "India",
    },
    {
        "title": "Eco Bamboo Stay in Wayanad",
        "description": "Beautiful bamboo cottage surrounded by nature.",
        "image": "https://example.com/img12.jpg",
        "price": Decimal("3000.00"),
        "location": "Wayanad, Kerala",
        "country": "India",
    },
    {
        "title": "Lakeside Cottage in Ooty",
        "description": "Quiet lakeside stay with bonfire nights.",
        "image": "https://example.com/img13.jpg",
        "price": Decimal("3700.00"),
        "location": "Ooty, Tamil Nadu",
        "country": "India",
    },
    {
        "title": "Penthouse in Chandigarh",
        "description": "City-view penthouse with modern amenities.",
        "image": "https://example.com/img14.jpg",
        "price": Decimal("6800.00"),
        "location": "Chandigarh",
        "country": "India",
    },
    {
        "title": "Jungle Resort in Jim Corbett",
        "description": "Tiger reserve stay with safari packages.",
        "image": "https://example.com/img15.jpg",
        "price": Decimal("5900.00"),
        "location": "Jim Corbett, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Desert Camp in Jaisalmer",
        "description": "Camel rides, dune bashing and cultural nights.",
        "image": "https://example.com/img16.jpg",
        "price": Decimal("4500.00"),
        "location": "Sam Sand Dunes, Jaisalmer",
        "country": "India",
    },
    {
        "title": "Lake View Apartment in Pune",
        "description": "2BHK premium stay near Hinjawadi IT Park.",
        "image": "https://example.com/img17.jpg",
        "price": Decimal("3200.00"),
        "location": "Pune, Maharashtra",
        "country": "India",
    },
    {
        "title": "Tea Estate Bungalow in Darjeeling",
        "description": "Vintage bungalow overlooking tea gardens.",
        "image": "https://example.com/img18.jpg",
        "price": Decimal("4300.00"),
        "location": "Darjeeling, West Bengal",
        "country": "India",
    },
    {
        "title": "Forest Retreat in Matheran",
        "description": "Car-free hill station stay inside forest zone.",
        "image": "https://example.com/img19.jpg",
        "price": Decimal("2800.00"),
        "location": "Matheran, Maharashtra",
        "country": "India",
    },
    {
        "title": "Island Stay in Andaman",
        "description": "Beach hut with snorkeling and scuba access.",
        "image": "https://example.com/img20.jpg",
        "price": Decimal("7000.00"),
        "location": "Havelock Island, Andaman",
        "country": "India",
    },
    {
        "title": "Farm Stay in Nashik",
        "description": "Grape vineyard stay with wine tasting.",
        "image": "https://example.com/img21.jpg",
        "price": Decimal("3100.00"),
        "location": "Nashik, Maharashtra",
        "country": "India",
    },
    {
        "title": "River Camp in Spiti",
        "description": "Glamping tents beside the Spiti river.",
        "image": "https://example.com/img22.jpg",
        "price": Decimal("5200.00"),
        "location": "Spiti Valley, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Artistic Loft in Kolkata",
        "description": "Stylish loft apartment in Park Street.",
        "image": "https://example.com/img23.jpg",
        "price": Decimal("3600.00"),
        "location": "Kolkata, West Bengal",
        "country": "India",
    },
    {
        "title": "Mountain Chalet in Kodaikanal",
        "description": "Private wooden chalet with valley views.",
        "image": "https://example.com/img24.jpg",
        "price": Decimal("4800.00"),
        "location": "Kodaikanal, Tamil Nadu",
        "country": "India",
    },
    {
        "title": "Riverside Cabin in Kasol",
        "description": "Perfect stay for backpackers and trekkers.",
        "image": "https://example.com/img25.jpg",
        "price": Decimal("2700.00"),
        "location": "Kasol, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Skyview Apartment in Bengaluru",
        "description": "Modern 1BHK with skyline view near Indiranagar.",
        "image": "https://example.com/img26.jpg",
        "price": Decimal("3900.00"),
        "location": "Indiranagar, Bengaluru",
        "country": "India",
    },
    {
        "title": "Rustic Homestay in Shimla",
        "description": "Snow-kissed wooden cottage with fireplace.",
        "image": "https://example.com/img27.jpg",
        "price": Decimal("4800.00"),
        "location": "Shimla, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Traditional Homestay in Varanasi",
        "description": "Ghatside rooms with peaceful morning aartis.",
        "image": "https://example.com/img28.jpg",
        "price": Decimal("2900.00"),
        "location": "Assi Ghat, Varanasi",
        "country": "India",
    },
    {
        "title": "Cliffside Cottage in Pondicherry",
        "description": "Two-storey cottage near Auroville beach.",
        "image": "https://example.com/img29.jpg",
        "price": Decimal("3300.00"),
        "location": "White Town, Pondicherry",
        "country": "India",
    },
    {
        "title": "Luxury Tent in Ranthambore",
        "description": "Safari-style luxury tents near tiger reserve.",
        "image": "https://example.com/img30.jpg",
        "price": Decimal("6100.00"),
        "location": "Sawai Madhopur, Rajasthan",
        "country": "India",
    },
    {
        "title": "Golf Course Villa in Gurugram",
        "description": "Premium villa overlooking golf course.",
        "image": "https://example.com/img31.jpg",
        "price": Decimal("8900.00"),
        "location": "DLF Phase 5, Gurugram",
        "country": "India",
    },
    {
        "title": "Artist’s Studio in Chennai",
        "description": "Beach-facing studio perfect for creatives.",
        "image": "https://example.com/img32.jpg",
        "price": Decimal("3500.00"),
        "location": "Besant Nagar, Chennai",
        "country": "India",
    },
    {
        "title": "Wildlife Lodge in Bandipur",
        "description": "Calm jungle lodge with safari tours.",
        "image": "https://example.com/img33.jpg",
        "price": Decimal("5200.00"),
        "location": "Bandipur, Karnataka",
        "country": "India",
    },
    {
        "title": "Island Wooden Hut in Lakshadweep",
        "description": "Private beach hut with crystal-clear water.",
        "image": "https://example.com/img34.jpg",
        "price": Decimal("9500.00"),
        "location": "Agatti Island, Lakshadweep",
        "country": "India",
    },
    {
        "title": "Lakehouse in Bhopal",
        "description": "Beautiful lake-facing villa in the city of lakes.",
        "image": "https://example.com/img35.jpg",
        "price": Decimal("3100.00"),
        "location": "Upper Lake, Bhopal",
        "country": "India",
    },
    {
        "title": "Terracotta Hut in Bir",
        "description": "Eco-friendly hut perfect for paragliders.",
        "image": "https://example.com/img36.jpg",
        "price": Decimal("2600.00"),
        "location": "Bir Billing, Himachal Pradesh",
        "country": "India",
    },
    {
        "title": "Mountain Homestay in Tawang",
        "description": "Rare stay with stunning monastery views.",
        "image": "https://example.com/img37.jpg",
        "price": Decimal("4700.00"),
        "location": "Tawang, Arunachal Pradesh",
        "country": "India",
    },
    {
        "title": "Desert Home in Kutch",
        "description": "Mudhouse stay in the white desert region.",
        "image": "https://example.com/img38.jpg",
        "price": Decimal("2600.00"),
        "location": "Rann of Kutch, Gujarat",
        "country": "India",
    },
    {
        "title": "Rainforest Retreat in Meghalaya",
        "description": "Cottage stay near living root bridges.",
        "image": "https://example.com/img39.jpg",
        "price": Decimal("4100.00"),
        "location": "Cherrapunji, Meghalaya",
        "country": "India",
    },
    {
        "title": "Budget Stay in Nagpur",
        "description": "Simple and cozy private rooms.",
        "image": "https://example.com/img40.jpg",
        "price": Decimal("1700.00"),
        "location": "DH Road, Nagpur",
        "country": "India",
    },
    {
        "title": "Royal Palace Room in Udaipur",
        "description": "Live like royalty in lakeside palace suites.",
        "image": "https://example.com/img41.jpg",
        "price": Decimal("9300.00"),
        "location": "Udaipur City Palace, Rajasthan",
        "country": "India",
    },
    {
        "title": "Tea Garden Stay in Munnar",
        "description": "Cottage with scenic tea garden views.",
        "image": "https://example.com/img42.jpg",
        "price": Decimal("3300.00"),
        "location": "Munnar, Kerala",
        "country": "India",
    },
    {
        "title": "Hilltop Bungalow in Mussoorie",
        "description": "Bungalow with spectacular Doon Valley view.",
        "image": "https://example.com/img43.jpg",
        "price": Decimal("5600.00"),
        "location": "Mussoorie, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Minimalist Loft in Ahmedabad",
        "description": "Modern loft apartment near law garden.",
        "image": "https://example.com/img44.jpg",
        "price": Decimal("3000.00"),
        "location": "Ahmedabad, Gujarat",
        "country": "India",
    },
    {
        "title": "Eco Resort in Pachmarhi",
        "description": "Jungle eco-resort with nature trails.",
        "image": "https://example.com/img45.jpg",
        "price": Decimal("4400.00"),
        "location": "Pachmarhi, Madhya Pradesh",
        "country": "India",
    },
    {
        "title": "Dome Stay in Lonavala",
        "description": "Futuristic dome accommodation with hillside views.",
        "image": "https://example.com/img46.jpg",
        "price": Decimal("7000.00"),
        "location": "Lonavala, Maharashtra",
        "country": "India",
    },
    {
        "title": "Luxury Lake Cabin in Nainital",
        "description": "Private lake cabin perfect for romantic getaways.",
        "image": "https://example.com/img47.jpg",
        "price": Decimal("6700.00"),
        "location": "Nainital, Uttarakhand",
        "country": "India",
    },
    {
        "title": "Couple's Retreat in Kanyakumari",
        "description": "Oceanfront stay with sunrise-facing rooms.",
        "image": "https://example.com/img48.jpg",
        "price": Decimal("3600.00"),
        "location": "Kanyakumari, Tamil Nadu",
        "country": "India",
    },
    {
        "title": "Adventure Camp in Zanskar",
        "description": "High-altitude camping for trekkers.",
        "image": "https://example.com/img49.jpg",
        "price": Decimal("5500.00"),
        "location": "Zanskar Valley, Ladakh",
        "country": "India",
    },
    {
        "title": "Cliff House in Mahabaleshwar",
        "description": "Panoramic cliff-edge stay with valley views.",
        "image": "https://example.com/img50.jpg",
        "price": Decimal("4600.00"),
        "location": "Mahabaleshwar, Maharashtra",
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