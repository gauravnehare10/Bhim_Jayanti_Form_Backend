from fastapi import APIRouter, HTTPException, Depends
from config.database import registrations, withdraw_registrations
from models.models import WithdrawalUpdate, User
from typing import Annotated
from schemas.admin_auth import get_current_user

router = APIRouter()

@router.get("/admin/registrations")
async def get_all_registrations(current_user: User=Depends(get_current_user)):
    try:
        registrations_data = await registrations.find().to_list(length=None)
        return registrations_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/admin/withdrawals")
async def get_all_withdrawals(current_user: User=Depends(get_current_user)):
    try:
        all_withdrawals = await withdraw_registrations.find().to_list(length=None)
        return all_withdrawals
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/admin/update_withdraw/{registration_id}")
async def withdraw_update(registration_id: str, update: WithdrawalUpdate, current_user: User=Depends(get_current_user)):
    withdrawal = await withdraw_registrations.find_one({"_id": registration_id})
    if not withdrawal:
        raise HTTPException(status_code=404, detail="Withdrawal not found")
    
    updated_withdrawal = await withdraw_registrations.update_one(
        {"_id": registration_id},
        {"$set": {"Withdraw": update.status}}
    )

    if updated_withdrawal.modified_count == 0:
        raise HTTPException(status_code=400, detail="Status update failed")

    return {"message": "Withdrawal status updated successfully", "id": registration_id}
