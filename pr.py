from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


def check_token(token):
    if len(token) < 8:
        raise HTTPException(status_code=400, detail={
                "data":"token is not valid",
                "status":400
        })
    
    return token
def check_token2(token:str = Depends(check_token)):
    if "a" in token:
        return token
    else:
        raise HTTPException(status_code=400, detail={
                "data":"token is not valid dont have a",
                "status":400
        })

@app.get("/")
def test(token:str = Depends(check_token2)):
    return token
 


@app.get("/a")
def test(token:str = Depends(check_token)):

    return token + "12434"

@app.get("/b")
def test(token:str= Depends(check_token)):
    return token + "124"

# Dry - dont reapet yourself
#  Crud 

# users = [{} - 0,{} - 1,{} - 2]