from .search_filter.student_filter import StudentFilter
from .search_filter.teacher_filter import TeacherCardFilter



import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional


from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_filter import FilterDepends

from fastapi_pagination import  add_pagination,Page,paginate
from fastapi_pagination.utils import disable_installed_extensions_check
disable_installed_extensions_check()




app = APIRouter(tags=["search_system"], prefix="/search")




# #  Students

# @app.get("/students") 
# async def get_students(me = Depends(get_current_active_user),user_filter: Optional[StudentFilter] = FilterDepends(StudentFilter),session:AsyncSession = Depends(get_session)) -> Page[ShowUser]:
#     query = user_filter.filter(select(User).where(User.role == Role.student))   # 
#     result = await session.execute(query)
#     return paginate(result.scalars().all())


# @app.get("/student", response_model=ShowUser)
# async def get_student(user_id:uuid.UUID,me = Depends(get_current_active_user),session:AsyncSession = Depends(get_session)):
#     user = await session.scalar(select(User).where(User.id == user_id, User.role == Role.student))
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail={"status_code":404, "user":"student not found"})


# #  Teachers


# @app.get("/teacher", response_model=ShowOptionalTeacher)
# async def get_teacher(user_id:uuid.UUID,me = Depends(get_current_active_user),session:AsyncSession = Depends(get_session)):
#     user = await session.scalar(select(User)
#                                 .options(selectinload(User.teacher_card).joinedload(TeacherCard.subjects))
#                                 .where(User.id == user_id, User.role == Role.teacher))
#     if user:
#         return user
#     raise HTTPException(status_code=404, detail={"status_code":404, "user":"student not found"})


# @app.get("/subjects", response_model=list[ShowSubjects])
# async def get_subjects(me = Depends(get_current_active_user),session:AsyncSession = Depends(get_session)):
    
#     subjects = await session.scalars(select(Subjects))
#     return subjects.all()


# @app.get("/teachers") 
# async def get_teachers(id_subject:int | None = None,
#                        me = Depends(get_current_active_user),
#                        teacher_card_filter:Optional[TeacherCardFilter] = FilterDepends(TeacherCardFilter)
#                        ,user_filter: Optional[StudentFilter] = FilterDepends(StudentFilter)
#                        ,session:AsyncSession = Depends(get_session)) -> Page[ShowOptionalTeacher]:
    
  
#     query1 = teacher_card_filter.filter(select(TeacherCard).options(selectinload(TeacherCard.subject)))
#     result1 = await session.execute(query1)
        

#     ids = [teacher_card.id for teacher_card in result1.scalars().all()]
    
#     if id_subject:
#         subject = await session.scalar(select(Subjects).where(Subjects.id == id_subject))
#         if subject:

#             query = user_filter.filter(select(User)
#                 .options(selectinload(User.teacher_cards).joinedload(TeacherCard.subject))
#                 .where(User.role == Role.teacher, TeacherCard.id.in_(ids), TeacherCard.subject_id ==  subject.id ))
#             result = await session.execute(query)
#             return paginate(result.scalars().all())
#         else:
#             raise HTTPException(status_code=404, detail="Subject not found")
        
#     query = user_filter.filter(select(User)
#         .options(selectinload(User.teacher_cards).joinedload(TeacherCard.subject))
#         .where(User.role == Role.teacher, TeacherCard.id.in_(ids)))
           
#     result = await session.execute(query)
#     return paginate(result.scalars().all())

# # users


# @app.delete("/delete/users")
# async def delete_user(ids: list[uuid.UUID],me = Depends(get_current_active_user), session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(User).options(selectinload(User.teacher_cards)).where(User.id.in_(ids)))
#     users = result.scalars().all()

#     if not users:
#         raise HTTPException(status_code=404, detail="Users not found")
    
#     for user in users:
#         await session.delete(user)
#     await session.commit()

#     return {"message": "Users deleted"}


# # @app.put("/update/users")
# # async def update_user(data:UpdateUser,id_user:uuid.UUID,me = Depends(get_current_active_user), session:AsyncSession = Depends(get_session)):
# #     user = await session.scalar(select(User).where(User.id == id_user))
# #     for field, value in data.model_dump().items():
# #         setattr(user, field, value)
    
    
# #     await session.commit()
# #     return {"message":"user updated"}


# # app.put("/update/teacher_card")
# # async def update_teacher_card(data:CreateTeacherCard,id_teacher_card:int, session:AsyncSession = Depends(get_session)):
# #     teacher_card = await session.scalar(select(TeacherCard).where(TeacherCard.id == id_teacher_card))
# #     for field, value in data.model_dump().items():
# #         setattr(teacher_card, field, value)
# #     await session.commit()
# #     return {"message":"teacher card updated"}




# add_pagination(app)  




