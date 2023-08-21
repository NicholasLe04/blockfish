import axios from "axios";
import './App.css';
import { useEffect, useState } from "react";

function App() {
  
  const [board, setBoard] = useState([]);

  useEffect(() => {
    async function fetchBoardData() {
      try {
        const response = await fetch('http://localhost:8000/get-board');  // Make sure to replace this with the actual API endpoint URL
        const data = await response.json();
        setBoard(data.board);
      } catch (error) {
        console.error('Error fetching board data:', error);
      }
    }

    fetchBoardData();
  }, []);

  console.log(board);

  return (
    <div className="App">
      <h1>Board Data</h1>
      <table className="board-container">
        {board.map((row, rowIndex) => (
          <tr className="board-row" key={rowIndex}>
            {row.map((cell, cellIndex) => (
              <td className="board-cell" key={cellIndex}>
                {cell !== ' ' && cell}
                {cell === ' ' && <>-</>}
              </td>
            ))}
          </tr>
        ))}
      </table>
    </div>
  );
}

export default App;
