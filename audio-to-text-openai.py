from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import sounddevice as sd
import numpy as np
import wave
from openai import OpenAI
import psycopg2
import os
import uvicorn

app = FastAPI()

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    
    filename = file.filename
    client = OpenAI()

    audio_file= open(filename, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    # Transcribe audio
    client = OpenAI()
    audio_file = open(filename, "rb")
    transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    print(transcription.text)

    # Remove the uploaded file
    if os.path.exists(filename):
        os.remove(filename)

    prompt = f'''
    You are a helpful assistant specialising in PostGRE SQL database.
    Answer the questions by providing only the SQL statement that is compatible with the PostGRE database.
    The response should contain only the generated SQL statement.
    This is the question you are required to answer: 
    {transcription.text}

    Here is the relevant context of the database:
    CREATE TABLE Accounts (
        AccountName        varchar(40),
        AccountNumber      char(8) primary key,
        AccountValue       DECIMAL(10, 2),
        LastRebalanceDate   date,
        DaysSinceLastRebalance        integer,
        TotalSecurityDriftValue         DECIMAL(10, 2),
        AccountClass        varchar(20),
        Username                char(4)
    );
    '''

    completion = client.chat.completions.create(
        model="gpt-4o",

        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message.content)

    sql = completion.choices[0].message.content
    print(sql)
    iIndex = sql.find("SELECT")
    end = sql.find(";")
    if iIndex != -1 and end != -1:
        sql = sql[iIndex:end]
    else:
        sql = 'SELECT 1'

    DB_PARAMS = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": "5432"
    }

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(sql)
        
    rows = cur.fetchall()
    output = "\n\n".join([f"Result: {row[0]}" for row in rows])

    return JSONResponse(content={"transcription": transcription.text, "sql": sql, "output": output})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

    