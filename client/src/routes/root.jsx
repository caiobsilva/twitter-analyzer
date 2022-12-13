import React, { useState, useEffect, useCallback } from "react";
import Analysis from "../analysis";
import styles from "./root.module.css"

export default function Root() {
  const [analyses, setAnalyses] = useState([])
  const [analysisQuery, setAnalysisQuery] = useState("")

  const updateState = useCallback(async () => {
    const response = await fetch('http://localhost:5000/api/status');
    const data = await response.json();
    setAnalyses(data)
  }, []);

  useEffect(() => {
    setInterval(updateState, 5000);
  }, [updateState])

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch(`http://localhost:5000/api/analysis?query=${analysisQuery}&start_time=2022-12-12`, { method: "POST" })
      .then((response) => { return response.json() })

    updateState()
    setAnalysisQuery("")
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Análise de tweets</h1>
      </div>

      <div className={styles.query}>
        <h2>{analyses.length} consultas</h2>

        <form method="post" onSubmit={(event) => handleSubmit(event)}>
          <input 
            placeholder="Nova consulta"
            onChange={(event) => setAnalysisQuery(event.target.value)}
          />
          <button type="submit">+</button>
        </form>
      </div>

      <div className={styles.detail}>
        { analyses.map(analysis => <div><Analysis {...analysis}/></div>) }
      </div>
    </div>
  );
}
