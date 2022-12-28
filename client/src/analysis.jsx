import { Form } from "react-router-dom"
import styles from './analysis.module.css'

export default function Analysis(props) {
  const analysis = {
    id: props.id,
    term: props.term,
    status: props.status,
    createdAt: new Date(props.created_at),
  }

  const statusEnum = {
    "parsing": { text: "processando", color: "#fcbf49" },
    "analyzing": { text: "analisando", color: "#2a9d8f" },
    "done": { text: "concluído", color: "#003049" },
    "error": { text: "erro", color: "#d62828" }
  }

  return (
    <div className={styles.analysis}>
      <div className={styles.info}>
        <h1><b>termo: </b>{analysis.term}</h1>

        <h2>{analysis.id}</h2>

        <span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12">
            <title>status</title>
            <circle cx="6" cy="6" r="6" fill={statusEnum[analysis.status].color}></circle>
          </svg>
          <h3>{statusEnum[analysis.status].text}</h3>
        </span>

        <h3>criado em {analysis.createdAt.toLocaleDateString("pt-BR")}</h3>
      </div>

      <div className={styles.actions}>
        <Form action={`graph/${analysis.id}`}>
          <button type="submit">ver</button>
        </Form>
        <Form
          method="post"
          action="destroy"
          onSubmit={(event) => {
            if (
              !window.confirm(
                "tem certeza que deseja deletar esta análise?"
              )
            ) {
              event.preventDefault()
            }
          }}
        >
          <button type="submit">apagar</button>
        </Form>
      </div>
    </div>
  );
}