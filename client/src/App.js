import './App.css';
import React, { useState, useEffect} from 'react'
function App() {

  const [ data, setData ]= useState("");

  useEffect(() => {
      fetch("http://localhost:5000/members").then(
        res => res.json()
      ).then(
        data => {
          setData(data)
          console.log(data)
        }
      )
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
