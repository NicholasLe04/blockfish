import math

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from engine.chess import Position
from engine.blockfish import minimax

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

board = Position()

@app.get("/reset-board")
async def reset():
    global board
    board = Position()

@app.get("/get-move")
async def get_move():
    return {"message": minimax(board, 3, -math.inf, math.inf, True)}

@app.get("/get-board")
async def get_board():
    board_list = board.bitboards_to_list()
    return JSONResponse({ "board": [
                        board_list[0:8],
                        board_list[8:16],
                        board_list[16:24],
                        board_list[24:32],
                        board_list[32:40],
                        board_list[40:48],
                        board_list[48:56],
                        board_list[56:64],
                    ] })

if __name__ == "__main__":
    uvicorn.run(app)