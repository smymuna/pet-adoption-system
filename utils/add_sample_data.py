"""
Add Sample Data
Populate the database with sample data for testing
Creates comprehensive data for all collections including multiple medical records for each animal
"""

from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import MONGO_URI, DB_NAME

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Connection error: {e}")
    sys.exit(1)

# Veterinary doctors
vet_names = [
    "Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Rodriguez", 
    "Dr. David Kim", "Dr. Lisa Thompson", "Dr. James Wilson",
    "Dr. Maria Garcia", "Dr. Robert Brown"
]

# Medical diagnoses and treatments
medical_scenarios = [
    {
        "diagnosis": "Routine health checkup",
        "treatment": "Physical examination, vaccinations (DHPP and Rabies)",
        "notes": "Animal is healthy and up-to-date on vaccinations"
    },
    {
        "diagnosis": "Spay/Neuter procedure",
        "treatment": "Surgical sterilization, post-operative care",
        "notes": "Procedure completed successfully, recovery going well"
    },
    {
        "diagnosis": "Upper respiratory infection",
        "treatment": "Antibiotics (Amoxicillin 10mg/kg twice daily for 7 days), rest",
        "notes": "Monitor for improvement, follow-up in 7 days"
    },
    {
        "diagnosis": "Dental cleaning",
        "treatment": "Professional dental scaling and polishing under anesthesia",
        "notes": "Teeth in good condition, minor tartar removed"
    },
    {
        "diagnosis": "Vaccination booster",
        "treatment": "Annual vaccination booster shots",
        "notes": "All vaccinations current"
    },
    {
        "diagnosis": "Minor skin irritation",
        "treatment": "Topical ointment (Hydrocortisone), medicated shampoo",
        "notes": "Likely due to allergies, monitor for improvement"
    },
    {
        "diagnosis": "Parasite treatment",
        "treatment": "Flea and tick prevention (Frontline), deworming medication",
        "notes": "Preventive treatment applied, schedule follow-up"
    },
    {
        "diagnosis": "Weight check and nutrition consultation",
        "treatment": "Dietary assessment, weight management plan",
        "notes": "Animal at healthy weight, continue current diet"
    },
    {
        "diagnosis": "Eye infection",
        "treatment": "Antibiotic eye drops (Tobramycin 3 times daily for 5 days)",
        "notes": "Clearing up well, continue treatment"
    },
    {
        "diagnosis": "Annual wellness exam",
        "treatment": "Complete physical exam, blood work, vaccinations",
        "notes": "All systems normal, excellent health"
    }
]

# Sample animals with full details - covering all species
animals_data = [
    # Dogs
    {
        "name": "Buddy", "species": "Dog", "breed": "Labrador Retriever", "age": 2, 
        "gender": "Male", "status": "Available", 
        "intake_date": (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Friendly and energetic, loves to play fetch. Good with children."
    },
    {
        "name": "Max", "species": "Dog", "breed": "German Shepherd", "age": 3, 
        "gender": "Male", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Loyal and protective, well-trained. Great guard dog."
    },
    {
        "name": "Shadow", "species": "Dog", "breed": "Siberian Husky", "age": 2, 
        "gender": "Male", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=160)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Energetic and friendly, loves cold weather. Great with active families."
    },
    {
        "name": "Bella", "species": "Dog", "breed": "Golden Retriever", "age": 4, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=150)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Gentle and patient, excellent with kids. Loves swimming."
    },
    {
        "name": "Daisy", "species": "Dog", "breed": "Beagle", "age": 2, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Curious and energetic, loves to sniff and explore. Good with dogs."
    },
    {
        "name": "Rocky", "species": "Dog", "breed": "Bulldog", "age": 5, 
        "gender": "Male", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=250)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Laid-back and friendly, loves to nap. Good apartment dog."
    },
    {
        "name": "Sophie", "species": "Dog", "breed": "Border Collie", "age": 3, 
        "gender": "Female", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=170)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Highly intelligent and active, needs lots of exercise. Great for active owners."
    },
    {
        "name": "Charlie", "species": "Dog", "breed": "Poodle", "age": 3, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=80)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Intelligent and playful, hypoallergenic. Great for families with allergies."
    },
    # Cats
    {
        "name": "Luna", "species": "Cat", "breed": "Persian", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Calm and affectionate, enjoys being petted. Prefers quiet environments."
    },
    {
        "name": "Whiskers", "species": "Cat", "breed": "Siamese", "age": 2, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Vocal and playful, very social. Gets along with other cats."
    },
    {
        "name": "Milo", "species": "Cat", "breed": "Maine Coon", "age": 1, 
        "gender": "Male", "status": "Medical",
        "intake_date": (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Large and friendly, recovering from surgery. Very gentle."
    },
    {
        "name": "Oreo", "species": "Cat", "breed": "Mixed Breed", "age": 3, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Independent but affectionate on his terms. Good mouser."
    },
    {
        "name": "Lily", "species": "Cat", "breed": "Ragdoll", "age": 1, 
        "gender": "Female", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Very docile and relaxed, goes limp when held. Perfect lap cat."
    },
    {
        "name": "Simba", "species": "Cat", "breed": "British Shorthair", "age": 2, 
        "gender": "Male", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Calm and easygoing, enjoys lounging. Perfect indoor cat."
    },
    {
        "name": "Zoe", "species": "Cat", "breed": "Bengal", "age": 2, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=110)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Active and athletic, loves to climb. Needs lots of stimulation."
    },
    # Rabbits
    {
        "name": "Thumper", "species": "Rabbit", "breed": "Holland Lop", "age": 1, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=75)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Friendly and curious, loves to explore. Good with gentle handling."
    },
    {
        "name": "Bunny", "species": "Rabbit", "breed": "Netherland Dwarf", "age": 2, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Small and energetic, enjoys hopping around. Needs space to exercise."
    },
    {
        "name": "Cocoa", "species": "Rabbit", "breed": "Lionhead", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=40)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Fluffy and gentle, loves being brushed. Great for families."
    },
    # Birds
    {
        "name": "Polly", "species": "Bird", "breed": "Parrot", "age": 3, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=130)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Very talkative and intelligent, can learn many words. Needs social interaction."
    },
    {
        "name": "Tweety", "species": "Bird", "breed": "Cockatiel", "age": 2, 
        "gender": "Male", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=65)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Friendly and musical, loves to whistle. Enjoys perching on shoulders."
    },
    {
        "name": "Rio", "species": "Bird", "breed": "Macaw", "age": 5, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Colorful and social, requires lots of attention and mental stimulation."
    },
    # Hamsters
    {
        "name": "Hammy", "species": "Hamster", "breed": "Syrian", "age": 1, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=25)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Active at night, loves running on wheel. Gentle when handled carefully."
    },
    {
        "name": "Nibbles", "species": "Hamster", "breed": "Dwarf Campbell", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Small and quick, enjoys burrowing. Best for older children."
    },
    # Guinea Pigs
    {
        "name": "Piglet", "species": "Guinea Pig", "breed": "American", "age": 1, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=35)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Social and vocal, makes cute squeaking sounds. Enjoys being with other guinea pigs."
    },
    {
        "name": "Ginger", "species": "Guinea Pig", "breed": "Abyssinian", "age": 2, 
        "gender": "Female", "status": "Adopted",
        "intake_date": (datetime.now() - timedelta(days=55)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Friendly and easy to handle, loves fresh vegetables. Great for kids."
    },
    # Ferrets
    {
        "name": "Bandit", "species": "Ferret", "breed": "Standard", "age": 2, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=70)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Playful and mischievous, loves to explore and hide things. Very active."
    },
    {
        "name": "Slinky", "species": "Ferret", "breed": "Standard", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Curious and energetic, enjoys interactive play. Needs supervised playtime."
    },
    # Reptiles
    {
        "name": "Spike", "species": "Reptile", "breed": "Bearded Dragon", "age": 2, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=95)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Docile and calm, enjoys basking. Easy to handle, great for beginners."
    },
    {
        "name": "Gecko", "species": "Reptile", "breed": "Leopard Gecko", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=50)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Nocturnal and gentle, easy to care for. Perfect for reptile enthusiasts."
    },
    {
        "name": "Monty", "species": "Reptile", "breed": "Ball Python", "age": 3, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=140)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Calm and docile, rarely bites. Requires proper habitat setup."
    },
    # Fish
    {
        "name": "Goldie", "species": "Fish", "breed": "Goldfish", "age": 1, 
        "gender": "Female", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Hardy and easy to care for, great for beginners. Needs proper tank setup."
    },
    {
        "name": "Bubbles", "species": "Fish", "breed": "Betta", "age": 1, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Colorful and active, prefers to be alone. Beautiful fins, easy maintenance."
    },
    {
        "name": "Nemo", "species": "Fish", "breed": "Guppy", "age": 1, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Peaceful and colorful, good for community tanks. Easy to breed."
    },
    # Other
    {
        "name": "Mystery", "species": "Other", "breed": "Other", "age": 2, 
        "gender": "Male", "status": "Available",
        "intake_date": (datetime.now() - timedelta(days=85)).strftime('%Y-%m-%d'),
        "behavioral_notes": "Unique animal, requires special care. Please inquire for more details."
    },
]

adopters_data = [
    {"name": "John Doe", "phone": "555-0101", "email": "john.doe@example.com", "address": "123 Main St, Anytown, ST 12345"},
    {"name": "Jane Smith", "phone": "555-0102", "email": "jane.smith@example.com", "address": "456 Oak Ave, Somewhere, ST 67890"},
    {"name": "Bob Johnson", "phone": "555-0103", "email": "bob.johnson@example.com", "address": "789 Pine Rd, Elsewhere, ST 11223"},
    {"name": "Sarah Williams", "phone": "555-0104", "email": "sarah.w@example.com", "address": "321 Elm St, Nowhere, ST 44556"},
    {"name": "Mike Davis", "phone": "555-0105", "email": "mike.davis@example.com", "address": "654 Maple Dr, Anywhere, ST 77889"},
    {"name": "Emily Chen", "phone": "555-0106", "email": "emily.chen@example.com", "address": "987 Cedar Ln, Springfield, ST 33445"},
    {"name": "Robert Taylor", "phone": "555-0107", "email": "robert.t@example.com", "address": "147 Birch Way, Riverside, ST 55667"},
    {"name": "Amanda White", "phone": "555-0108", "email": "amanda.white@example.com", "address": "258 Willow St, Greenfield, ST 77889"},
    {"name": "Chris Martinez", "phone": "555-0109", "email": "chris.m@example.com", "address": "369 Spruce Ave, Hilltop, ST 99001"},
    {"name": "Jessica Brown", "phone": "555-0110", "email": "jessica.brown@example.com", "address": "741 Cherry Dr, Lakeside, ST 22334"},
    {"name": "Daniel Lee", "phone": "555-0111", "email": "daniel.lee@example.com", "address": "852 Poplar Rd, Mountain View, ST 44556"},
    {"name": "Michelle Garcia", "phone": "555-0112", "email": "michelle.g@example.com", "address": "963 Ash Blvd, Oceanview, ST 66778"},
    {"name": "Kevin Anderson", "phone": "555-0113", "email": "kevin.a@example.com", "address": "159 Hickory Ct, Valley, ST 88990"},
    {"name": "Rachel Thompson", "phone": "555-0114", "email": "rachel.t@example.com", "address": "357 Walnut Pl, Summit, ST 11223"},
]

volunteers_data = [
    {"name": "Alice Brown", "phone": "555-0201", "email": "alice.brown@example.com", "skills": ["Grooming", "Feeding", "Medical Assistance"], "availability": "Weekends"},
    {"name": "Charlie Wilson", "phone": "555-0202", "email": "charlie.wilson@example.com", "skills": ["Dog Training", "Dog Walking", "Behavioral Assessment"], "availability": "Weekdays"},
    {"name": "Diana Martinez", "phone": "555-0203", "email": "diana.m@example.com", "skills": ["Medical Assistance", "Feeding", "Senior Animal Care"], "availability": "Flexible"},
    {"name": "Tom Anderson", "phone": "555-0204", "email": "tom.a@example.com", "skills": ["Cat Socialization", "Meet & Greets", "Adoption Events"], "availability": "Evenings"},
    {"name": "Grace Lee", "phone": "555-0205", "email": "grace.lee@example.com", "skills": ["Administrative", "Social Media", "Photography"], "availability": "Weekdays"},
    {"name": "Mark Johnson", "phone": "555-0206", "email": "mark.j@example.com", "skills": ["Dog Walking", "Transportation", "Cleaning"], "availability": "Mornings"},
    {"name": "Lisa Park", "phone": "555-0207", "email": "lisa.park@example.com", "skills": ["Cat Socialization", "Grooming", "Puppy/Kitten Care"], "availability": "Afternoons"},
    {"name": "Steve Rogers", "phone": "555-0208", "email": "steve.r@example.com", "skills": ["Small Animal Care", "Cleaning", "Feeding"], "availability": "Weekends"},
    {"name": "Patricia Kim", "phone": "555-0209", "email": "patricia.kim@example.com", "skills": ["Bird Care", "Grooming", "Feeding"], "availability": "Flexible"},
    {"name": "James Wright", "phone": "555-0210", "email": "james.w@example.com", "skills": ["Dog Training", "Behavioral Assessment", "Meet & Greets"], "availability": "Weekdays"},
]

print("\n📝 Adding comprehensive sample data...")

# Clear existing data
print("\n🗑️  Clearing existing data...")
db.animals.delete_many({})
db.adopters.delete_many({})
db.adoptions.delete_many({})
db.medical_records.delete_many({})
db.volunteers.delete_many({})
db.volunteer_activities.delete_many({})
print("✅ Cleared all collections")

# Insert animals
print("\n🐾 Adding animals...")
animals_result = db.animals.insert_many(animals_data)
animal_ids = list(animals_result.inserted_ids)
print(f"✅ Added {len(animal_ids)} animals")

# Insert adopters
print("\n👥 Adding adopters...")
adopters_result = db.adopters.insert_many(adopters_data)
adopter_ids = list(adopters_result.inserted_ids)
print(f"✅ Added {len(adopter_ids)} adopters")

# Insert adoptions for some animals
print("\n🤝 Adding adoptions...")
adoptions_count = 0
adopted_animals = [animal for animal in animals_data if animal["status"] == "Adopted"]

# Define adoption dates spread across multiple months (Aug 2024 to Nov 2025)
adoption_dates = [
    # 2024 dates
    "2024-08-15", "2024-08-22", "2024-08-28",
    "2024-09-05", "2024-09-12", "2024-09-18", "2024-09-25",
    "2024-10-03", "2024-10-10", "2024-10-17", "2024-10-24", "2024-10-31",
    "2024-11-07", "2024-11-14", "2024-11-21", "2024-11-28",
    "2024-12-05", "2024-12-12", "2024-12-19", "2024-12-26",
    # 2025 dates
    "2025-01-08", "2025-01-15", "2025-01-22", "2025-01-29",
    "2025-02-05", "2025-02-12", "2025-02-19", "2025-02-26",
    "2025-03-03", "2025-03-10", "2025-03-17", "2025-03-24", "2025-03-31",
    "2025-04-07", "2025-04-14", "2025-04-21", "2025-04-28",
    "2025-05-05", "2025-05-12", "2025-05-19", "2025-05-26",
    "2025-06-02", "2025-06-09", "2025-06-16", "2025-06-23", "2025-06-30",
    "2025-07-07", "2025-07-14", "2025-07-21", "2025-07-28",
    "2025-08-04", "2025-08-11", "2025-08-18", "2025-08-25",
    "2025-09-01", "2025-09-08", "2025-09-15", "2025-09-22", "2025-09-29",
    "2025-10-06", "2025-10-13", "2025-10-20", "2025-10-27",
    "2025-11-03", "2025-11-10", "2025-11-17", "2025-11-24"
]

# Assign adoption dates to adopted animals
for i, animal_data in enumerate(adopted_animals):
    animal = db.animals.find_one({"name": animal_data["name"]})
    if animal and i < len(adopter_ids):
        # Use predefined dates, or generate random if we run out
        if i < len(adoption_dates):
            adoption_date = adoption_dates[i]
        else:
            # Fallback: spread across last 6 months
            months_ago = random.randint(0, 6)
            days_ago = random.randint(0, 30)
            adoption_date = (datetime.now() - timedelta(days=months_ago*30 + days_ago)).strftime('%Y-%m-%d')
        
        adoption_data = {
            "animal_id": str(animal["_id"]),
            "adopter_id": str(adopter_ids[i % len(adopter_ids)]),  # Cycle through adopters
            "adoption_date": adoption_date,
            "notes": f"Great match! {animal_data['name']} is settling in well."
        }
        db.adoptions.insert_one(adoption_data)
        adoptions_count += 1

# Add more adoptions for available animals (change some to adopted status)
print("   Adding additional adoptions...")
additional_adoptions = 0
available_animals = [animal for animal in animals_data if animal["status"] == "Available"]
# Adopt more animals to use 2025 dates (need at least 30+ total to reach 2025)
animals_to_adopt = random.sample(available_animals, min(25, len(available_animals)))

for i, animal_data in enumerate(animals_to_adopt):
    animal = db.animals.find_one({"name": animal_data["name"]})
    if animal:
        # Use remaining adoption dates
        date_index = adoptions_count + i
        if date_index < len(adoption_dates):
            adoption_date = adoption_dates[date_index]
        else:
            # Generate date in the past 6 months
            months_ago = random.randint(0, 6)
            days_ago = random.randint(0, 30)
            adoption_date = (datetime.now() - timedelta(days=months_ago*30 + days_ago)).strftime('%Y-%m-%d')
        
        adoption_data = {
            "animal_id": str(animal["_id"]),
            "adopter_id": str(adopter_ids[(adoptions_count + i) % len(adopter_ids)]),
            "adoption_date": adoption_date,
            "notes": f"Great match! {animal_data['name']} is settling in well."
        }
        db.adoptions.insert_one(adoption_data)
        # Update animal status to Adopted
        db.animals.update_one({"_id": animal["_id"]}, {"$set": {"status": "Adopted"}})
        additional_adoptions += 1

total_adoptions = adoptions_count + additional_adoptions
print(f"✅ Added {total_adoptions} adoptions ({adoptions_count} from originally adopted animals, {additional_adoptions} newly adopted)")

# Insert medical records - MULTIPLE RECORDS FOR EACH ANIMAL
print("\n🏥 Adding medical records for each animal...")
medical_records_count = 0

for animal_id in animal_ids:
    animal = db.animals.find_one({"_id": animal_id})
    if not animal:
        continue
    
    # Get intake date
    intake_date = datetime.strptime(animal.get("intake_date", datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
    days_since_intake = (datetime.now() - intake_date).days
    
    # Determine number of visits based on days in shelter (more time = more visits)
    if days_since_intake < 30:
        num_visits = random.randint(1, 2)
    elif days_since_intake < 90:
        num_visits = random.randint(2, 4)
    elif days_since_intake < 180:
        num_visits = random.randint(3, 6)
    else:
        num_visits = random.randint(4, 8)
    
    # Create medical records spread over time
    visit_dates = []
    base_date = intake_date
    
    # First visit should be soon after intake (initial health check)
    first_visit = base_date + timedelta(days=random.randint(1, 7))
    visit_dates.append(first_visit)
    
    # Additional visits spread over time
    for i in range(1, num_visits):
        # Space visits roughly 2-8 weeks apart
        days_apart = random.randint(14, 56)
        next_date = visit_dates[-1] + timedelta(days=days_apart)
        if next_date <= datetime.now():
            visit_dates.append(next_date)
        else:
            break
    
    # Create medical record for each visit
    for visit_num, visit_date in enumerate(visit_dates):
        # First visit is usually intake exam/vaccination
        if visit_num == 0:
            scenario = random.choice([
                medical_scenarios[0],  # Routine checkup
                medical_scenarios[1],  # Spay/Neuter
                medical_scenarios[4],  # Vaccination
            ])
        elif visit_num == 1 and animal.get("status") == "Medical":
            # If animal is in medical status, might have ongoing treatment
            scenario = random.choice([
                medical_scenarios[2],  # Upper respiratory
                medical_scenarios[5],  # Skin irritation
                medical_scenarios[8],  # Eye infection
            ])
        else:
            # Random scenario for other visits
            scenario = random.choice(medical_scenarios)
        
        medical_data = {
            "animal_id": str(animal_id),
            "vet_name": random.choice(vet_names),
            "visit_date": visit_date.strftime('%Y-%m-%d'),
            "diagnosis": scenario["diagnosis"],
            "treatment": scenario["treatment"],
            "notes": scenario["notes"]
        }
        db.medical_records.insert_one(medical_data)
        medical_records_count += 1

print(f"✅ Added {medical_records_count} medical records across all animals")

# Insert volunteers
print("\n🙋 Adding volunteers...")
volunteers_result = db.volunteers.insert_many(volunteers_data)
volunteer_ids = list(volunteers_result.inserted_ids)
print(f"✅ Added {len(volunteer_ids)} volunteers")

# Assign volunteers to animals (skill-based matching)
print("\n🤝 Assigning volunteers to animals...")
volunteer_assignments = 0

# Create a mapping of species to relevant volunteer skills
species_volunteer_mapping = {
    "Dog": ["Dog Walking", "Dog Training"],
    "Cat": ["Cat Socialization"],
    "Rabbit": ["Small Animal Care"],
    "Hamster": ["Small Animal Care"],
    "Guinea Pig": ["Small Animal Care"],
    "Ferret": ["Small Animal Care"],
    "Bird": ["Bird Care"],
}

# Assign volunteers based on skills
for idx, animal in enumerate(animals_data):
    animal_id = animal_ids[idx]
    species = animal.get("species", "")
    assigned_volunteers = []
    
    # Find volunteers with matching skills
    for volunteer_idx, volunteer in enumerate(volunteers_data):
        volunteer_id = volunteer_ids[volunteer_idx]
        volunteer_skills = volunteer.get("skills", [])
        
        # Check if volunteer has relevant skills for this species
        relevant_skills = species_volunteer_mapping.get(species, [])
        general_skills = ["Grooming", "Feeding", "Medical Assistance"]
        
        # Match if volunteer has species-specific skills OR general skills
        has_relevant_skill = any(skill in volunteer_skills for skill in relevant_skills)
        has_general_skill = any(skill in volunteer_skills for skill in general_skills)
        
        if has_relevant_skill or has_general_skill:
            if len(assigned_volunteers) < 2:  # Assign max 2 volunteers per animal
                assigned_volunteers.append(str(volunteer_id))
    
    # Assign volunteers to animal (only if animal is Available)
    if assigned_volunteers and animal.get("status") == "Available":
        db.animals.update_one({'_id': animal_id}, {'$set': {'assigned_volunteers': assigned_volunteers}})
        volunteer_assignments += len(assigned_volunteers)

print(f"✅ Assigned volunteers to {volunteer_assignments} animal-volunteer pairs")

# Add volunteer activities
print("\n📝 Adding volunteer activities...")
volunteer_activities_data = []
activity_types = ["Walking", "Feeding", "Grooming", "Training", "Socialization", "Medical Assistance", "Cleaning"]

# Get all animals with assigned volunteers
animals_with_volunteers = []
for animal_id in animal_ids:
    animal = db.animals.find_one({'_id': animal_id})
    if animal and animal.get('assigned_volunteers'):
        animals_with_volunteers.append(animal)

# Generate activities for the past 30 days
if animals_with_volunteers:
    for day_offset in range(30):
        activity_date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        # Create 2-5 activities per day
        num_activities = random.randint(2, 5)
        for _ in range(num_activities):
            # Randomly select an animal with assigned volunteers
            animal = random.choice(animals_with_volunteers)
            animal_id = animal['_id']
            
            if animal.get('assigned_volunteers'):
                volunteer_id = random.choice(animal['assigned_volunteers'])
                activity_type = random.choice(activity_types)
                duration = random.randint(15, 120)  # 15 to 120 minutes
                
                notes_options = [
                    "Animal was very cooperative",
                    "Needs more practice",
                    "Excellent progress",
                    "Regular checkup completed",
                    "Animal enjoyed the activity",
                    "No issues observed",
                    "Follow-up needed",
                    "Animal responded well to training",
                    "Completed scheduled activity",
                    "Animal is making good progress"
                ]
                
                volunteer_activities_data.append({
                    "volunteer_id": volunteer_id,
                    "animal_id": str(animal_id),
                    "activity_type": activity_type,
                    "activity_date": activity_date,
                    "duration_minutes": duration,
                    "notes": random.choice(notes_options) if random.random() > 0.3 else None
                })

if volunteer_activities_data:
    activities_result = db.volunteer_activities.insert_many(volunteer_activities_data)
    print(f"✅ Added {len(activities_result.inserted_ids)} volunteer activities")
else:
    print("⚠️  No activities added (no animals have assigned volunteers)")

# Summary
print("\n" + "="*50)
print("📊 DATA POPULATION SUMMARY")
print("="*50)
print(f"🐾 Animals:           {len(animal_ids)}")
print(f"👥 Adopters:          {len(adopter_ids)}")
print(f"🤝 Adoptions:         {total_adoptions}")
print(f"🏥 Medical Records:   {medical_records_count}")
print(f"🙋 Volunteers:        {len(volunteer_ids)}")
print(f"🔗 Volunteer Assignments: {volunteer_assignments}")
print(f"📝 Volunteer Activities: {len(volunteer_activities_data)}")
print(f"📈 Avg Records/Animal: {medical_records_count / len(animal_ids):.1f}")
print("="*50)
print("\n✅ Sample data added successfully!")
client.close()

