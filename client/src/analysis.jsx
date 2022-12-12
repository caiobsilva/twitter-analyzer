import { Form } from "react-router-dom";
import styles from './analysis.module.css';


export default function Analysis(props) {
  const analysis = {
    id: props.id,
    term: props.term,
    status: props.status,
  };

  return (
    <div className={styles.analysis}>
      <div>
        <h1><b>termo: </b>{analysis.term}</h1>
        <h2>{analysis.id}</h2>
      </div>

      <div>
        <h3>{analysis.status}</h3>
      </div>

      <div>
        <Form action="graph/1">
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
              event.preventDefault();
            }
          }}
        >
          <button type="submit">apagar</button>
        </Form>
      </div>
    </div>
  );
}