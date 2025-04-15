from fastapi import APIRouter, Depends, HTTPException
from app.schemas.image_data_schema import ImageDataCreate, ImageDataUpdate
from app.services.image_data_service import get_image_generated
from app.utils.dependencies import get_current_user
from app.utils.functions import create_response, handle_exception
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
        return create_response(200,True,"",await get_image_generated(procedure_id))
    except Exception as e:
        print("image data get", e)
        raise HTTPException(status_code=404, detail=handle_exception(e, ""))

