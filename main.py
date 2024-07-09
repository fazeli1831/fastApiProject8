from fastapi import FastAPI, BackgroundTasks
from random import randrange
from threading import Barrier, Thread
from time import ctime, sleep
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Set up the race parameters
num_runners = 3
finish_line = Barrier(num_runners)
runners = ['Huey', 'Dewey', 'Louie']
race_results = []

# Define the runner function
def runner(name: str):
    sleep(randrange(2, 6))
    result = f'Runner {name} reached the barrier at: {ctime()}'
    print(result)  # Print to console for debugging
    race_results.append(result)
    finish_line.wait()

# Define the function to start the race
def start_race():
    global race_results, runners, finish_line
    race_results = []
    finish_line = Barrier(num_runners)
    threads = []
    names = runners.copy()
    print('START RACE!!!!')
    for name in names:
        thread = Thread(target=runner, args=(name,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print('Race over')

# Define the API endpoint to start the race
@app.get("/start_race")
async def api_start_race(background_tasks: BackgroundTasks):
    global runners
    if not runners:
        runners = ['Huey', 'Dewey', 'Louie']
    background_tasks.add_task(start_race)
    return {"message": "Race started! Check /race_results for the results."}

# Define the API endpoint to get race results
@app.get("/race_results")
def api_race_results() -> List[str]:
    return race_results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
