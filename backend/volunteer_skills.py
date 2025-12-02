"""
Volunteer Skills Definitions
Standardized list of skills for volunteer matching
"""

# Standard volunteer skills
VOLUNTEER_SKILLS = [
    "Dog Walking",
    "Dog Training",
    "Cat Socialization",
    "Small Animal Care",
    "Bird Care",
    "Grooming",
    "Feeding",
    "Medical Assistance",
    "Adoption Events",
    "Meet & Greets",
    "Photography",
    "Social Media",
    "Administrative",
    "Cleaning",
    "Transportation",
    "Behavioral Assessment",
    "Senior Animal Care",
    "Puppy/Kitten Care"
]

# Skills that match with specific animal needs
SKILL_ANIMAL_MATCHES = {
    "Dog Walking": ["Dog"],
    "Dog Training": ["Dog"],
    "Cat Socialization": ["Cat"],
    "Small Animal Care": ["Rabbit", "Hamster", "Guinea Pig", "Ferret"],
    "Bird Care": ["Bird"],
    "Senior Animal Care": [],  # Applies to all species based on age
    "Puppy/Kitten Care": ["Dog", "Cat"]  # Based on age
}

def get_skills_for_species(species: str) -> list:
    """Get relevant skills for a given species"""
    matching_skills = []
    for skill, species_list in SKILL_ANIMAL_MATCHES.items():
        if not species_list or species in species_list:
            matching_skills.append(skill)
    # Add general skills
    matching_skills.extend(["Grooming", "Feeding", "Medical Assistance", "Adoption Events", "Meet & Greets"])
    return sorted(list(set(matching_skills)))

