from fastapi import APIRouter, HTTPException, Depends
from app.schemas.plan_schema import PlanCreate, PlanUpdate, PlanOut
from app.services import plan_service
from app.utils.dependencies import admin_only
from app.utils.functions import  create_response, handle_exception
router = APIRouter(tags=["Plans"])

@router.get("/")
async def get_plans():
    try:
        plans=await plan_service.get_all_plans()
        return create_response(200,True,"Plan Recieved Successfully",plans)
    except Exception as e:
        print("plan get",e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))


# @router.post("/create", response_model=PlanOut)
@router.post("/create")
async def create_plan(plan: PlanCreate, current_user=Depends(admin_only)):
    try:
        plan = await plan_service.create_plan(plan)
        return create_response(200,True,"plan created Successfully",plan)
    except Exception as e:
        print("plan post",e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))

@router.put("/{plan_id}")
async def update_plan(plan_id: str, plan: PlanUpdate, current_user=Depends(admin_only)):
    try:
        updated = await plan_service.update_plan(plan_id, plan)
        if not updated:
            raise HTTPException(status_code=404, detail="Plan not found")
        return create_response(200,True,"Plan updated",None)
    except Exception as e:
        print("plan put",e)
        raise HTTPException(status_code=500, detail=handle_exception(e, "",500))

@router.delete("/{plan_id}")
async def delete_plan(plan_id: str, current_user=Depends(admin_only)):
    try:
        deleted = await plan_service.delete_plan(plan_id)
        if not deleted:
            raise HTTPException(status_code=404,  detail=handle_exception(e,"Plan not found",404))
        return create_response(200,True, "Plan deleted", None)
    except Exception as e:
        print("plan delete",e)
        raise HTTPException(status_code=500, detail=handle_exception(e, "",500))
