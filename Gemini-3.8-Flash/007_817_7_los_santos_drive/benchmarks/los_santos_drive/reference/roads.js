/**
 * Road Network Graph for Los Santos Drive
 * Single source of truth for traffic, missions, and player resets.
 */

export class RoadGraph {
  constructor() {
    this.nodes = new Map(); // id -> { id, x, z, neighbors: [] }
    this.edges = []; // list of directed lane segments
    this.lanes = []; // alias to edges with helper properties
    this.initGrid();
  }

  initGrid() {
    // 5x5 grid of intersections from -160 to +160 with 80m spacing
    const coords = [-160, -80, 0, 80, 160];
    const laneOffset = 3.5; // distance from centerline to lane center

    // 1. Create nodes
    for (let ix = 0; ix < coords.length; ix++) {
      for (let iz = 0; iz < coords.length; iz++) {
        const id = `node_${ix}_${iz}`;
        this.nodes.set(id, {
          id,
          ix,
          iz,
          x: coords[ix],
          z: coords[iz],
          neighbors: []
        });
      }
    }

    // Helper to add directed lane between nodes
    const addLane = (fromNode, toNode, offsetSign) => {
      const dx = toNode.x - fromNode.x;
      const dz = toNode.z - fromNode.z;
      const len = Math.hypot(dx, dz);
      if (len === 0) return;

      const ux = dx / len;
      const uz = dz / len;
      // Perpendicular vector for lane offset (right side of driving direction)
      const px = -uz * offsetSign * laneOffset;
      const pz = ux * offsetSign * laneOffset;

      const startX = fromNode.x + px;
      const startZ = fromNode.z + pz;
      const endX = toNode.x + px;
      const endZ = toNode.z + pz;

      const lane = {
        id: `lane_${fromNode.id}_${toNode.id}`,
        fromNode: fromNode.id,
        toNode: toNode.id,
        startX,
        startZ,
        endX,
        endZ,
        dirX: ux,
        dirZ: uz,
        heading: Math.atan2(ux, uz), // yaw angle where 0 is +Z
        length: len,
        speedLimit: 12.0 // ~43 km/h
      };

      this.edges.push(lane);
      this.lanes.push(lane);
      fromNode.neighbors.push({
        nodeId: toNode.id,
        laneId: lane.id,
        distance: len
      });
    };

    // 2. Connect grid nodes horizontally and vertically
    for (let ix = 0; ix < coords.length; ix++) {
      for (let iz = 0; iz < coords.length; iz++) {
        const curr = this.nodes.get(`node_${ix}_${iz}`);

        // Horizontal connection (East: +X)
        if (ix < coords.length - 1) {
          const east = this.nodes.get(`node_${ix + 1}_${iz}`);
          // Eastbound lane (drives on right side: offsetSign = -1)
          addLane(curr, east, -1);
          // Westbound lane (drives on right side: offsetSign = -1)
          addLane(east, curr, -1);
        }

        // Vertical connection (South: +Z)
        if (iz < coords.length - 1) {
          const south = this.nodes.get(`node_${ix}_${iz + 1}`);
          // Southbound lane (drives on right side: offsetSign = -1)
          addLane(curr, south, -1);
          // Northbound lane (drives on right side: offsetSign = -1)
          addLane(south, curr, -1);
        }
      }
    }
  }

  /**
   * Find the closest point on any road lane to (x, z).
   * Used by R reset, vehicle positioning, and mission placement.
   */
  getNearestLane(x, z) {
    let bestDistSq = Infinity;
    let bestResult = null;

    for (const lane of this.lanes) {
      const dx = lane.endX - lane.startX;
      const dz = lane.endZ - lane.startZ;
      const lenSq = dx * dx + dz * dz;

      // Project (x, z) onto lane segment
      let t = ((x - lane.startX) * dx + (z - lane.startZ) * dz) / lenSq;
      t = Math.max(0.05, Math.min(0.95, t)); // keep away from sharp intersection centers

      const projX = lane.startX + t * dx;
      const projZ = lane.startZ + t * dz;
      const distSq = (x - projX) * (x - projX) + (z - projZ) * (z - projZ);

      if (distSq < bestDistSq) {
        bestDistSq = distSq;
        bestResult = {
          lane,
          point: { x: projX, z: projZ },
          distance: Math.sqrt(distSq),
          heading: lane.heading,
          direction: { x: lane.dirX, z: lane.dirZ }
        };
      }
    }

    return bestResult;
  }

  /**
   * Pick a random valid position along a road lane.
   */
  getRandomLanePosition(margin = 0.15) {
    const lane = this.lanes[Math.floor(Math.random() * this.lanes.length)];
    const t = margin + Math.random() * (1 - 2 * margin);
    const x = lane.startX + t * (lane.endX - lane.startX);
    const z = lane.startZ + t * (lane.endZ - lane.startZ);

    return {
      x,
      z,
      lane,
      heading: lane.heading,
      direction: { x: lane.dirX, z: lane.dirZ }
    };
  }

  /**
   * Dijkstra shortest path search on the road network graph.
   */
  findPathDijkstra(startNodeId, targetNodeId) {
    const distances = new Map();
    const previous = new Map();
    const unvisited = new Set(this.nodes.keys());

    for (const nodeId of this.nodes.keys()) {
      distances.set(nodeId, Infinity);
    }
    distances.set(startNodeId, 0);

    while (unvisited.size > 0) {
      let current = null;
      let minDistance = Infinity;

      for (const nodeId of unvisited) {
        const dist = distances.get(nodeId);
        if (dist < minDistance) {
          minDistance = dist;
          current = nodeId;
        }
      }

      if (!current || minDistance === Infinity || current === targetNodeId) {
        break;
      }

      unvisited.delete(current);
      const node = this.nodes.get(current);

      for (const edge of node.neighbors) {
        if (!unvisited.has(edge.nodeId)) continue;
        const alt = distances.get(current) + edge.distance;
        if (alt < distances.get(edge.nodeId)) {
          distances.set(edge.nodeId, alt);
          previous.set(edge.nodeId, { fromNode: current, laneId: edge.laneId });
        }
      }
    }

    // Reconstruct path
    const path = [];
    let curr = targetNodeId;
    while (previous.has(curr)) {
      const prevInfo = previous.get(curr);
      path.unshift(prevInfo);
      curr = prevInfo.fromNode;
    }

    return path;
  }

  /**
   * Get outgoing lanes from a specific node.
   */
  getOutgoingLanes(nodeId) {
    const node = this.nodes.get(nodeId);
    if (!node) return [];
    return node.neighbors.map(n => this.lanes.find(l => l.id === n.laneId)).filter(Boolean);
  }
}
