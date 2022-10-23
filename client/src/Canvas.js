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
        size: size
      }
    })

    var min = graph_data.nodes.reduce(function(prev, curr) {
      return prev.size < curr.size ? prev : curr
    })

    var max = graph_data.nodes.reduce(function(prev, curr) {
      return prev.size < curr.size ? curr : prev
    })

    console.log(`min: ${min.size}, max: ${max.size}`)

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
          background: "#E5989B",
          // hover: {
          //   border: ,
          //   background:
          // }
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
