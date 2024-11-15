# Design Patterns & Principles Used:
# Creational Patterns
1. Factory Method Pattern
- Located in supplier implementations (AcmeSupplier, PatagoniaSupplier, PaperfliesSupplier)
- Each supplier creates hotel objects in their own format
2. Dependency Injection
- In HotelService constructor: 
```def __init__(self, repository: IHotelRepository, suppliers: List[ISupplier], merge_strategy: IMergeStrategy)```

# Structural Patterns
1. Repository Pattern
- InMemoryHotelRepository implements IHotelRepository
- Centralizes data access logic
2. Adapter Pattern
- Supplier classes adapt different data formats to common Hotel model
- Example in parse_hotel() methods of each supplier

# Behavioral Patterns
1. Strategy Pattern
- DefaultMergeStrategy implements IMergeStrategy
- Encapsulates merging algorithm
- Located in merge_strategy.py

# SOLID Principles
1. Single Responsibility (S)
- Each supplier handles only its data format
- MergeStrategy focuses only on merging logic
- Repository handles only data storage
2. Open/Closed (O)
- New suppliers can be added without modifying existing code
- Base supplier class is extended, not modified
3. Liskov Substitution (L)
- All suppliers can be used interchangeably through ISupplier interface
- All merge strategies can be swapped through IMergeStrategy
4. Interface Segregation (I)
- Clean interfaces defined in interfaces.py
- ISupplier, IHotelRepository, IMergeStrategy
5. Dependency Inversion (D)
- High-level modules depend on abstractions
- HotelService depends on interfaces, not concrete classes


# Project Structure:
```
src/
├── domain/
│   ├── models.py
│   └── interfaces.py
├── infrastructure/
│   ├── suppliers/
│   │   ├── base.py
│   │   ├── acme.py
│   │   ├── patagonia.py
│   │   └── paperflies.py
│   └── repositories.py
├── application/
│   ├── hotel_service.py
│   └── merge_strategy.py
└── main.py
```