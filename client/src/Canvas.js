import React, { useState, useEffect } from "react"
import Graph from "react-graph-vis"
import InfoBox from "./InfoBox"

function Canvas() {
  const [graph, setGraph] = useState({
    nodes: [],
    edges: []
  })

  const [visJS, setVisJS] = useState(null)

  const [palette, setPalette] = useState(
    ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51"]
  )

  const [infoBox, setInfoBox] = useState({
    display: "none",
    name: "",
    username: ""
  })

  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((response) => { return response.json() })
      .then((data) => { setGraphData(data) })
  }, [])

  const setGraphData = (graph_data) => {
    graph_data.nodes = Object.values(graph_data.nodes).map((node) => {
      var size = node.degree_centrality * 10000

      size = size < 20 ? 20 : size
      size = size > 100 ? 100 : size

      return {
        id: node.id,
        name: node.name,
        username: node.username,
        created_at: node.created_at,
        x: node.x * 20000,
        y: node.y * 20000,
        label: node.username,
        size: size,
        title: node.community,
        color: {
          border: palette[node.community % 5],
          background: palette[node.community % 5]
        }
      }
    })

    // ensure there are no repeated IDs
    graph_data.nodes = graph_data.nodes.reduce((foundValues, nextNode) =>
      foundValues.map((value) => value.id).includes(nextNode.id) ?
      foundValues : foundValues.concat(nextNode), []
    )

    graph_data.edges = Object.values(graph_data.edges).map((edge) => {
      var parent_node = graph_data.nodes.reduce((node) => node.id === edge.from)

      return {
        from: edge.from,
        to: edge.to,
        color: {
          color: palette[parent_node.community % 5]
        }
      }
    })

    setGraph(graph_data)
  }

  const canvasStyle = {
    // backgroundColor: "#041C32"
    backgroundColor: "#FFFFFF"
  }

  const options = {
    nodes: {
      shape: "dot",
      color: {
        // border: "#000000",
        // background: "#ECB365",
        hover: {
          border: "#000000",
          background: "#A5C9CA"
        }
      },
      font: {
        color: "#DCD7C9"
      }
    },
    edges: {
      smooth: false,
      // color: {
      //   color: "#A5C9CA"
      // }
    },
    physics: false,
    interaction: {
      dragNodes: true,
      zoomView: true,
      dragView: true,
      hover: true
    }
  }

  const events = {
    hoverNode: (e) => { 
      // var node_data = visJS.get(node)
      var node = visJS.body.nodes[e.node].options
      // console.log(visJS)
      // console.log(visJS.body.nodes[node.node].options)
      setInfoBox({
        display: "block",
        name: node.name,
        username: node.username
      })
    },
    blurNode: () => {
      setInfoBox({
        display: "none",
        name: "",
        username: ""
      })
    }
  }

  return (
    <div id="graph-screen">
      <div style={
        { 
          display: infoBox.display, 
          position: "absolute", 
          backgroundColor: "#FFFFFF", 
          width: 300, 
          height: 300, 
          right: "4%",
          top: "4%",
          zIndex: 1000 
        }
      }>
        <InfoBox {...infoBox}/>
      </div>
      
      <div id="canvas" style={canvasStyle}>
        <Graph
          graph={graph}
          options={options}
          events={events}
          style={{ height: "100vh", position: "relative", zIndex: 1 }}
          getNetwork={network => {
            network.moveTo({scale: 0.05})
            setVisJS(network)
          }}
        />
      </div>
    </div>
  )
}

export default Canvas