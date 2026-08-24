from datetime import datetime

from db.database import SessionLocal
from core.security import hash_password
from models.user import UserModel
from models.club import ClubModel
from models.member import ClubMemberModel
from models.activity import ClubActivityModel


def seed_data():

    db = SessionLocal()

    try:

        # =====================
        # USER
        # =====================

        user1 = UserModel(
            email="admin@gmail.com",
            password_hash=hash_password("admin123"),
            full_name="Admin",
            role="ADMIN",
            is_active=True,
            created_at=datetime.now()
        )

        user2 = UserModel(
            email="user@gmail.com",
            password_hash=hash_password("user123"), 
            full_name="Nguyen Van A",
            role="USER",
            is_active=True,
            created_at=datetime.now()
        )

        db.add_all([user1, user2])
        db.flush()


        # =====================
        # CLUB
        # =====================

        club = ClubModel(
            name="Python Club",
            description="Cau lac bo Python",
            owner_id=user1.id,
            created_at=datetime.now()
        )

        db.add(club)
        db.flush()


        # =====================
        # MEMBER
        # =====================

        member1 = ClubMemberModel(
            club_id=club.id,
            user_id=user1.id,
            role="OWNER",
            joined_at=datetime.now()
        )

        member2 = ClubMemberModel(
            club_id=club.id,
            user_id=user2.id,
            role="MEMBER",
            joined_at=datetime.now()
        )

        db.add_all([member1, member2])


        # =====================
        # ACTIVITY
        # =====================

        activity = ClubActivityModel(
            club_id=club.id,
            title="Workshop Python",
            description="Workshop Python co ban",
            assignee_id=user2.id,
            status="TODO",
            priority="HIGH",
            due_date=None,
            created_at=datetime.now()
        )

        db.add(activity)

        db.commit()

        print("Seed successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()