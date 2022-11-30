import React, { useState, useEffect } from "react";

export default function InfoBox(props) {
  // const [style, setStyle] = useState({display: 'none'});

  const [name, setName] = useState(props.name)
  const [username, setUsername] = useState(props.username)

  useEffect(() => {
    setName(props.name)
    setUsername(props.username)
  }, [props])


  return (
    <div className="info-box" style={
      { 
        boxShadow: "rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px",
        padding: "10px"
      }
    }>
      <h1>{name}</h1>
      <h2>{`@${username}`}</h2>
    </div>
  );
}