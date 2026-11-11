from app.db.session import SessionLocal
from app.models import Case


db = SessionLocal()

try:
    test_case = Case(
        title="Database connection test",
        description="Testing incident case insertion and retrieval.",
        status="submitted",
    )

    db.add(test_case)
    db.commit()
    db.refresh(test_case)

    print("Case inserted successfully!")
    print("Case ID:", test_case.id)

    retrieved_case = db.get(Case, test_case.id)

    print("Case retrieved successfully!")
    print("Title:", retrieved_case.title)
    print("Status:", retrieved_case.status)

finally:
    db.close()
