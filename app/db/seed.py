from datetime import datetime, timedelta

from db.database import SessionLocal
from core.security import hash_password

from models.user import UserModel
from models.club import ClubModel
from models.member import ClubMemberModel
from models.activity import ClubActivityModel


def seed_data():
    db = SessionLocal()

    try:
        now = datetime.now()

        # =========================================================
        # USERS
        # Chỉ user1 là ADMIN
        # =========================================================

        user1 = UserModel(
            email="user1@gmail.com",
            password_hash=hash_password("user1--1"),
            full_name="User One",
            role="ADMIN",
            is_active=True,
            created_at=now
        )

        user2 = UserModel(
            email="user2@gmail.com",
            password_hash=hash_password("user2--2"),
            full_name="User Two",
            role="USER",
            is_active=True,
            created_at=now
        )

        user3 = UserModel(
            email="user3@gmail.com",
            password_hash=hash_password("user3--3"),
            full_name="User Three",
            role="USER",
            is_active=True,
            created_at=now
        )

        user4 = UserModel(
            email="user4@gmail.com",
            password_hash=hash_password("user4--4"),
            full_name="User Four",
            role="USER",
            is_active=True,
            created_at=now
        )

        user5 = UserModel(
            email="user5@gmail.com",
            password_hash=hash_password("user5--5"),
            full_name="User Five",
            role="USER",
            is_active=True,
            created_at=now
        )

        user6 = UserModel(
            email="user6@gmail.com",
            password_hash=hash_password("user6--6"),
            full_name="User Six",
            role="USER",
            is_active=True,
            created_at=now
        )

        users = [user1, user2, user3, user4, user5, user6]

        db.add_all(users)
        db.flush()

        # =========================================================
        # CLUBS
        # =========================================================

        club1 = ClubModel(
            name="Python Club",
            description="Cau lac bo Python",
            owner_id=user1.id,
            created_at=now
        )

        club2 = ClubModel(
            name="Ballet Club",
            description="Cau lac bo Ballet",
            owner_id=user2.id,
            created_at=now
        )

        club3 = ClubModel(
            name="Music Club",
            description="Cau lac bo am nhac",
            owner_id=user3.id,
            created_at=now
        )

        club4 = ClubModel(
            name="Technology Club",
            description="Cau lac bo cong nghe",
            owner_id=user4.id,
            created_at=now
        )

        clubs = [club1, club2, club3, club4]

        db.add_all(clubs)
        db.flush()

        # =========================================================
        # CLUB MEMBERS
        # =========================================================

        members = [

            # ---------- CLUB 1 ----------
            ClubMemberModel(
                club_id=club1.id,
                user_id=user1.id,
                role="OWNER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club1.id,
                user_id=user2.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club1.id,
                user_id=user3.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club1.id,
                user_id=user4.id,
                role="MEMBER",
                joined_at=now
            ),

            # ---------- CLUB 2 ----------
            ClubMemberModel(
                club_id=club2.id,
                user_id=user2.id,
                role="OWNER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club2.id,
                user_id=user3.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club2.id,
                user_id=user4.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club2.id,
                user_id=user5.id,
                role="MEMBER",
                joined_at=now
            ),

            # ---------- CLUB 3 ----------
            ClubMemberModel(
                club_id=club3.id,
                user_id=user3.id,
                role="OWNER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club3.id,
                user_id=user2.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club3.id,
                user_id=user5.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club3.id,
                user_id=user6.id,
                role="MEMBER",
                joined_at=now
            ),

            # ---------- CLUB 4 ----------
            ClubMemberModel(
                club_id=club4.id,
                user_id=user4.id,
                role="OWNER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club4.id,
                user_id=user2.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club4.id,
                user_id=user3.id,
                role="MEMBER",
                joined_at=now
            ),

            ClubMemberModel(
                club_id=club4.id,
                user_id=user6.id,
                role="MEMBER",
                joined_at=now
            ),
        ]

        db.add_all(members)
        db.flush()

        # =========================================================
        # ACTIVITIES
        # =========================================================

        activities = [

            # ================= CLUB 1 =================

            ClubActivityModel(
                club_id=club1.id,
                title="Python Workshop",
                description="Workshop Python co ban",
                created_by=user1.id,
                assignee_id=user2.id,
                status="TODO",
                priority="HIGH",
                due_date=now + timedelta(days=3),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club1.id,
                title="Prepare Python Slides",
                description="Chuan bi slide workshop",
                created_by=user2.id,
                assignee_id=user3.id,
                status="IN_PROGRESS",
                priority="MEDIUM",
                due_date=now + timedelta(days=5),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club1.id,
                title="Review Python Exercises",
                description="Kiem tra bai tap",
                created_by=user3.id,
                assignee_id=user4.id,
                status="DONE",
                priority="LOW",
                due_date=now - timedelta(days=1),
                created_at=now - timedelta(days=2)
            ),

            ClubActivityModel(
                club_id=club1.id,
                title="Club Meeting",
                description="Hop thanh vien",
                created_by=user4.id,
                assignee_id=None,
                status="TODO",
                priority="MEDIUM",
                due_date=now + timedelta(days=7),
                created_at=now
            ),

            # ================= CLUB 2 =================

            ClubActivityModel(
                club_id=club2.id,
                title="Ballet Practice",
                description="Luyen tap bai mua",
                created_by=user2.id,
                assignee_id=user3.id,
                status="IN_PROGRESS",
                priority="HIGH",
                due_date=now + timedelta(days=2),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club2.id,
                title="Prepare Costume",
                description="Chuan bi trang phuc",
                created_by=user3.id,
                assignee_id=user4.id,
                status="TODO",
                priority="MEDIUM",
                due_date=now + timedelta(days=6),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club2.id,
                title="Stage Rehearsal",
                description="Tong duyet san khau",
                created_by=user4.id,
                assignee_id=user5.id,
                status="DONE",
                priority="HIGH",
                due_date=now - timedelta(days=1),
                created_at=now - timedelta(days=3)
            ),

            ClubActivityModel(
                club_id=club2.id,
                title="Ballet Club Meeting",
                description="Hop ban chu nhiem",
                created_by=user2.id,
                assignee_id=None,
                status="TODO",
                priority="LOW",
                due_date=None,
                created_at=now
            ),

            # ================= CLUB 3 =================

            ClubActivityModel(
                club_id=club3.id,
                title="Music Rehearsal",
                description="Tap nhac cho su kien",
                created_by=user3.id,
                assignee_id=user2.id,
                status="IN_PROGRESS",
                priority="HIGH",
                due_date=now + timedelta(days=1),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club3.id,
                title="Choose Songs",
                description="Lua chon bai hat",
                created_by=user2.id,
                assignee_id=user5.id,
                status="DONE",
                priority="LOW",
                due_date=now - timedelta(days=2),
                created_at=now - timedelta(days=4)
            ),

            ClubActivityModel(
                club_id=club3.id,
                title="Sound Check",
                description="Kiem tra am thanh",
                created_by=user5.id,
                assignee_id=user6.id,
                status="TODO",
                priority="HIGH",
                due_date=now + timedelta(days=4),
                created_at=now
            ),

            # ================= CLUB 4 =================

            ClubActivityModel(
                club_id=club4.id,
                title="API Workshop",
                description="Workshop FastAPI",
                created_by=user4.id,
                assignee_id=user2.id,
                status="TODO",
                priority="HIGH",
                due_date=now + timedelta(days=4),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club4.id,
                title="Database Design",
                description="Thiet ke database",
                created_by=user2.id,
                assignee_id=user3.id,
                status="IN_PROGRESS",
                priority="HIGH",
                due_date=now + timedelta(days=8),
                created_at=now
            ),

            ClubActivityModel(
                club_id=club4.id,
                title="Code Review",
                description="Review code project",
                created_by=user3.id,
                assignee_id=user6.id,
                status="DONE",
                priority="MEDIUM",
                due_date=now - timedelta(days=2),
                created_at=now - timedelta(days=5)
            ),

            ClubActivityModel(
                club_id=club4.id,
                title="Technology Club Meeting",
                description="Hop dinh ky",
                created_by=user4.id,
                assignee_id=None,
                status="TODO",
                priority="LOW",
                due_date=None,
                created_at=now
            ),
        ]

        db.add_all(activities)

        db.commit()

        print("========================================")
        print("SEED SUCCESSFULLY!")
        print("========================================")
        print("USER:")
        print("user1@gmail.com / user1--1 -> ADMIN")
        print("user2@gmail.com / user2--2 -> USER")
        print("user3@gmail.com / user3--3 -> USER")
        print("user4@gmail.com / user4--4 -> USER")
        print("user5@gmail.com / user5--5 -> USER")
        print("user6@gmail.com / user6--6 -> USER")
        print("----------------------------------------")
        print("CLUB:")
        print("Python Club      -> owner user1")
        print("Ballet Club      -> owner user2")
        print("Music Club       -> owner user3")
        print("Technology Club -> owner user4")
        print("----------------------------------------")
        print("ACTIVITIES: 15")
        print("========================================")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()