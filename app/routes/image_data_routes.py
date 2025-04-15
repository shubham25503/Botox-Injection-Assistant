from fastapi import APIRouter, Depends, HTTPException
from app.schemas.image_data_schema import ImageDataCreate, ImageDataUpdate
from app.services.image_data_service import create_image_data, update_image_data, get_image_data
from app.utils.dependencies import get_current_user

router = APIRouter(tags=["Image Data Management"])

# @router.post("/upload/{procedure_id}", dependencies=[Depends(get_current_user)])
# async def upload_image_data(procedure_id: str, data: ImageDataCreate, user=Depends(get_current_user)):
#     try:
#         return {"id": await create_image_data(procedure_id, user, data)}
#     except Exception as e:
#         print("image data post", e)
#         raise HTTPException(status_code=500, detail=str(e))

# @router.put("/{procedure_id}", dependencies=[Depends(get_current_user)])
# async def edit_image_data(procedure_id: str, data: ImageDataUpdate):
#     try:
#         await update_image_data(procedure_id, data)
#         return {"message": "Updated successfully"}
#     except Exception as e:
#         print("image data put", e)
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/{procedure_id}", dependencies=[Depends(get_current_user)])
async def get_image_data_route(procedure_id: str):
    try:
        return await get_image_data(procedure_id)
    except Exception as e:
        print("image data get", e)
        raise HTTPException(status_code=404, detail=str(e))
