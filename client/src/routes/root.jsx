import React, { useState, useEffect, useCallback } from "react";
import Query from "../query";
import Analyses from "../analyses";
import styles from "./root.module.css"

export default function Root() {
  const [analyses, setAnalyses] = useState([])
  const [connectionFailure, setConnectionFailure] = useState(false)

  const updateState = useCallback(async () => {
    fetch("http://localhost:5000/api/status")
      .then((response) => { return response.json() })
      .then((data) => { setAnalyses(data) })
      .then(() => { setConnectionFailure(false) })
      .catch(() => { setConnectionFailure(true) })
  }, []);

  useEffect(() => { updateState() }, [])

  useEffect(() => {
    setInterval(updateState, 5000);
  }, [updateState])

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Análise de tweets</h1>
      </div>

      <div className={styles.subheader}>
        <div>
          <h2>{analyses.length} consultas</h2>
        </div>

        <Query onQuerySubmit={() => updateState()} />
      </div>

      <div className={styles.analysesDisplay}>
        <Analyses connectionFailure={connectionFailure} analyses={analyses} />
      </div>
    </div>
  );
}
