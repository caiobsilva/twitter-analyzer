import React, { useState, useEffect, useCallback } from "react";
import styles from "./query.module.css"

export default function Query(props) {
  const [analysisQuery, setAnalysisQuery] = useState("")
  const [startTime, setStartTime] = useState("")

  useEffect(() => {
    setStartTime(minStartTime())
  }, [])

  const minStartTime = useCallback(() => {
    const date = new Date()
    const futureDate = date.getDate() - 6
    date.setDate(futureDate)

    return date.toLocaleDateString('en-CA');
  }, [])

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch(`http://localhost:5000/api/analysis?query=${analysisQuery}&start_time=${startTime}`, { method: "POST" })
      .then((response) => { return response.json() })

    props.onQuerySubmit()
    setAnalysisQuery("")
  }

  return (
    <div className={styles.query}>
      <form method="post" onSubmit={(event) => handleSubmit(event)}>
        <input
          type="date"
          className={styles.dateSelector}
          defaultValue={startTime}
          min={minStartTime()}
          onChange={(event) => setStartTime(event.target.value)}
        />
        <input
          className={styles.queryInput}
          placeholder="Nova consulta"
          onChange={(event) => setAnalysisQuery(event.target.value)}
        />
        <button type="submit">+</button>
      </form>
    </div>
  )
}