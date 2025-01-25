from fastapi import FastAPI, Request,HTTPException,Header,Depends
from fastapi.responses import JSONResponse
from pathlib import Path
import os
import sys
import time

project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)
from config.config import maximise_time,credentials_type
from src.palindrom import pal_length_v2,pal_length_manachers,clean_string
from logger import logger
import dotenv
if credentials_type =='env':
    dotenv.load_dotenv(os.path.join(project_root, '.env'))
if credentials_type =='docker_env':
    dotenv.load_dotenv()

app = FastAPI()

def get_docker_credentials():
    """
    Retrieve credentials based on configuration.
    
    Returns:
    - tuple: (username, password)
    """
    try:
        with open('/run/secrets/username', 'r') as f:
                username = f.read().strip()
        with open('/run/secrets/password', 'r') as f:
                password = f.read().strip()
        logger.info("Docker secrets loaded")
        return username, password
    except FileNotFoundError:
        logger.eror("Docker secrets not found")
        return None, None
def check_pass_name(username:str,password:str):
    """
    Validate user credentials against predefined credentials.

    inputs:
    - username (str): Provided username
    - password (str): Provided password
    
    Returns:
    - bool: True if credentials match, False otherwise
    """
    logger.info("Validate user credentials")
    if credentials_type =='env' or 'docker_env':
        if username==os.getenv('USERNAME') and password==os.getenv('PASSWORD'):
            logger.info("user credentials are currect")
            return True
    if credentials_type =='docker_sworm':
        secret_username,secret_password =get_docker_credentials() #מתלבט אם נכון להכניס הודעת שגיאה אחרת אם אין סיסמא בשרת
        if username==secret_username and password==secret_password:
            logger.info("user credentials are currect")
            return True
    logger.info("user credentials are wrong")
    return False
    
@app.middleware("http")    
async def authenticator(request: Request, call_next):
    """
    Middleware to authenticate incoming requests.
    Checks for valid username and password in request headers.
    return 401 if credentials are missing or incorrect. else - activate palindrom_length.
    
    """
    username = request.headers.get('username')
    password = request.headers.get('password')

    if (not username) or (not password) or not check_pass_name(username, password):
        return JSONResponse(
            status_code=401, 
            content={"detail": "wrong credentials"}
        )
    
    response = await call_next(request)
    return response

@app.post("/string")
async def palindrom_length(request: Request,maximise_time = maximise_time):
    """
    Calculate max palindrome lengths in a substring.
    Expects JSON input with a 'string' key.
     Returns lengths of longest palindromic substrings.

     inputs:
     - request (Request): Incoming HTTP request with JSON body
     - maximise_time: Does the user want to minimize runtime (True) or memory usage (False)
    """
    try:
        body = await request.json()
        s = body.get('string', None)
        if not isinstance(s, str):
            raise HTTPException(status_code=400, detail='"string" must be a  string')
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid JSON')  
    start_time = time.time()  
    string = clean_string(s)
    if maximise_time:
        answer = pal_length_manachers(string=string)
    else:
        answer = pal_length_v2(string=string)
    func_processing_time = time.time() - start_time
    logger.info(f'the function process {s} in {func_processing_time:.5f}')
    return {'answer ':answer}
    

@app.get("/")
def read_root():
    """
    a get request 
    return: instructions on how to use this API """
    return {"instructions": 
            """Please provide a JSON file in the following format: 

            {

                "string": str - string with only alphabetic characters

            }
            
            and enter username and password as an header
            """}


#TODO לארוז יפה
#TODO דוק+מקרה קצה בכל אחד מהשלבים
#TODO לשים לוגים להכל
#TODO לארוז בדוקר
#TODO CICD?