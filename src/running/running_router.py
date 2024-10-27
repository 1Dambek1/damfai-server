from fastapi import APIRouter, Depends, HTTPException


app = APIRouter(prefix="/running", tags=["running"])