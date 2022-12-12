import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div id="error-page">
      <h1>oops!</h1>
      <p>ocorreu um erro.</p>
      <p>
        <i>{(error.statusText || error.message).toLowerCase()}</i>
      </p>
    </div>
  );
}