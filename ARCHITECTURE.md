# 🏗️ Application Architecture

## System Overview

The AI Diet Planner is a three-tier web application built with Python and Streamlit.

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│              (Streamlit Web Application)                 │
│  ┌────────┬────────┬────────┬────────┬────────┐        │
│  │  Home  │Profile │  Diet  │  Data  │ About  │        │
│  │  Page  │Creator │  Plan  │  View  │  Page  │        │
│  └────────┴────────┴────────┴────────┴────────┘        │
└─────────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────────┐
│               BUSINESS LOGIC LAYER                       │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │         diet_planner.py                       │      │
│  │  • BMR Calculation (Mifflin-St Jeor)         │      │
│  │  • TDEE Calculation                           │      │
│  │  • Macro Distribution                         │      │
│  │  • Meal Plan Generation                       │      │
│  │  • Dietary Restriction Filtering              │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────────┐
│                  DATA ACCESS LAYER                       │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │         database.py                           │      │
│  │  • Database Connection Management             │      │
│  │  • CRUD Operations                            │      │
│  │  • Query Methods                              │      │
│  │  • Statistics & Analytics                     │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────────┐
│                  DATABASE LAYER                          │
│                                                          │
│          SQLite Database (diet_planner.db)               │
│  ┌────────┐   ┌────────────┐   ┌────────────┐         │
│  │ users  │   │ diet_plans │   │   meals    │         │
│  └────────┘   └────────────┘   └────────────┘         │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer (app.py)

**Responsibilities:**
- Display user interface
- Handle user input
- Render visualizations
- Navigation between pages

**Key Features:**
- 5 main pages (Home, Create Profile, Generate Diet Plan, View Data, About)
- Interactive forms with validation
- Real-time data visualization with Plotly
- CSV export functionality
- Responsive design

### 2. Business Logic Layer (diet_planner.py)

**Responsibilities:**
- Calculate nutritional requirements
- Generate personalized meal plans
- Apply dietary restrictions
- Validate nutritional data

**Core Algorithms:**

```python
# BMR Calculation (Mifflin-St Jeor)
BMR_male = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
BMR_female = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161

# TDEE Calculation
TDEE = BMR × Activity_Multiplier

# Target Calories
Target = TDEE + Goal_Adjustment
```

**Activity Multipliers:**
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Very Active: 1.725
- Extreme: 1.9

**Goal Adjustments:**
- Lose Weight: -500 kcal
- Maintain: 0 kcal
- Gain Muscle: +300 kcal

### 3. Data Access Layer (database.py)

**Responsibilities:**
- Database connection management
- Execute SQL queries
- Data validation and sanitization
- Return data as Pandas DataFrames

**Key Methods:**
- `add_user()` - Create new user profile
- `add_diet_plan()` - Store diet plan
- `add_meal()` - Store meal information
- `get_all_*()` - Retrieve data as DataFrames
- `get_statistics()` - Calculate aggregates

### 4. Database Layer

**Schema Design:**

```sql
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ age                 │
│ gender              │
│ weight              │
│ height              │
│ activity_level      │
│ goal                │
│ dietary_restrictions│
│ created_at          │
└─────────────────────┘
          │
          │ 1:N
          ↓
┌─────────────────────┐
│    diet_plans       │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ target_calories     │
│ protein_grams       │
│ carbs_grams         │
│ fats_grams          │
│ plan_date           │
│ created_at          │
└─────────────────────┘
          │
          │ 1:N
          ↓
┌─────────────────────┐
│       meals         │
├─────────────────────┤
│ id (PK)             │
│ plan_id (FK)        │
│ meal_type           │
│ meal_name           │
│ ingredients         │
│ calories            │
│ protein             │
│ carbs               │
│ fats                │
└─────────────────────┘
```

## Data Flow

### Creating a Diet Plan

```
User Input (app.py)
    ↓
1. User fills profile form
    ↓
2. Submit → database.add_user()
    ↓
3. User selects profile → Generate Plan
    ↓
4. diet_planner.get_complete_nutrition_plan()
    ├─ calculate_bmr()
    ├─ calculate_tdee()
    ├─ calculate_target_calories()
    ├─ calculate_macros()
    └─ generate_meal_plan()
    ↓
5. Save to database
    ├─ database.add_diet_plan()
    └─ database.add_meal() (for each meal)
    ↓
6. Display results with visualizations
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.28.1 | Web UI framework |
| Visualization | Plotly 5.17.0 | Interactive charts |
| Data Processing | Pandas 2.1.1 | Data manipulation |
| Numerical | NumPy 1.24.3 | Mathematical operations |
| Database | SQLite | Data persistence |
| ORM | SQLAlchemy 2.0.21 | Database toolkit |

## Design Patterns

### 1. Singleton Pattern
- Database connection management
- Single instance shared across application

### 2. Repository Pattern
- `DietPlannerDB` class abstracts database operations
- Clean separation of data access logic

### 3. Factory Pattern
- Meal generation creates different meal types
- Dynamic meal selection based on criteria

### 4. Strategy Pattern
- Different calculation strategies for goals
- Pluggable macro distribution algorithms

## Security Considerations

### Current Implementation
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation
- ✅ No hardcoded credentials
- ✅ Clean separation of concerns

### Production Recommendations
- Add user authentication
- Implement role-based access control
- Use environment variables for sensitive config
- Add rate limiting
- Enable HTTPS
- Implement data encryption at rest

## Scalability

### Current Limitations
- SQLite (single-file database)
- Single-user session state
- No caching layer

### Scaling Options

**Horizontal Scaling:**
```
Load Balancer
    ↓
┌────────┬────────┬────────┐
│App 1   │App 2   │App 3   │
└────────┴────────┴────────┘
         ↓
    Cloud Database
    (PostgreSQL)
```

**Caching Layer:**
```
Application
    ↓
Redis Cache ←→ Database
```

## Performance Optimization

### Current Performance
- **Page Load**: < 1 second
- **Plan Generation**: < 500ms
- **Database Queries**: < 100ms

### Optimization Strategies
1. Use `@st.cache_resource` for database connections
2. Lazy load data in View Data page
3. Pagination for large datasets
4. Index database columns
5. Optimize SQL queries

## Testing Strategy

### Unit Tests
- Individual function testing
- Mathematical calculations validation
- Database operations

### Integration Tests
- Complete workflow testing
- Multi-component interaction
- Edge case validation

### Manual Testing
- UI/UX testing
- Cross-browser compatibility
- Mobile responsiveness

## Deployment Architecture

### Streamlit Cloud
```
GitHub Repository
    ↓
Streamlit Cloud
    ├─ Auto-deploy on push
    ├─ Managed hosting
    └─ Built-in SSL/CDN
```

### Docker Deployment
```
Dockerfile
    ↓
Docker Image
    ↓
Container Registry
    ↓
Kubernetes/Docker Swarm
```

## Monitoring & Logging

### Recommended Additions
- Application logging (Python logging module)
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- User analytics (Google Analytics)

## Future Enhancements

### Phase 2 Features
- [ ] Multi-day meal planning
- [ ] Recipe API integration
- [ ] Shopping list generation
- [ ] Exercise tracking
- [ ] Progress tracking with charts
- [ ] Mobile app version
- [ ] Social features (sharing plans)
- [ ] AI-powered recommendations
- [ ] Integration with fitness trackers
- [ ] Email notifications

### Technical Improvements
- [ ] GraphQL API
- [ ] Real-time updates with WebSockets
- [ ] Progressive Web App (PWA)
- [ ] Offline support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

## Maintenance

### Regular Tasks
- Update dependencies (monthly)
- Database backup (daily in production)
- Monitor error logs
- Review user feedback
- Performance optimization

### Version Control
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Maintain changelog
- Tag releases in Git

---

**Architecture Version**: 1.0  
**Last Updated**: November 2024  
**Author**: AI Diet Planner Team
