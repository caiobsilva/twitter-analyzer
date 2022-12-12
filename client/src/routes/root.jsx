import React, { useState, useEffect } from "react";
import Analysis from "../analysis";
import styles from "./root.module.css"

export default function Root() {
  const [analyses, setAnalyses] = useState([])
  const [analysisQuery, setAnalysisQuery] = useState("")

  useEffect(() => {
    fetch("http://localhost:5000/api/status")
      .then((response) => { return response.json() })
      .then((results) => setAnalyses(results) )
  }, [])

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch(`http://localhost:5000/api/analysis?query=${analysisQuery}`, { method: "POST" })
      .then((response) => { return response.json() })

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
