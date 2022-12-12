import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
  Route,
} from "react-router-dom";
import './index.css';
import Root from "./routes/root";
import ErrorPage from "./error-page";
import Analysis from './analysis';
import Graph from "./routes/graph.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "analysis/:analysisId",
        element: <Analysis />,
      },
    ],
  },
  {
    path: "graph/:graphId",
    element: <Graph />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <RouterProvider router={router} />
);