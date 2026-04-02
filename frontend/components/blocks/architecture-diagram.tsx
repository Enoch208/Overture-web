"use client";

import { ElementType } from "react";
import {
  ReactFlow,
  Background,
  type Node,
  type Edge,
  type NodeProps,
  Handle,
  Position,
  BaseEdge,
  getSmoothStepPath,
  type EdgeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import {
  StethoscopeIcon,
  DocumentValidationIcon,
  AiNetworkIcon,
  DatabaseIcon,
  ChatBotIcon,
  BrainIcon,
  SecurityCheckIcon,
} from "hugeicons-react";

/* ── Icon map ── */
const iconMap: Record<string, ElementType> = {
  stethoscope: StethoscopeIcon,
  document: DocumentValidationIcon,
  network: AiNetworkIcon,
  database: DatabaseIcon,
  chatbot: ChatBotIcon,
  brain: BrainIcon,
  security: SecurityCheckIcon,
};

/* ── Custom Node ── */
function AgentNode({ data }: NodeProps) {
  const Icon = iconMap[data.icon as string];
  const isCenter = data.accent === "emerald";

  return (
    <div className="flex flex-col items-center gap-2.5 group">
      {/* Icon circle — handles are anchored here */}
      <div className="relative">
        <Handle type="target" position={Position.Left} className="!bg-transparent !border-0 !w-0 !h-0 !top-1/2" />
        <Handle type="target" position={Position.Top} className="!bg-transparent !border-0 !w-0 !h-0 !left-1/2" />
        <Handle type="source" position={Position.Right} className="!bg-transparent !border-0 !w-0 !h-0 !top-1/2" />
        <Handle type="source" position={Position.Bottom} className="!bg-transparent !border-0 !w-0 !h-0 !left-1/2" />

        <div
          className={`
            w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500
            ${
              isCenter
                ? "bg-dark-contrast shadow-[0_0_40px_-8px_rgba(26,47,36,0.25)]"
                : "bg-slate-50"
            }
          `}
        >
          {Icon && (
            <Icon
              size={22}
              strokeWidth={1.5}
              className={isCenter ? "text-white" : "text-secondary"}
            />
          )}
        </div>
      </div>

      {/* Label — outside the handle container */}
      <div className="text-center">
        <p className="font-body text-[13px] font-medium text-primary leading-tight">
          {data.label as string}
        </p>
        <p className="font-mono text-[9px] uppercase tracking-widest text-secondary/60 mt-0.5">
          {data.sublabel as string}
        </p>
      </div>
    </div>
  );
}

/* ── Animated Edge with flowing dot ── */
function AnimatedEdge(props: EdgeProps) {
  const { sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition } = props;
  const [edgePath] = getSmoothStepPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    borderRadius: 24,
  });

  return (
    <>
      <BaseEdge path={edgePath} style={{ stroke: "rgba(26,47,36,0.12)", strokeWidth: 2 }} />
      {/* Animated pulse dot */}
      <circle r="3.5" fill="#10b981">
        <animateMotion dur="3s" repeatCount="indefinite" path={edgePath} />
        <animate attributeName="opacity" values="0;0.8;0.8;0" dur="3s" repeatCount="indefinite" />
      </circle>
    </>
  );
}

/* ── Node & Edge definitions ── */
const nodeDefaults = { type: "agent" as const, draggable: false, selectable: false, connectable: false };

/*
  Actual flow:
  1. EHR → Provider Agent (triggers PA detection)
  2. Provider Agent → Evidence Bundler MCP (pulls FHIR data)
  3. Provider Agent → Rules Engine MCP (checks criteria)
  4. Provider Agent ↔ Payer Agent (A2A/COIN negotiation — the core)
  5. Payer Agent → Rules Engine MCP (evaluates evidence)
  6. Provider Agent → EHR (writes back determination)

  Layout: EHR on far left, Provider Agent left-center, Payer Agent right-center,
  MCP tools above each agent, A2A connection in the middle
*/
// Evenly spaced: 0, 250, 500, 750. MCP tools centered above their agents.
const initialNodes: Node[] = [
  // Main row (y=140)
  {
    id: "ehr",
    position: { x: 0, y: 140 },
    data: { label: "EHR System", sublabel: "FHIR R4", icon: "stethoscope" },
    ...nodeDefaults,
  },
  {
    id: "provider",
    position: { x: 250, y: 140 },
    data: { label: "Provider Agent", sublabel: "PA Coordinator", icon: "chatbot", accent: "emerald" },
    ...nodeDefaults,
  },
  {
    id: "payeragent",
    position: { x: 500, y: 140 },
    data: { label: "Payer Agent", sublabel: "Review Agent", icon: "brain", accent: "emerald" },
    ...nodeDefaults,
  },
  {
    id: "payer",
    position: { x: 750, y: 140 },
    data: { label: "Payer System", sublabel: "Determination", icon: "security" },
    ...nodeDefaults,
  },
  // MCP tools (y=0) — Evidence Bundler above Provider, Rules Engine above Payer Agent
  {
    id: "bundler",
    position: { x: 250, y: 0 },
    data: { label: "Evidence Bundler", sublabel: "MCP Server", icon: "document" },
    ...nodeDefaults,
  },
  {
    id: "rules",
    position: { x: 500, y: 0 },
    data: { label: "Rules Engine", sublabel: "MCP Server", icon: "database" },
    ...nodeDefaults,
  },
];

const initialEdges: Edge[] = [
  // EHR triggers Provider Agent
  { id: "e-ehr-provider", source: "ehr", target: "provider", type: "animated" },
  // Provider Agent calls Evidence Bundler
  { id: "e-provider-bundler", source: "provider", target: "bundler", type: "animated" },
  // Provider Agent calls Rules Engine
  { id: "e-provider-rules", source: "provider", target: "rules", type: "animated" },
  // A2A: Provider Agent ↔ Payer Agent (the core negotiation)
  { id: "e-provider-payer-agent", source: "provider", target: "payeragent", type: "animated" },
  // Payer Agent calls Rules Engine
  { id: "e-payeragent-rules", source: "payeragent", target: "rules", type: "animated" },
  // Payer Agent returns to Payer System
  { id: "e-payeragent-payer", source: "payeragent", target: "payer", type: "animated" },
];

const nodeTypes = { agent: AgentNode };
const edgeTypes = { animated: AnimatedEdge };

/* ── Main Component ── */
export function ArchitectureDiagram() {

  return (
    <div className="relative">
      <div className="relative bg-canvas-elevated rounded-3xl border border-black/5 overflow-hidden shadow-soft">
        <div className="p-6 md:p-10">
          {/* React Flow canvas */}
          <div className="h-[280px] w-full">
            <ReactFlow
              nodes={initialNodes}
              edges={initialEdges}
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}

              fitView
              fitViewOptions={{ padding: 0.1 }}
              proOptions={{ hideAttribution: true }}
              panOnDrag={false}
              zoomOnScroll={false}
              zoomOnPinch={false}
              zoomOnDoubleClick={false}
              nodesDraggable={false}
              nodesConnectable={false}
              elementsSelectable={false}
              minZoom={0.5}
              maxZoom={1}
            >
              <Background color="rgba(0,0,0,0.03)" gap={32} size={1} />
            </ReactFlow>
          </div>

          {/* FHIR resources footer */}
          <div className="mt-4 pt-5 border-t border-black/5 flex flex-wrap items-center gap-2">
            <span className="font-mono text-[10px] text-secondary/50 uppercase tracking-widest mr-2">
              FHIR R4:
            </span>
            {["Patient", "Condition", "Observation", "MedicationRequest", "Procedure", "Claim", "ClaimResponse"].map(
              (resource) => (
                <span
                  key={resource}
                  className="px-2.5 py-1 rounded-full bg-slate-50 border border-black/5 font-mono text-[10px] text-secondary"
                >
                  {resource}
                </span>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
