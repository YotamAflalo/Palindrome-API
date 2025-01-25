# Palindrome Length Finder

## Project Overview
A FastAPI-based web service that calculates the length of the longest palindromic substring using two different algorithms.

## Algorithms
1. **Expand Around Center (v2)**: 
   - Time Complexity: O(n²)
   - space complexity: o(1)
   - Explores all possible center points
   - Expands outwards to find palindromes

2. **Manacher's Algorithm (v3)**: 
   - Time Complexity: O(n)
   - space complexity: o(n)
   - Reduces redundant comparisons
   - for deeper explanation see https://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/ 

## API Endpoints
- `/string` (POST)
  - Accepts JSON with a 'string' parameter
  - Returns longest palindrome lengths using the method specify in the config file

## Authentication
- Requires HTTP headers:
  - `username`
  - `password`

### Authentication Methods

#### 1. Environment File (.env)
- Create `.env` file:
```
USERNAME=your_username
PASSWORD=your_password
```
- Set in `config.py`: `credential_type = 'env'`

#### 2. Docker Environment Variables
```bash
docker run -p 8000:8000 \
  -e USERNAME=your_username \
  -e PASSWORD=your_password \
  palindrom-api
```
- Set in `config.py`: `credential_type = 'docker_env'`

#### 3. Docker Swarm Secrets
1. Initialize Swarm:
```bash
docker swarm init
```

2. Create Secrets:
```bash
echo "your_username" | docker secret create username -
echo "your_password" | docker secret create password -
```

3. Run Container:
```bash
docker run -p 8000:8000 \
  --secret username \
  --secret password \
  palindrom-api
```
- Set in `config.py`: `credential_type = 'docker_swarm'`

### Configuration
- Modify `config.py` to choose credential method:
  ```python
  credential_type = 'env'  # Options: 'env', 'docker_secrets', 'docker_swarm'
  ```
## Setup
1. Install dependencies
2. Configure `config.py` with `maximise_time` (True for minimising runnig time, False for minimising space used) and `credential_type`
3. create credential an expleined above..
3. Run with FastAPI server:
- ...
- ....
4. [optional] run the docker file as explained above

## Requirements
- Python 3.8+
- fastapi==0.110.3
- uvicorn==0.23.2
- python-dotenv==1.0.0
- pytest==7.4.0
- httpx==0.26.0
- regex==2024.9.11

## Testing
- Unit tests [TODO - add explanation]

