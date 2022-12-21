import React from "react";
import Analysis from "./analysis";
import styles from "./analyses.module.css";

export default function Analyses(props) {
  if (props.connectionFailure) {
    return <div className={styles.analysesError}><h2>erro de conexão :/</h2></div>
  }

  return (
    <div className={styles.analyses}>
      {props.analyses.map(analysis => <Analysis {...analysis} />)}
    </div>
  )
}