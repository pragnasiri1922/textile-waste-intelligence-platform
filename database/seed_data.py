"""
Seed Database Script
Creates default admin user and loads sample data from CSV.
Run from project root: python database/seed_data.py
"""
import sys
import os
import csv

# Add project root to path so we can import backend.app
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.app.database import engine, SessionLocal, Base
from backend.app.models import User, WasteBatch

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_database():
    print("=" * 60)
    print("  Textile Waste Intelligence Platform")
    print("  Database Seeder")
    print("=" * 60)

    # Create all tables from ORM models
    Base.metadata.create_all(bind=engine)
    print("\n[OK] Database tables created successfully.")

    db = SessionLocal()

    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("[!] Admin user already exists. Skipping user creation.")
        else:
            admin = User(
                username="admin",
                email="admin@textilewaste.com",
                hashed_password=pwd_context.hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("[OK] Admin user created (username: admin, password: admin123)")

        admin_user = db.query(User).filter(User.username == "admin").first()

        # Load CSV data
        existing_count = db.query(WasteBatch).count()
        if existing_count > 0:
            print(f"[!] {existing_count} waste batches already exist. Skipping CSV import.")
        else:
            csv_path = os.path.join(project_root, "dataset", "textile_waste_samples.csv")
            if not os.path.exists(csv_path):
                print(f"[X] CSV file not found: {csv_path}")
                return

            imported = 0
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        batch = WasteBatch(
                            batch_id=row["batch_id"],
                            fabric_type=row["fabric_type"],
                            source=row["source"],
                            quantity_kg=float(row["quantity_kg"]),
                            color=row["color"],
                            condition=row["condition"],
                            waste_category=row["waste_category"],
                            recyclability_score=float(row["recyclability_score"]),
                            contamination_level=row.get("contamination_level", "None"),
                            damage_level=row.get("damage_level", "None"),
                            user_id=admin_user.id
                        )
                        db.add(batch)
                        imported += 1
                    except Exception as e:
                        print(f"  [!] Skipped row: {e}")

            db.commit()
            print(f"[OK] Successfully imported {imported} waste batch records.")

        # Create demo users
        demo_users = [
            ("operator1", "operator1@textilewaste.com", "operator123", "operator"),
            ("manager1", "manager1@textilewaste.com", "manager123", "manager"),
            ("manufacturer1", "manufacturer1@textilewaste.com", "mfg123", "manufacturer"),
        ]
        for username, email, password, role in demo_users:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                user = User(
                    username=username,
                    email=email,
                    hashed_password=pwd_context.hash(password),
                    role=role,
                    is_active=True
                )
                db.add(user)
                print(f"[OK] Demo user created: {username} ({role})")
        db.commit()

    except Exception as e:
        print(f"[X] Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

    print("\n" + "=" * 60)
    print("  Seeding Complete!")
    print("  Default Login: admin / admin123")
    print("=" * 60)


if __name__ == "__main__":
    seed_database()
