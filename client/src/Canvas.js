import React, { Component } from "react"
import Graph from "react-graph-vis";

class Canvas extends Component {
  constructor(props) {
    super(props)

    this.state = {
      graph: {
        nodes: [],
        edges: []
      }
    }

    this.setGraphData = this.setGraphData.bind(this)
  }

  componentDidMount() {
    fetch("http://localhost:5000/")
      .then((response) => { return response.json() })
      .then((data) => { this.setGraphData(data) })
  }

  setGraphData(graph_data) {
    graph_data.nodes = Object.values(graph_data.nodes).map((node) => {
      return {
        id: node.id,
        name: node.name,
        username: node.username,
        created_at: node.created_at,
        x: node.x * 10000,
        y: node.y * 10000,
        label: node.username
      }
    })

    this.setState(() => {
      return { graph: graph_data }
    })
  }

  render() {
    const canvasStyle = {
      backgroundColor: "#6D6875"
    }

    const options = {
      nodes: {
        shape: "dot",
        color: {
          border: "#B5838D",
          background: "#E5989B"
        }
      },
      edges: {
        smooth: false
      },
      physics: false,
      interaction: {
        dragNodes: true,
        zoomView: true,
        dragView: true
      }
    }

    return (
      <div id="canvas" style={canvasStyle}>
        <Graph
          graph={this.state.graph}
          options={options}
          style={{ height: "100vh" }}
        />
      </div>
    )
  }
}

export default Canvas
