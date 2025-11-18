"""
Species and Breed Definitions
Mapping of species to their breeds
"""

SPECIES_BREEDS = {
    "Dog": [
        "Labrador Retriever", "Golden Retriever", "German Shepherd", "Bulldog", "Beagle",
        "French Bulldog", "Poodle", "Rottweiler", "Yorkshire Terrier", "Dachshund",
        "Siberian Husky", "Boxer", "Great Dane", "Doberman Pinscher", "Shih Tzu",
        "Australian Shepherd", "Border Collie", "Chihuahua", "Pomeranian", "Maltese",
        "Cocker Spaniel", "Boston Terrier", "Havanese", "Shetland Sheepdog", "Bichon Frise",
        "Pug", "Mastiff", "Saint Bernard", "Bernese Mountain Dog", "Basset Hound",
        "Mixed Breed", "Other"
    ],
    "Cat": [
        "Persian", "Maine Coon", "British Shorthair", "Ragdoll", "Bengal",
        "Siamese", "American Shorthair", "Abyssinian", "Russian Blue", "Scottish Fold",
        "Sphynx", "Norwegian Forest Cat", "Oriental Shorthair", "Exotic Shorthair", "Birman",
        "Turkish Angora", "Himalayan", "Devon Rex", "Cornish Rex", "Manx",
        "American Curl", "Japanese Bobtail", "Tonkinese", "Burmese", "Chartreux",
        "Mixed Breed", "Other"
    ],
    "Rabbit": [
        "Holland Lop", "Mini Rex", "Netherland Dwarf", "Lionhead", "Flemish Giant",
        "Angora", "Californian", "New Zealand", "English Spot", "French Lop",
        "Mixed Breed", "Other"
    ],
    "Bird": [
        "Parrot", "Cockatiel", "Budgerigar", "Canary", "Finch",
        "Lovebird", "Conure", "Macaw", "Cockatoo", "African Grey",
        "Other"
    ],
    "Hamster": [
        "Syrian", "Dwarf Campbell", "Dwarf Winter White", "Roborovski", "Chinese",
        "Other"
    ],
    "Guinea Pig": [
        "American", "Abyssinian", "Peruvian", "Silkie", "Teddy",
        "Texel", "Other"
    ],
    "Ferret": [
        "Standard", "Angora", "Other"
    ],
    "Reptile": [
        "Bearded Dragon", "Leopard Gecko", "Ball Python", "Corn Snake", "Tortoise",
        "Iguana", "Chameleon", "Other"
    ],
    "Fish": [
        "Goldfish", "Betta", "Guppy", "Tetra", "Cichlid",
        "Other"
    ],
    "Other": [
        "Other"
    ]
}

SPECIES_LIST = sorted(SPECIES_BREEDS.keys())

def get_breeds_for_species(species: str) -> list:
    """Get list of breeds for a given species"""
    return SPECIES_BREEDS.get(species, ["Other"])

