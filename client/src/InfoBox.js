import React, { useState, useEffect } from "react";

export default function InfoBox(props) {
  const [name, setName] = useState("")
  const [username, setUsername] = useState("")
  const [connections, setConnections] = useState("")
  const [createdAt, setCreatedAt] = useState(new Date())

  useEffect(() => {
    setName(props.name)
    setUsername(props.username)
    setConnections(props.connections)
    setCreatedAt(new Date(props.createdAt))
  }, [props])


  return (
    <div className="info-box" style={
      { 
        boxShadow: "rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px",
        padding: "10px",
        backgroundColor: "#cfdbd5",
        width: "100%",
        borderRadius: "5px"
      }
    }>
      <h1>{name}</h1>
      <h2 style={{ fontStyle: "italic", color: "#343a40" }}>@{username}</h2>
      <ul style={{ color: "#343a40", listStyleType: "none", padding: 0, marginTop: "5px" }}>
        <li>{connections} {connections > 1 ? "conexões" : "conexão"}</li>
        <li>membro desde {createdAt.getFullYear()}</li>
      </ul>
    </div>
  );
}