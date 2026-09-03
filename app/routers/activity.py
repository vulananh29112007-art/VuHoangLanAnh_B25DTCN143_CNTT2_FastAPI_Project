from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth import get_current_user

from models.user import UserModel
from schemas.activity_schema import (
    ActivityCreate,
    ActivityResponse,
    ActivityUpdate,
    ActivityListResponse
)
from services.activity import (
    create_activity_service,
    get_activities_service,
    get_activity_service,
    update_activity_service,
    delete_activity_service,
    search_filter_activities_service,
    paginate_sort_activities_service
)


router = APIRouter(
    prefix="/clubs",
    tags=["Club Activities"]
)


@router.post("/{club_id}/activities")
def create_activity(
    club_id: int,
    data: ActivityCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_activity_service(
        db=db,
        club_id=club_id,
        data=data,
        current_user=current_user
    )


@router.get(
    "/{club_id}/activities",
    response_model=ActivityListResponse
)
def get_activities(
    club_id: int,

    status: str | None = Query(
        default=None,
        pattern="^(TODO|IN_PROGRESS|DONE)$"
    ),

    priority: str | None = Query(
        default=None,
        pattern="^(LOW|MEDIUM|HIGH)$"
    ),

    assignee_id: int | None = Query(
        default=None,
        ge=1
    ),

    search: str | None = Query(
        default=None
    ),

    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),

    offset: int = Query(
        default=0,
        ge=0
    ),

    sort_by: str = Query(
        default="created_at",
        pattern="^(created_at|due_date)$"
    ),

    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),

    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = search_filter_activities_service(
        db=db,
        club_id=club_id,
        current_user=current_user,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        search=search
    )

    return paginate_sort_activities_service(
        query=query,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )


@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_activity_service(
        db=db,
        activity_id=activity_id,
        current_user=current_user
    )


@router.patch("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    data: ActivityUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_activity_service(
        db=db,
        activity_id=activity_id,
        data=data,
        current_user=current_user
    )

@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_activity_service(
        db=db,
        activity_id=activity_id,
        current_user=current_user
    )