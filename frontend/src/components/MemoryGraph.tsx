"use client"

import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'

interface Memory {
  id: string
  name: string
  type: string
  recall_strength: number
  risk_score?: number
  emotional_weight?: number
  importance?: number
}

interface MemoryConnection {
  source: string
  target: string
  strength: number
  type?: string
}

interface MemoryGraphProps {
  memories: Memory[]
  connections: MemoryConnection[]
  width?: number
  height?: number
  onNodeClick?: (memory: Memory) => void
}

export default function MemoryGraph({
  memories,
  connections,
  width = 800,
  height = 600,
  onNodeClick
}: MemoryGraphProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [selectedNode, setSelectedNode] = useState<Memory | null>(null)

  useEffect(() => {
    if (!svgRef.current || memories.length === 0) return

    // Clear previous graph
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height])

    // Create a container group for zooming/panning
    const container = svg.append('g')

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        container.attr('transform', event.transform)
      })

    svg.call(zoom as any)

    // Prepare data for D3
    const nodes = memories.map(m => ({ ...m }))
    const links = connections.map(c => ({ ...c }))

    // Create force simulation
    const simulation = d3.forceSimulation(nodes as any)
      .force('link', d3.forceLink(links as any)
        .id((d: any) => d.id)
        .distance(100)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30))

    // Add arrow markers for directed edges
    svg.append('defs').selectAll('marker')
      .data(['end'])
      .enter().append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 25)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#999')

    // Add links
    const link = container.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d: any) => Math.sqrt(d.strength * 5))
      .attr('marker-end', 'url(#arrowhead)')

    // Add nodes
    const node = container.append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(nodes)
      .enter().append('g')
      .call(d3.drag<any, any>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended) as any
      )

    // Add circles for nodes
    node.append('circle')
      .attr('r', (d: any) => 10 + (d.importance || 5))
      .attr('fill', (d: any) => getNodeColor(d))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', function(event, d: any) {
        setSelectedNode(d)
        if (onNodeClick) onNodeClick(d)

        // Highlight selected node
        d3.selectAll('circle').attr('stroke-width', 2)
        d3.select(this).attr('stroke-width', 4)
      })
      .on('mouseover', function(event, d: any) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', (d: any) => 15 + (d.importance || 5))
      })
      .on('mouseout', function(event, d: any) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('r', (d: any) => 10 + (d.importance || 5))
      })

    // Add labels
    node.append('text')
      .text((d: any) => d.name)
      .attr('x', 15)
      .attr('y', 3)
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .style('pointer-events', 'none')

    // Add memory type icon
    node.append('text')
      .text((d: any) => getMemoryIcon(d.type))
      .attr('x', -5)
      .attr('y', 5)
      .attr('font-size', '14px')
      .style('pointer-events', 'none')

    // Update positions on each tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y)

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`)
    })

    // Drag functions
    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    }

    function dragged(event: any, d: any) {
      d.fx = event.x
      d.fy = event.y
    }

    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    }

    // Cleanup
    return () => {
      simulation.stop()
    }

  }, [memories, connections, width, height, onNodeClick])

  // Helper function to get node color based on risk
  function getNodeColor(memory: Memory): string {
    const recallStrength = memory.recall_strength || 80
    const riskScore = memory.risk_score || (1 - recallStrength / 100)

    if (riskScore > 0.7) return '#ef4444' // High risk - red
    if (riskScore > 0.4) return '#f59e0b' // Medium risk - orange
    if (riskScore > 0.2) return '#fbbf24' // Low risk - yellow
    return '#10b981' // Safe - green
  }

  // Helper function to get memory type icon
  function getMemoryIcon(type: string): string {
    const icons: Record<string, string> = {
      person: '👤',
      place: '📍',
      event: '📅',
      skill: '🎯',
      routine: '🔄',
      object: '📦'
    }
    return icons[type.toLowerCase()] || '💭'
  }

  return (
    <div className="relative">
      <svg
        ref={svgRef}
        className="border border-gray-200 rounded-lg bg-white shadow-sm"
      />

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-md border border-gray-200">
        <h4 className="font-semibold text-sm mb-2">Risk Levels</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Safe (80-100%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
            <span>Low Risk (60-80%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span>Medium Risk (40-60%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>High Risk (&lt;40%)</span>
          </div>
        </div>
      </div>

      {/* Selected node info */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 bg-white p-4 rounded-lg shadow-md border border-gray-200 max-w-xs">
          <h4 className="font-semibold text-sm mb-2">
            {getMemoryIcon(selectedNode.type)} {selectedNode.name}
          </h4>
          <div className="space-y-1 text-xs text-gray-600">
            <div>Type: <span className="font-medium">{selectedNode.type}</span></div>
            <div>Recall: <span className="font-medium">{selectedNode.recall_strength}%</span></div>
            {selectedNode.emotional_weight !== undefined && (
              <div>Emotional: <span className="font-medium">{(selectedNode.emotional_weight * 100).toFixed(0)}%</span></div>
            )}
            {selectedNode.importance !== undefined && (
              <div>Importance: <span className="font-medium">{selectedNode.importance}/10</span></div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
