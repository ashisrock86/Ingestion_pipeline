from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Example: just return file info (you can save it instead)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(contents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))