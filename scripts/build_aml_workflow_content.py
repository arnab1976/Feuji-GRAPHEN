# -*- coding: utf-8 -*-
"""
Full AML Workflow Generator and Injector for index.html
Builds the complete interactive animated AML workflow tab with SVG, controls, deep-dives, inspector, and cheat sheet.
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

def get_aml_workflow_html():
    return '''
        <!-- ==================== STYLES FOR AML MODAL & ANIMATIONS ==================== -->
        <style id="aml-workflow-modal-styles">
          .aml-modal-overlay {
            position: fixed;
            inset: 0;
            z-index: 999999;
            background: rgba(3, 7, 18, 0.94);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            display: none;
            align-items: center;
            justify-content: center;
            padding: 12px;
            box-sizing: border-box;
          }
          .aml-modal-card {
            width: 98vw;
            height: 96vh;
            max-width: 1750px;
            background: #090E1A;
            border: 2px solid var(--amber, #FF9F0A);
            border-radius: 14px;
            box-shadow: 0 0 60px rgba(0,0,0,0.95), 0 0 32px rgba(255,159,10,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
          }
          .aml-modal-header {
            background: #0E1626;
            border-bottom: 1.5px solid #1E293B;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
            gap: 16px;
          }
          .aml-modal-close-btn {
            background: rgba(244, 63, 94, 0.15);
            border: 1.5px solid #F43F5E;
            color: #F43F5E;
            width: 38px;
            height: 38px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            box-shadow: 0 0 10px rgba(244, 63, 94, 0.25);
            line-height: 1;
          }
          .aml-modal-close-btn:hover {
            background: #F43F5E;
            color: #FFFFFF;
            transform: scale(1.08);
            box-shadow: 0 0 18px rgba(244, 63, 94, 0.65);
          }
          .aml-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.02em;
          }
          .aml-badge.amber { background: rgba(255,159,10,0.15); border: 1px solid rgba(255,159,10,0.4); color: #FF9F0A; }
          .aml-badge.blue { background: rgba(96,165,250,0.15); border: 1px solid rgba(96,165,250,0.4); color: #60A5FA; }
          .aml-badge.emerald { background: rgba(61,220,151,0.15); border: 1px solid rgba(61,220,151,0.4); color: #3DDC97; }
          .aml-badge.purple { background: rgba(168,85,247,0.15); border: 1px solid rgba(168,85,247,0.4); color: #C084FC; }
          .aml-badge.rose { background: rgba(244,63,94,0.15); border: 1px solid rgba(244,63,94,0.4); color: #F43F5E; }

          .aml-step-btn {
            background: #111827;
            border: 1px solid #374151;
            color: #9CA3AF;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            transition: all 0.2s ease;
          }
          .aml-step-btn:hover {
            border-color: #FF9F0A;
            color: #F3F4F6;
            background: #1F2937;
          }
          .aml-step-btn.active {
            background: rgba(255,159,10,0.18);
            border-color: #FF9F0A;
            color: #FFFFFF;
            box-shadow: 0 0 12px rgba(255,159,10,0.3);
          }

          .aml-tab-pill {
            background: #111827;
            border: 1px solid #374151;
            color: #9CA3AF;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
          }
          .aml-tab-pill:hover {
            background: #1F2937;
            color: #F3F4F6;
          }
          .aml-tab-pill.active {
            background: #2563EB;
            border-color: #3B82F6;
            color: #FFFFFF;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(59,130,246,0.35);
          }

          .aml-node {
            cursor: pointer;
            transition: transform 0.2s ease, filter 0.2s ease;
          }
          .aml-node:hover {
            filter: drop-shadow(0 0 12px rgba(255,159,10,0.85)) !important;
            transform: scale(1.05);
          }

          .aml-edge {
            cursor: pointer;
            transition: stroke 0.2s ease, stroke-width 0.2s ease;
          }
          .aml-edge:hover {
            stroke-width: 4 !important;
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.85));
          }

          @keyframes amlEdgeDash {
            0% { stroke-dashoffset: 48; }
            100% { stroke-dashoffset: 0; }
          }
          .aml-flowing-edge {
            stroke-dasharray: 8 6 !important;
            animation: amlEdgeDash 1.2s linear infinite !important;
          }

          @keyframes amlPulseGlow {
            0%, 100% { transform: scale(1); filter: drop-shadow(0 0 5px rgba(255,159,10,0.5)); }
            50% { transform: scale(1.04); filter: drop-shadow(0 0 16px rgba(255,159,10,0.95)); }
          }
          .aml-active-pulse {
            animation: amlPulseGlow 1.8s ease-in-out infinite;
            transform-origin: center;
          }

          @keyframes amlRedDangerPulse {
            0%, 100% { stroke-width: 3; filter: drop-shadow(0 0 6px rgba(244,63,94,0.6)); }
            50% { stroke-width: 5; filter: drop-shadow(0 0 20px rgba(244,63,94,1)); }
          }
          .aml-danger-cycle {
            animation: amlRedDangerPulse 1.2s ease-in-out infinite !important;
          }

          @keyframes amlDotPulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); opacity: 0.5; }
          }
        </style>

        <!-- ==================== FULL-SCALE SEPARATE POPUP MODAL WINDOW ==================== -->
        <div id="amlModalOverlay" class="aml-modal-overlay" onclick="if(event.target===this)closeAmlModal()">
          <div id="amlModalCard" class="aml-modal-card" onclick="event.stopPropagation()">
            
            <!-- MODAL HEADER BAR -->
            <div id="amlModalHeader" class="aml-modal-header">
              <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <span class="aml-badge amber">⚡ FULL-SCREEN INTERACTIVE SIMULATOR</span>
                <span class="aml-badge blue">FINANCIAL AML & FRAUD USE CASE</span>
                <span class="aml-badge emerald">7-STAGE MASTER WORKFLOW</span>
                <span class="aml-badge purple">HYBRID GRAPH-RAG</span>
                <h2 style="color:#F8FAFC; font-size:16px; margin:0; font-weight:800; display:inline-flex; align-items:center; gap:8px;">
                  Interactive AML Knowledge Graph Simulator: Data Unification & Pattern Recognition
                </h2>
              </div>

              <!-- RIGHT SIDE: STATUS & CROSS (X) CLOSE BUTTON -->
              <div style="display:flex; align-items:center; gap:14px;">
                <div style="background:rgba(255,159,10,0.12); border:1px solid rgba(255,159,10,0.4); border-radius:8px; padding:4px 12px; text-align:right;">
                  <div style="font-size:10px; color:var(--amber); font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Executive Panel Mode</div>
                  <div id="amlModalStageIndicator" style="font-size:12.5px; font-weight:800; color:#FFFFFF;">Stage 1 of 7 Active</div>
                </div>

                <!-- TOP-RIGHT CROSS (X) BUTTON -->
                <button type="button" onclick="closeAmlModal()" id="amlModalCloseBtn" class="aml-modal-close-btn" title="Close Window (Esc)" aria-label="Close interactive window">
                  ✕
                </button>
              </div>
            </div>

            <!-- MODAL BODY (SCROLLABLE, EXPANSIVE VIEWPORT) -->
            <div id="amlModalBody" style="flex:1; overflow-y:auto; padding:18px 22px; display:flex; flex-direction:column; gap:14px;">

            
            <!-- HEADER -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:16px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                  <span class="aml-badge amber">⚡ INTERVIEW-READY SIMULATOR</span>
                  <span class="aml-badge blue">FINANCIAL AML & FRAUD USE CASE</span>
                  <span class="aml-badge emerald">7-STAGE INTERACTIVE WORKFLOW</span>
                  <span class="aml-badge purple">HYBRID GRAPH-RAG</span>
                </div>
                <h2 style="color:var(--tx-0); font-size:22px; margin:0 0 6px; font-weight:800; letter-spacing:-0.01em;">
                  Interactive Animated AML Workflow: Multi-Source Data Unification & Pattern Recognition
                </h2>
                <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin:0; max-width:980px;">
                  Step-by-step interactive demonstration explaining how structured banking tables and unstructured compliance documents map together, transform, bind into a unified Neo4j property graph via canonical keys, and leverage <strong>Protégé, ChromaDB, Neo4j, Cypher & Hybrid Graph-RAG</strong> to detect a <strong>$14.25M circular laundering ring</strong>. Designed specifically for explaining to an executive or technical interview panel.
                </p>
              </div>
              <div style="background:rgba(255,159,10,0.1); border:1px solid rgba(255,159,10,0.3); border-radius:8px; padding:8px 14px; text-align:right;">
                <div style="font-size:11px; color:var(--amber); font-weight:700;">PANEL TALK-TRACK READY</div>
                <div style="font-size:16px; font-weight:800; color:var(--tx-0);">7-Step Master Simulation</div>
              </div>
            </div>

            <!-- STEP SELECTOR PILLS -->
            <div style="display:flex; gap:8px; overflow-x:auto; padding-bottom:8px; margin-bottom:14px;" id="amlStepSelectorBar">
              <button type="button" class="aml-step-btn active" onclick="setAmlStep(1)" id="amlStepBtn-1">
                <span style="background:var(--amber); color:#000; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">1</span>
                <span>Structured Joins</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(2)" id="amlStepBtn-2">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">2</span>
                <span>Unstructured Mapping</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(3)" id="amlStepBtn-3">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">3</span>
                <span>Data Transformation</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(4)" id="amlStepBtn-4">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">4</span>
                <span>Key Binding Engine</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(5)" id="amlStepBtn-5">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">5</span>
                <span>5 Core Tool Roles</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(6)" id="amlStepBtn-6">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">6</span>
                <span>Pattern Recognition</span>
              </button>
              <button type="button" class="aml-step-btn" onclick="setAmlStep(7)" id="amlStepBtn-7">
                <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">7</span>
                <span>Executive Deliverables</span>
              </button>
            </div>

            <!-- PLAYBACK CONTROL TOOLBAR WITH REAL-TIME TIMER FEEDBACK -->
            <div style="background:#0F172A; border:1px solid #1E293B; border-radius:8px; padding:10px 16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
              <div style="display:flex; align-items:center; gap:8px;">
                <button type="button" class="btn btn-sm btn-secondary" onclick="prevAmlStep()" title="Previous Step">◀ Prev</button>
                <button type="button" class="btn btn-sm btn-primary" id="amlPlayPauseBtn" onclick="toggleAmlPlay()" style="min-width:125px; font-weight:800;">
                  ▶ Auto-Play Tour
                </button>
                <button type="button" class="btn btn-sm btn-secondary" onclick="nextAmlStep()" title="Next Step">Next ▶</button>
                <button type="button" class="btn btn-sm btn-secondary" onclick="resetAmlTour()" title="Reset to Step 1" style="color:var(--tx-3);">↺ Reset</button>
                
                <!-- LIVE TIMER COUNTDOWN BADGE -->
                <span id="amlTimerBadge" style="display:none; align-items:center; gap:6px; background:rgba(255,159,10,0.12); border:1px solid rgba(255,159,10,0.4); color:var(--amber); border-radius:20px; padding:3px 12px; font-size:11.5px; font-weight:700; font-family:monospace;">
                  ⏱ Auto-advancing in 8.0s
                </span>
              </div>

              <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:12px; color:var(--tx-2);">Speed:</span>
                <select id="amlSpeedSelect" onchange="changeAmlSpeed(this.value)" style="background:#090E1A; color:#E2E8F0; border:1px solid #334155; border-radius:6px; padding:4px 8px; font-size:12px;">
                  <option value="1">1x (Normal - 8s)</option>
                  <option value="2">2x (Fast - 4s)</option>
                  <option value="0.5">0.5x (Detailed - 14s)</option>
                </select>
                <div style="height:18px; width:1px; background:#334155;"></div>
                <div id="amlStepLabel" style="font-size:12.5px; font-weight:700; color:var(--amber);">
                  Stage 1/7: Multi-Source Structured Data Mapping
                </div>
              </div>
            </div>

            <!-- DUAL PROGRESS BAR: STEP COUNTDOWN (TOP) & OVERALL TOUR PROGRESS (BOTTOM) -->
            <div style="background:#0B101B; border:1px solid #1E293B; border-radius:4px; padding:3px; display:flex; flex-direction:column; gap:3px;">
              <!-- Step countdown bar -->
              <div style="height:4px; background:#1E293B; border-radius:2px; overflow:hidden;">
                <div id="amlStepProgressBar" style="height:100%; width:0%; background:linear-gradient(90deg, #FF9F0A, #3DDC97); transition:width 0.05s linear;"></div>
              </div>
              <!-- Overall Tour 1-7 progress bar -->
              <div style="height:3px; background:#111827; border-radius:2px; overflow:hidden;">
                <div id="amlOverallProgressBar" style="height:100%; width:14.28%; background:linear-gradient(90deg, #3B82F6, #A855F7); transition:width 0.3s ease;"></div>
              </div>
            </div>

            <!-- ANIMATED HIGH-DEFINITION SVG CANVAS -->
            <div style="background:#0B101B; border:1.5px solid var(--line-strong); border-radius:12px; padding:12px; position:relative; overflow:hidden; box-shadow:inset 0 0 40px rgba(0,0,0,0.6);">
              
              <!-- Canvas Watermark / Sub-header -->
              <div style="position:absolute; top:12px; right:16px; z-index:5; font-size:11px; color:var(--tx-3); font-family:var(--mono);">
                INTERACTIVE CANVAS · CLICK ANY NODE OR RELATIONSHIP TO INSPECT
              </div>

              <svg id="amlSvgCanvas" viewBox="0 0 1150 560" style="width:100%; height:auto; display:block; user-select:none;">
                <defs>
                  <!-- Glow Filters -->
                  <filter id="glowAmber" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#FF9F0A" flood-opacity="0.8"/>
                  </filter>
                  <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#60A5FA" flood-opacity="0.8"/>
                  </filter>
                  <filter id="glowEmerald" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#3DDC97" flood-opacity="0.8"/>
                  </filter>
                  <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#A855F7" flood-opacity="0.8"/>
                  </filter>
                  <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#F43F5E" flood-opacity="1"/>
                  </filter>

                  <!-- Arrow Markers -->
                  <marker id="arrowAmber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 9 5 L 0 9 z" fill="#FF9F0A"/>
                  </marker>
                  <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 9 5 L 0 9 z" fill="#60A5FA"/>
                  </marker>
                  <marker id="arrowEmerald" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 9 5 L 0 9 z" fill="#3DDC97"/>
                  </marker>
                  <marker id="arrowPurple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 9 5 L 0 9 z" fill="#A855F7"/>
                  </marker>
                  <marker id="arrowRed" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 1 L 9 5 L 0 9 z" fill="#F43F5E"/>
                  </marker>

                  <!-- Gradient Shaders -->
                  <linearGradient id="gradStructured" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#1E293B"/>
                    <stop offset="100%" stop-color="#0F172A"/>
                  </linearGradient>
                  <linearGradient id="gradTransform" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#2D1F47"/>
                    <stop offset="100%" stop-color="#171126"/>
                  </linearGradient>
                  <linearGradient id="gradGraph" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#14213D"/>
                    <stop offset="100%" stop-color="#090E17"/>
                  </linearGradient>
                </defs>

                <!-- ================= ZONE 1: RAW MULTI-SOURCE INGESTION ================= -->
                <!-- Zone 1A: Structured Feeds -->
                <g id="svgZoneStructured" class="aml-zone" opacity="1">
                  <rect x="20" y="25" width="225" height="245" rx="8" fill="url(#gradStructured)" stroke="#334155" stroke-width="1.5"/>
                  <text x="32" y="46" fill="#60A5FA" font-size="12" font-weight="700">1A. Structured Banking Feeds</text>
                  <text x="32" y="60" fill="#94A3B8" font-size="9.5">Relational SQL & SWIFT Message Queues</text>

                  <!-- Table 1: KYC -->
                  <g class="aml-node" onclick="inspectAmlElement('tbl_kyc')">
                    <rect x="30" y="70" width="205" height="42" rx="5" fill="#1E293B" stroke="#475569" stroke-width="1"/>
                    <text x="38" y="86" fill="#F8FAFC" font-size="10" font-weight="700">KYC_CUSTOMER_REGISTRY</text>
                    <text x="38" y="100" fill="#CBD5E1" font-size="9" font-family="monospace">cust_id:C-901 · <tspan fill="#FF9F0A" font-weight="700">tax_id:99-887711</tspan></text>
                  </g>

                  <!-- Table 2: Accounts -->
                  <g class="aml-node" onclick="inspectAmlElement('tbl_accounts')">
                    <rect x="30" y="118" width="205" height="42" rx="5" fill="#1E293B" stroke="#475569" stroke-width="1"/>
                    <text x="38" y="134" fill="#F8FAFC" font-size="10" font-weight="700">CORE_BANKING_ACCOUNTS</text>
                    <text x="38" y="148" fill="#CBD5E1" font-size="9" font-family="monospace">cust_id:C-901 · <tspan fill="#60A5FA" font-weight="700">iban:DE89370001</tspan></text>
                  </g>

                  <!-- Table 3: SWIFT Wires -->
                  <g class="aml-node" onclick="inspectAmlElement('tbl_wires')">
                    <rect x="30" y="166" width="205" height="44" rx="5" fill="#1E293B" stroke="#475569" stroke-width="1"/>
                    <text x="38" y="182" fill="#F8FAFC" font-size="10" font-weight="700">SWIFT_MT103_WIRES</text>
                    <text x="38" y="196" fill="#CBD5E1" font-size="8.5" font-family="monospace">from:DE89... ➔ to:CH93... ($4.5M)</text>
                    <text x="38" y="206" fill="#94A3B8" font-size="8" font-family="monospace">Tx: W-8821 · 2026-09-12 09:14</text>
                  </g>

                  <!-- Table 4: OFAC -->
                  <g class="aml-node" onclick="inspectAmlElement('tbl_ofac')">
                    <rect x="30" y="216" width="205" height="44" rx="5" fill="#1E293B" stroke="#475569" stroke-width="1"/>
                    <text x="38" y="232" fill="#F43F5E" font-size="10" font-weight="700">OFAC_SANCTIONS_LIST</text>
                    <text x="38" y="246" fill="#CBD5E1" font-size="9" font-family="monospace"><tspan fill="#FF9F0A" font-weight="700">tax_id:99-887711</tspan> · SDNTK Flag</text>
                  </g>
                </g>

                <!-- Zone 1B: Unstructured Documents -->
                <g id="svgZoneUnstructured" class="aml-zone" opacity="1">
                  <rect x="20" y="285" width="225" height="255" rx="8" fill="url(#gradStructured)" stroke="#334155" stroke-width="1.5"/>
                  <text x="32" y="306" fill="#3DDC97" font-size="12" font-weight="700">1B. Unstructured Compliance Docs</text>
                  <text x="32" y="320" fill="#94A3B8" font-size="9.5">Narrative PDFs, Loan Apps & Email Alerts</text>

                  <!-- Doc 1: SAR -->
                  <g class="aml-node" onclick="inspectAmlElement('doc_sar')">
                    <rect x="30" y="330" width="205" height="58" rx="5" fill="#132E22" stroke="#1FB16D" stroke-width="1"/>
                    <text x="38" y="346" fill="#3DDC97" font-size="10" font-weight="700">📄 FinCEN SAR-2026-09.pdf</text>
                    <text x="38" y="360" fill="#E2E8F0" font-size="8.5">"Suspect Acme Shell wired $4.5M..."</text>
                    <text x="38" y="372" fill="#94A3B8" font-size="8" font-family="monospace">Mentions: Tax ID 99-887711</text>
                    <text x="38" y="382" fill="#60A5FA" font-size="7.5" font-family="monospace">ChromaDB Embedding: [0.12, -0.45, ...]</text>
                  </g>

                  <!-- Doc 2: Loan App -->
                  <g class="aml-node" onclick="inspectAmlElement('doc_loan')">
                    <rect x="30" y="396" width="205" height="58" rx="5" fill="#132E22" stroke="#1FB16D" stroke-width="1"/>
                    <text x="38" y="412" fill="#3DDC97" font-size="10" font-weight="700">📑 Commercial LoanApp-410.pdf</text>
                    <text x="38" y="426" fill="#E2E8F0" font-size="8.5">"Borrower: Acme Shell Corp"</text>
                    <text x="38" y="438" fill="#FF9F0A" font-size="8" font-family="monospace">Beneficial Owner: John Doe · MAC 00:14</text>
                    <text x="38" y="449" fill="#94A3B8" font-size="7.5" font-family="monospace">Explicit Citation: CITES 'SAR-2026-09'</text>
                  </g>

                  <!-- Doc 3: Email -->
                  <g class="aml-node" onclick="inspectAmlElement('doc_email')">
                    <rect x="30" y="462" width="205" height="66" rx="5" fill="#132E22" stroke="#1FB16D" stroke-width="1"/>
                    <text x="38" y="478" fill="#3DDC97" font-size="10" font-weight="700">✉️ Compliance Email-Thread-88</text>
                    <text x="38" y="492" fill="#E2E8F0" font-size="8.5">"Swiss & Cyprus accounts operated"</text>
                    <text x="38" y="504" fill="#A855F7" font-size="8" font-family="monospace">Shared IP: 192.168.1.50</text>
                    <text x="38" y="518" fill="#3DDC97" font-size="7.5">Cosine Sim > 0.82 to SAR-09</text>
                  </g>
                </g>

                <!-- ================= ZONE 2: TRANSFORMATION & KEY BINDING ================= -->
                <g id="svgZoneTransform" class="aml-zone" opacity="1">
                  <rect x="260" y="285" width="200" height="255" rx="8" fill="url(#gradTransform)" stroke="#6D28D9" stroke-width="1.5"/>
                  <text x="272" y="306" fill="#A855F7" font-size="12" font-weight="700">2. Transformation Pipeline</text>
                  <text x="272" y="320" fill="#94A3B8" font-size="9.5">Unstructured ➔ Canonical Schema</text>

                  <!-- Stage A: Regex -->
                  <g class="aml-node" onclick="inspectAmlElement('step_regex')">
                    <rect x="270" y="330" width="180" height="42" rx="5" fill="#2E1065" stroke="#7C3AED" stroke-width="1"/>
                    <text x="278" y="346" fill="#DDD6FE" font-size="9.5" font-weight="700">A. Regex & Checksum Valid.</text>
                    <text x="278" y="360" fill="#A78BFA" font-size="8.5" font-family="monospace">IBAN ISO 7064 Mod-97 ✓</text>
                  </g>

                  <!-- Stage B: spaCy -->
                  <g class="aml-node" onclick="inspectAmlElement('step_spacy')">
                    <rect x="270" y="378" width="180" height="42" rx="5" fill="#2E1065" stroke="#7C3AED" stroke-width="1"/>
                    <text x="278" y="394" fill="#DDD6FE" font-size="9.5" font-weight="700">B. spaCy 3.7 Linguistic NER</text>
                    <text x="278" y="408" fill="#A78BFA" font-size="8.5" font-family="monospace">PERSON · ORG · MONEY · GPE</text>
                  </g>

                  <!-- Stage C: LLM JSON -->
                  <g class="aml-node" onclick="inspectAmlElement('step_llm_json')">
                    <rect x="270" y="426" width="180" height="46" rx="5" fill="#2E1065" stroke="#7C3AED" stroke-width="1"/>
                    <text x="278" y="442" fill="#DDD6FE" font-size="9.5" font-weight="700">C. LLM Structured Extractor</text>
                    <text x="278" y="456" fill="#3DDC97" font-size="8" font-family="monospace">Pydantic JSON Schema Validation</text>
                    <text x="278" y="466" fill="#94A3B8" font-size="7.5" font-family="monospace">Model: gpt-4o-mini (temp=0.0)</text>
                  </g>

                  <!-- Canonical Key Output -->
                  <g class="aml-node" onclick="inspectAmlElement('canonical_keys')">
                    <rect x="270" y="478" width="180" height="52" rx="5" fill="#3B0764" stroke="#FF9F0A" stroke-width="1.5" stroke-dasharray="4,2"/>
                    <text x="278" y="494" fill="#FF9F0A" font-size="9.5" font-weight="700">🔑 Canonical Mapping Keys</text>
                    <text x="278" y="508" fill="#F8FAFC" font-size="8" font-family="monospace">Tax_ID: "99-887711"</text>
                    <text x="278" y="520" fill="#60A5FA" font-size="8" font-family="monospace">IBAN: "DE89370001" · MAC: "00:14..."</text>
                  </g>
                </g>

                <!-- ================= ZONE 3: 5 TOOLS ARCHITECTURE TOWER ================= -->
                <g id="svgZoneTools" class="aml-zone" opacity="1">
                  <rect x="260" y="25" width="530" height="85" rx="8" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
                  <text x="272" y="44" fill="#38BDF8" font-size="12" font-weight="700">3. Five Core Enterprise Tools & System Roles</text>
                  <text x="272" y="58" fill="#94A3B8" font-size="9.5">How each tool contributes to build, govern, vectorize, and traverse the Knowledge Graph</text>

                  <!-- Tool 1: Protégé -->
                  <g class="aml-node" onclick="inspectAmlElement('tool_protege')">
                    <rect x="270" y="66" width="98" height="36" rx="4" fill="#1E293B" stroke="#FF9F0A" stroke-width="1"/>
                    <text x="276" y="80" fill="#FF9F0A" font-size="9" font-weight="700">Protégé OWL 2</text>
                    <text x="276" y="93" fill="#CBD5E1" font-size="7.5">Schema Law</text>
                  </g>

                  <!-- Tool 2: ChromaDB -->
                  <g class="aml-node" onclick="inspectAmlElement('tool_chroma')">
                    <rect x="374" y="66" width="98" height="36" rx="4" fill="#1E293B" stroke="#A855F7" stroke-width="1"/>
                    <text x="380" y="80" fill="#A855F7" font-size="9" font-weight="700">ChromaDB</text>
                    <text x="380" y="93" fill="#CBD5E1" font-size="7.5">Dense Vectors</text>
                  </g>

                  <!-- Tool 3: Neo4j -->
                  <g class="aml-node" onclick="inspectAmlElement('tool_neo4j')">
                    <rect x="478" y="66" width="98" height="36" rx="4" fill="#1E293B" stroke="#60A5FA" stroke-width="1"/>
                    <text x="484" y="80" fill="#60A5FA" font-size="9" font-weight="700">Neo4j DB</text>
                    <text x="484" y="93" fill="#CBD5E1" font-size="7.5">Property Graph</text>
                  </g>

                  <!-- Tool 4: Cypher -->
                  <g class="aml-node" onclick="inspectAmlElement('tool_cypher')">
                    <rect x="582" y="66" width="98" height="36" rx="4" fill="#1E293B" stroke="#3DDC97" stroke-width="1"/>
                    <text x="588" y="80" fill="#3DDC97" font-size="9" font-weight="700">Cypher Engine</text>
                    <text x="588" y="93" fill="#CBD5E1" font-size="7.5">Pattern Match</text>
                  </g>

                  <!-- Tool 5: Graph-RAG -->
                  <g class="aml-node" onclick="inspectAmlElement('tool_graphrag')">
                    <rect x="686" y="66" width="98" height="36" rx="4" fill="#1E293B" stroke="#F43F5E" stroke-width="1"/>
                    <text x="692" y="80" fill="#F43F5E" font-size="9" font-weight="700">Hybrid Graph-RAG</text>
                    <text x="692" y="93" fill="#CBD5E1" font-size="7.5">Dual Synthesis</text>
                  </g>
                </g>

                <!-- ================= ZONE 4: NEO4J TOPOLOGY (AML SUBGRAPH) ================= -->
                <g id="svgZoneTopology" class="aml-zone" opacity="1">
                  <rect x="480" y="125" width="370" height="415" rx="8" fill="url(#gradGraph)" stroke="#334155" stroke-width="1.5"/>
                  <text x="492" y="146" fill="#F8FAFC" font-size="12" font-weight="700">4. Joined Neo4j AML Knowledge Graph</text>
                  <text x="492" y="160" fill="#94A3B8" font-size="9.5">Index-Free Adjacency · Multi-Modal Nodes & Directed Relationships</text>

                  <!-- ================= RELATIONSHIP EDGES ================= -->
                  <!-- Edge 1: OWNS (Customer John Doe -> Account DE) -->
                  <path id="edgeOwns" class="aml-edge aml-flowing-edge" d="M 590 205 L 670 205" stroke="#FF9F0A" stroke-width="2" marker-end="url(#arrowAmber)" onclick="inspectAmlElement('edge_owns')"/>
                  <text x="618" y="198" fill="#FF9F0A" font-size="8.5" font-weight="700">OWNS</text>

                  <!-- Edge 2: TRANSFERRED Leg 1 (DE -> CH) -->
                  <path id="edgeWire1" class="aml-edge aml-flowing-edge" d="M 725 210 Q 770 190 780 230" fill="none" stroke="#60A5FA" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrowBlue)" onclick="inspectAmlElement('edge_wire1')"/>
                  <text x="735" y="195" fill="#60A5FA" font-size="8" font-weight="700">TRANSFERRED ($4.5M)</text>

                  <!-- Edge 3: TRANSFERRED Leg 2 (CH -> CY) -->
                  <path id="edgeWire2" class="aml-edge aml-flowing-edge" d="M 800 270 Q 810 320 760 345" fill="none" stroke="#60A5FA" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#arrowBlue)" onclick="inspectAmlElement('edge_wire2')"/>
                  <text x="795" y="315" fill="#60A5FA" font-size="8" font-weight="700">$4.48M</text>

                  <!-- Edge 4: TRANSFERRED Leg 3 (CY -> DE - THE CIRCULAR CYCLE!) -->
                  <path id="edgeWire3" class="aml-edge aml-flowing-edge" d="M 720 345 Q 675 300 690 240" fill="none" stroke="#F43F5E" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrowRed)" onclick="inspectAmlElement('edge_wire3')"/>
                  <text x="660" y="300" fill="#F43F5E" font-size="8.5" font-weight="800">CIRCULAR RETURN ($4.46M)</text>

                  <!-- Edge 5: EVIDENCE_FOR (SAR Chunk -> Account DE) [KEY BINDING!] -->
                  <path id="edgeEvidence" class="aml-edge aml-flowing-edge" d="M 545 285 Q 620 260 675 225" fill="none" stroke="#3DDC97" stroke-width="2.5" stroke-dasharray="4,3" marker-end="url(#arrowEmerald)" onclick="inspectAmlElement('edge_evidence')"/>
                  <text x="560" y="255" fill="#3DDC97" font-size="8.5" font-weight="700">EVIDENCE_FOR (Key Bind)</text>

                  <!-- Edge 6: MENTIONS (Loan Chunk -> Acme Shell) -->
                  <path id="edgeMentions" class="aml-edge" d="M 545 375 L 565 375" stroke="#3DDC97" stroke-width="2" marker-end="url(#arrowEmerald)" onclick="inspectAmlElement('edge_mentions')"/>
                  <text x="530" y="370" fill="#3DDC97" font-size="8">MENTIONS</text>

                  <!-- Edge 7: SIMILAR_TOPIC (ChromaDB Cosine Similarity Between Chunks) -->
                  <path id="edgeVectorSim" class="aml-edge" d="M 515 315 L 515 350" stroke="#A855F7" stroke-width="2" stroke-dasharray="3,3" onclick="inspectAmlElement('edge_vector_sim')"/>
                  <text x="445" y="338" fill="#A855F7" font-size="7.5">SIMILAR_TOPIC (cos=0.89)</text>

                  <!-- Edge 8: BENEFICIAL_OWNER (John Doe -> Acme Shell) -->
                  <path id="edgeBenOwner" class="aml-edge" d="M 550 225 L 575 350" stroke="#FF9F0A" stroke-width="1.8" marker-end="url(#arrowAmber)" onclick="inspectAmlElement('edge_ben_owner')"/>
                  <text x="555" y="280" fill="#FF9F0A" font-size="8">BENEFICIAL_OWNER</text>

                  <!-- Edge 9: OPERATES_FROM (Acme Shell -> Device) -->
                  <path id="edgeDevice1" class="aml-edge" d="M 605 385 L 640 445" stroke="#A855F7" stroke-width="1.8" marker-end="url(#arrowPurple)" onclick="inspectAmlElement('edge_device1')"/>
                  <text x="618" y="415" fill="#A855F7" font-size="7.5">OPERATES_FROM</text>

                  <!-- Edge 10: OPERATES_FROM (John Doe -> Device) -->
                  <path id="edgeDevice2" class="aml-edge" d="M 545 225 Q 560 400 640 460" fill="none" stroke="#A855F7" stroke-width="1.8" stroke-dasharray="4,2" marker-end="url(#arrowPurple)" onclick="inspectAmlElement('edge_device2')"/>
                  <text x="565" y="445" fill="#A855F7" font-size="7.5">OPERATES_FROM</text>

                  <!-- ================= GRAPH NODES ================= -->
                  <!-- Node 1: Customer John Doe -->
                  <g id="nodeCustJohn" class="aml-node" onclick="inspectAmlElement('node_cust_john')">
                    <circle cx="550" cy="205" r="26" fill="#1E293B" stroke="#FF9F0A" stroke-width="2.5"/>
                    <text x="550" y="202" fill="#FF9F0A" font-size="8.5" font-weight="700" text-anchor="middle">Customer</text>
                    <text x="550" y="214" fill="#F8FAFC" font-size="8" text-anchor="middle">John Doe</text>
                    <circle cx="568" cy="186" r="6" fill="#F43F5E"/>
                    <text x="568" y="189" fill="#FFF" font-size="6.5" font-weight="800" text-anchor="middle">!</text>
                  </g>

                  <!-- Node 2: Account DE -->
                  <g id="nodeAccDE" class="aml-node" onclick="inspectAmlElement('node_acc_de')">
                    <circle cx="698" cy="205" r="28" fill="#1E293B" stroke="#60A5FA" stroke-width="2.5"/>
                    <text x="698" y="200" fill="#60A5FA" font-size="8.5" font-weight="700" text-anchor="middle">Account</text>
                    <text x="698" y="211" fill="#F8FAFC" font-size="7.5" font-family="monospace" text-anchor="middle">DE8937...</text>
                    <text x="698" y="221" fill="#94A3B8" font-size="6.5" text-anchor="middle">Germany</text>
                  </g>

                  <!-- Node 3: Account CH -->
                  <g id="nodeAccCH" class="aml-node" onclick="inspectAmlElement('node_acc_ch')">
                    <circle cx="798" cy="245" r="26" fill="#1E293B" stroke="#60A5FA" stroke-width="2.5"/>
                    <text x="798" y="240" fill="#60A5FA" font-size="8.5" font-weight="700" text-anchor="middle">Account</text>
                    <text x="798" y="251" fill="#F8FAFC" font-size="7.5" font-family="monospace" text-anchor="middle">CH9300...</text>
                    <text x="798" y="261" fill="#94A3B8" font-size="6.5" text-anchor="middle">Swiss Shell</text>
                  </g>

                  <!-- Node 4: Account CY -->
                  <g id="nodeAccCY" class="aml-node" onclick="inspectAmlElement('node_acc_cy')">
                    <circle cx="740" cy="365" r="26" fill="#1E293B" stroke="#60A5FA" stroke-width="2.5"/>
                    <text x="740" y="360" fill="#60A5FA" font-size="8.5" font-weight="700" text-anchor="middle">Account</text>
                    <text x="740" y="371" fill="#F8FAFC" font-size="7.5" font-family="monospace" text-anchor="middle">CY1200...</text>
                    <text x="740" y="381" fill="#94A3B8" font-size="6.5" text-anchor="middle">Cyprus Shell</text>
                  </g>

                  <!-- Node 5: Customer Acme Shell Corp -->
                  <g id="nodeCustAcme" class="aml-node" onclick="inspectAmlElement('node_cust_acme')">
                    <circle cx="585" cy="370" r="26" fill="#1E293B" stroke="#FF9F0A" stroke-width="2.5"/>
                    <text x="585" y="365" fill="#FF9F0A" font-size="8.5" font-weight="700" text-anchor="middle">Customer</text>
                    <text x="585" y="376" fill="#F8FAFC" font-size="7.5" text-anchor="middle">Acme Shell</text>
                    <text x="585" y="386" fill="#94A3B8" font-size="6.5" text-anchor="middle">Front Co</text>
                  </g>

                  <!-- Node 6: Shared Device Fraud Hub -->
                  <g id="nodeDevice" class="aml-node" onclick="inspectAmlElement('node_device')">
                    <circle cx="660" cy="470" r="24" fill="#1E293B" stroke="#A855F7" stroke-width="2.5"/>
                    <text x="660" y="465" fill="#A855F7" font-size="8" font-weight="700" text-anchor="middle">Device Hub</text>
                    <text x="660" y="476" fill="#F8FAFC" font-size="7" font-family="monospace" text-anchor="middle">00:14:22:A9</text>
                    <text x="660" y="485" fill="#A855F7" font-size="6.5" text-anchor="middle">Shared MAC</text>
                  </g>

                  <!-- Node 7: Unstructured SAR Chunk Node -->
                  <g id="nodeChunkSAR" class="aml-node" onclick="inspectAmlElement('node_chunk_sar')">
                    <rect x="495" y="275" width="55" height="38" rx="4" fill="#132E22" stroke="#3DDC97" stroke-width="2"/>
                    <text x="522" y="291" fill="#3DDC97" font-size="8" font-weight="700" text-anchor="middle">Chunk #4</text>
                    <text x="522" y="303" fill="#E2E8F0" font-size="7" text-anchor="middle">SAR-09</text>
                  </g>

                  <!-- Node 8: Unstructured Loan Chunk Node -->
                  <g id="nodeChunkLoan" class="aml-node" onclick="inspectAmlElement('node_chunk_loan')">
                    <rect x="495" y="355" width="55" height="38" rx="4" fill="#132E22" stroke="#3DDC97" stroke-width="2"/>
                    <text x="522" y="371" fill="#3DDC97" font-size="8" font-weight="700" text-anchor="middle">Chunk #2</text>
                    <text x="522" y="383" fill="#E2E8F0" font-size="7" text-anchor="middle">LoanApp</text>
                  </g>
                </g>

                <!-- ================= ZONE 5: PATTERN RECOGNITION & OUTPUT ================= -->
                <g id="svgZoneOutputs" class="aml-zone" opacity="1">
                  <rect x="865" y="25" width="265" height="515" rx="8" fill="url(#gradStructured)" stroke="#334155" stroke-width="1.5"/>
                  <text x="878" y="46" fill="#F43F5E" font-size="12" font-weight="700">5. Pattern Detection & Deliverable</text>
                  <text x="878" y="60" fill="#94A3B8" font-size="9.5">Cypher Motifs & Regulatory SAR Package</text>

                  <!-- Pattern 1: Circular Ring Detection -->
                  <g class="aml-node" onclick="inspectAmlElement('pattern_ring')">
                    <rect x="875" y="72" width="245" height="74" rx="6" fill="#3B0D18" stroke="#F43F5E" stroke-width="1.5"/>
                    <text x="885" y="90" fill="#F43F5E" font-size="10.5" font-weight="800">🚨 3-Hop Wire Layering Ring</text>
                    <text x="885" y="105" fill="#E2E8F0" font-size="8.5">DE8937... ➔ CH9300... ➔ CY1200... ➔ DE8937...</text>
                    <text x="885" y="118" fill="#FF9F0A" font-size="8" font-family="monospace">Cypher: (a)-[:TRANSFERRED*3..6]->(a)</text>
                    <text x="885" y="130" fill="#94A3B8" font-size="8">Elapsed Time: 25.8 hrs (Obvious Structuring)</text>
                  </g>

                  <!-- Pattern 2: Mule Device Hub -->
                  <g class="aml-node" onclick="inspectAmlElement('pattern_device')">
                    <rect x="875" y="154" width="245" height="66" rx="6" fill="#24133B" stroke="#A855F7" stroke-width="1.5"/>
                    <text x="885" y="172" fill="#A855F7" font-size="10.5" font-weight="800">📱 Mule Device / IP Fraud Hub</text>
                    <text x="885" y="187" fill="#E2E8F0" font-size="8.5">2 Entities Share MAC: 00:14:22:A9:BC:11</text>
                    <text x="885" y="200" fill="#A78BFA" font-size="8" font-family="monospace">Cypher: (c1)-[:OPERATES_FROM]->(d)<-[:...]-(c2)</text>
                    <text x="885" y="211" fill="#94A3B8" font-size="8">Co-located login from Cyprus & Germany</text>
                  </g>

                  <!-- Pattern 3: PageRank Centrality -->
                  <g class="aml-node" onclick="inspectAmlElement('pattern_pagerank')">
                    <rect x="875" y="228" width="245" height="54" rx="6" fill="#1C1917" stroke="#FF9F0A" stroke-width="1"/>
                    <text x="885" y="246" fill="#FF9F0A" font-size="10" font-weight="700">👑 PageRank Kingpin Analysis</text>
                    <text x="885" y="260" fill="#E2E8F0" font-size="8.5">Ringleader: John Doe (Rank Score: 0.88)</text>
                    <text x="885" y="272" fill="#94A3B8" font-size="8">Concealed beneficial owner of 3 shell corps</text>
                  </g>

                  <!-- Executive Deliverable Summary Card -->
                  <g class="aml-node" onclick="inspectAmlElement('exec_deliverable')">
                    <rect x="875" y="292" width="245" height="236" rx="6" fill="#0F172A" stroke="#3DDC97" stroke-width="1.8"/>
                    <text x="885" y="312" fill="#3DDC97" font-size="11" font-weight="800">🎯 EXECUTIVE DELIVERABLES</text>
                    
                    <text x="885" y="332" fill="#94A3B8" font-size="8.5" font-weight="700">QUANTIFIED MONEY LAUNDERING:</text>
                    <text x="885" y="352" fill="#F43F5E" font-size="18" font-weight="800">$14,250,000.00</text>
                    <text x="885" y="366" fill="#94A3B8" font-size="8">Across 3 Layering Rings (14 Accts, 4 Jurisdictions)</text>

                    <line x1="885" y1="376" x2="1105" y2="376" stroke="#334155" stroke-width="1"/>

                    <text x="885" y="394" fill="#94A3B8" font-size="8.5" font-weight="700">UNMASKED BAD ACTORS & ENTITIES:</text>
                    <text x="885" y="408" fill="#F8FAFC" font-size="9" font-weight="700">• John Doe (Beneficial Owner / Sanctioned)</text>
                    <text x="885" y="420" fill="#F8FAFC" font-size="9">• Acme Shell Corp (Cyprus Front Co)</text>
                    <text x="885" y="432" fill="#F8FAFC" font-size="9">• Alpine Asset Holdco (Swiss Shell)</text>

                    <line x1="885" y1="442" x2="1105" y2="442" stroke="#334155" stroke-width="1"/>

                    <text x="885" y="460" fill="#3DDC97" font-size="8.5" font-weight="700">1-CLICK REGULATORY SAR FILING:</text>
                    <rect x="885" y="470" width="225" height="46" rx="4" fill="#132E22" stroke="#1FB16D" stroke-width="1"/>
                    <text x="895" y="488" fill="#3DDC97" font-size="9" font-weight="700">FinCEN Form 111 Pre-Populated</text>
                    <text x="895" y="502" fill="#E2E8F0" font-size="8">100% Cryptographic Subgraph Audit Trail Attached</text>
                  </g>
                </g>

              </svg>
            </div>

            <!-- ================= DYNAMIC STEP DEEP-DIVE CARD ================= -->
            <div style="margin-top:24px;">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span id="amlCurrentStageBadge" class="aml-badge amber">STAGE 1 DEEP-DIVE</span>
                  <h3 id="amlCurrentStageTitle" style="color:var(--tx-0); font-size:17px; margin:0; font-weight:700;">
                    Multi-Source Structured Data Mapping via Relational Keys
                  </h3>
                </div>
                <!-- Sub-Tabs for this Stage -->
                <div style="display:flex; gap:6px; background:var(--bg-2); border:1px solid var(--line); border-radius:6px; padding:3px;">
                  <button type="button" class="aml-tab-pill active" id="amlSubTabBtn-talk" onclick="setAmlSubTab('talk')">🎙️ Panel Talk-Track</button>
                  <button type="button" class="aml-tab-pill" id="amlSubTabBtn-mechanics" onclick="setAmlSubTab('mechanics')">⚙️ Joining & Creation</button>
                  <button type="button" class="aml-tab-pill" id="amlSubTabBtn-tools" onclick="setAmlSubTab('tools')">🛠️ Tool Contribution</button>
                  <button type="button" class="aml-tab-pill" id="amlSubTabBtn-qa" onclick="setAmlSubTab('qa')">❓ Panel Defense Q&A</button>
                </div>
              </div>

              <!-- Content Panes for Sub-Tabs -->
              <div id="amlSubContent-talk" class="aml-card-box" style="display:block;">
                <!-- Filled dynamically by JS -->
              </div>
              <div id="amlSubContent-mechanics" class="aml-card-box" style="display:none;">
                <!-- Filled dynamically by JS -->
              </div>
              <div id="amlSubContent-tools" class="aml-card-box" style="display:none;">
                <!-- Filled dynamically by JS -->
              </div>
              <div id="amlSubContent-qa" class="aml-card-box" style="display:none;">
                <!-- Filled dynamically by JS -->
              </div>
            </div>

            <!-- ================= LIVE INSPECTOR DRAWER / MODAL ================= -->
            <div id="amlInspectorBox" style="display:none; background:#121A29; border:1.5px solid var(--amber); border-radius:10px; padding:18px; margin-top:20px; box-shadow:0 8px 30px rgba(0,0,0,0.5);">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                <div>
                  <span id="amlInspBadge" class="aml-badge amber">NODE INSPECTOR</span>
                  <h4 id="amlInspTitle" style="color:var(--tx-0); font-size:16px; margin:4px 0 0; font-weight:700;">Element Details</h4>
                </div>
                <button type="button" onclick="closeAmlInspector()" style="background:transparent; border:none; color:var(--tx-2); font-size:18px; cursor:pointer;">✕</button>
              </div>
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px;">
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:6px; padding:12px;">
                  <strong style="color:var(--amber); font-size:11px; display:block; margin-bottom:6px;">PROPERTIES & VALUES</strong>
                  <pre id="amlInspProps" style="color:var(--tx-1); font-size:11px; margin:0; font-family:var(--mono); white-space:pre-wrap;"></pre>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:6px; padding:12px;">
                  <strong style="color:#60A5FA; font-size:11px; display:block; margin-bottom:6px;">PROVENANCE & ORIGIN DATA SOURCE</strong>
                  <div id="amlInspSource" style="color:var(--tx-1); font-size:11.5px; line-height:1.5;"></div>
                  <strong style="color:#3DDC97; font-size:11px; display:block; margin:8px 0 4px;">PROTÉGÉ OWL 2 SEMANTIC CONSTRAINT</strong>
                  <div id="amlInspProtege" style="color:var(--tx-2); font-size:11px; font-family:var(--mono);"></div>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:6px; padding:12px;">
                  <strong style="color:#A855F7; font-size:11px; display:block; margin-bottom:6px;">EXACT CYPHER STATEMENT</strong>
                  <pre id="amlInspCypher" style="color:var(--tx-1); font-size:10.5px; margin:0; font-family:var(--mono); background:#0D111A; padding:8px; border-radius:4px; overflow-x:auto;"></pre>
                </div>
              </div>
            </div>

            <!-- ================= INTERVIEW DEFENSE MASTER MATRIX CHEAT SHEET ================= -->
            <div style="margin-top:28px;">
              <h4 style="color:var(--tx-0); font-size:16px; margin:0 0 12px; font-weight:700;">
                📋 Interview Defense Master Matrix: 7-Stage Quick-Reference Cheat Sheet
              </h4>
              <p style="color:var(--tx-2); font-size:12.5px; margin:0 0 14px;">
                Keep this reference in mind when defending the architecture to technical leads and executive interviewers:
              </p>
              
              <div style="overflow-x:auto; background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px;">
                <table style="width:100%; border-collapse:collapse; font-size:12px; text-align:left; color:var(--tx-1);">
                  <thead>
                    <tr style="background:var(--surface); border-bottom:1.5px solid var(--line-strong); color:var(--tx-0);">
                      <th style="padding:10px 12px; font-weight:700; width:60px;">Stage</th>
                      <th style="padding:10px 12px; font-weight:700; width:160px;">Name</th>
                      <th style="padding:10px 12px; font-weight:700; width:160px;">Input Data Streams</th>
                      <th style="padding:10px 12px; font-weight:700; width:150px;">Primary Mapping Keys</th>
                      <th style="padding:10px 12px; font-weight:700; width:170px;">Transformation / Joins</th>
                      <th style="padding:10px 12px; font-weight:700; width:120px;">Tool Role</th>
                      <th style="padding:10px 12px; font-weight:700;">Panel 1-Liner Spoken Defense</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr style="border-bottom:1px solid var(--line-soft);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">1</td>
                      <td style="padding:10px 12px; font-weight:700;">Structured Joins</td>
                      <td style="padding:10px 12px;">Core Banking SQL, SWIFT Wires, KYC Master, OFAC</td>
                      <td style="padding:10px 12px;"><code style="color:var(--amber);">cust_id</code>, <code style="color:#60A5FA;">iban</code>, <code style="color:#3DDC97;">tax_id</code></td>
                      <td style="padding:10px 12px;">Primary/Foreign keys mapped to directed graph edges</td>
                      <td style="padding:10px 12px;"><span class="aml-badge blue">Neo4j</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"Instead of recursive SQL joins that blow up temp memory, foreign keys become O(1) physical pointers."</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--line-soft); background:rgba(255,255,255,0.02);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">2</td>
                      <td style="padding:10px 12px; font-weight:700;">Unstructured Mapping</td>
                      <td style="padding:10px 12px;">SAR Narratives, Loan Application PDFs, Compliance Emails</td>
                      <td style="padding:10px 12px;">Extracted entities, Case IDs, Vector similarity</td>
                      <td style="padding:10px 12px;">Co-occurrence bridges, citation regex, ChromaDB cosine &gt; 0.82</td>
                      <td style="padding:10px 12px;"><span class="aml-badge purple">ChromaDB</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"Unstructured documents link to each other via shared mentioned entities, case citations, and vector distance."</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--line-soft);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">3</td>
                      <td style="padding:10px 12px; font-weight:700;">Data Transformation</td>
                      <td style="padding:10px 12px;">Raw text paragraphs, OCR scans, free-text email bodies</td>
                      <td style="padding:10px 12px;">Target canonical schema fields (IBAN, SSN, BIC, MAC)</td>
                      <td style="padding:10px 12px;">Deterministic regex (Mod-97) + spaCy NER + LLM JSON Pydantic</td>
                      <td style="padding:10px 12px;"><span class="aml-badge emerald">spaCy + LLM</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"You can't join raw prose with database keys; our 3-tier pipeline distills noisy text into guaranteed Pydantic JSON."</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--line-soft); background:rgba(255,255,255,0.02);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">4</td>
                      <td style="padding:10px 12px; font-weight:700;">Key Binding Engine</td>
                      <td style="padding:10px 12px;">Extracted JSON payloads & existing Neo4j structured nodes</td>
                      <td style="padding:10px 12px;"><code style="color:#60A5FA;">extracted_iban</code>, <code style="color:var(--amber);">tax_id</code></td>
                      <td style="padding:10px 12px;">Cypher MERGE anchors Chunk node to Account node via <code style="color:#3DDC97;">[:EVIDENCE_FOR]</code></td>
                      <td style="padding:10px 12px;"><span class="aml-badge blue">Cypher</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"Key binding is where text meets data: Cypher glues document chunks directly to accounts as evidentiary edges."</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--line-soft);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">5</td>
                      <td style="padding:10px 12px; font-weight:700;">5 Core Tool Roles</td>
                      <td style="padding:10px 12px;">Ontology OWL, Vector store, Graph database, Query engine, LLM</td>
                      <td style="padding:10px 12px;">Formal classes, Embeddings, Nodes, Paths, Context</td>
                      <td style="padding:10px 12px;">Protégé governs schema law; ChromaDB vectors; Neo4j stores; Cypher traverses; RAG fuses</td>
                      <td style="padding:10px 12px;"><span class="aml-badge amber">Full Stack</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"Each tool has zero overlap: Protégé is the constitutional law, ChromaDB the fuzzy memory, Neo4j the physical brain."</td>
                    </tr>
                    <tr style="border-bottom:1px solid var(--line-soft); background:rgba(255,255,255,0.02);">
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">6</td>
                      <td style="padding:10px 12px; font-weight:700;">Pattern Recognition</td>
                      <td style="padding:10px 12px;">Multi-hop transaction paths, device logs, entity ownership</td>
                      <td style="padding:10px 12px;">Graph topology motifs (cycles, shared hubs, PageRank)</td>
                      <td style="padding:10px 12px;">Variable-length path queries: <code style="color:#F43F5E;">(a)-[:TRANSFERRED*3..6]->(a)</code></td>
                      <td style="padding:10px 12px;"><span class="aml-badge rose">Cypher GDS</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"Criminals hide in multi-hop circular loops; Cypher finds these cycles in milliseconds without arbitrary SQL joins."</td>
                    </tr>
                    <tr>
                      <td style="padding:10px 12px; font-weight:700; color:var(--amber);">7</td>
                      <td style="padding:10px 12px; font-weight:700;">Executive Deliverables</td>
                      <td style="padding:10px 12px;">Detected subgraph, transaction sums, unmasked shell entities</td>
                      <td style="padding:10px 12px;">$14.25M quantified sum, FinCEN Form 111 XML payload</td>
                      <td style="padding:10px 12px;">Hybrid Graph-RAG synthesizes auditable executive compliance brief</td>
                      <td style="padding:10px 12px;"><span class="aml-badge emerald">Graph-RAG</span></td>
                      <td style="padding:10px 12px; color:var(--tx-0);">"We don't give management fuzzy summaries; we give them $14.25M in detected exposure and a 1-click filed SAR."</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>


              <!-- MODAL FOOTER CONTROLS -->
              <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #1E293B; padding-top:12px; margin-top:8px;">
                <div style="font-size:12px; color:var(--tx-3);">
                  Tip: Use the <kbd style="background:#1E293B; padding:2px 6px; border-radius:4px; color:#CBD5E1;">Esc</kbd> key or the top-right <strong style="color:#F43F5E;">✕</strong> cross button to close this window.
                </div>
                <div style="display:flex; gap:8px;">
                  <button type="button" class="btn btn-sm btn-secondary" onclick="prevAmlStep()">◀ Previous Stage</button>
                  <button type="button" class="btn btn-sm btn-primary" onclick="nextAmlStep()">Next Stage ▶</button>
                  <button type="button" class="btn btn-sm btn-secondary" onclick="closeAmlModal()" style="border-color:#F43F5E; color:#F43F5E;">Close Window ✕</button>
                </div>
              </div>

            </div> <!-- end #amlModalBody -->
          </div> <!-- end #amlModalCard -->
        </div> <!-- end #amlModalOverlay -->

        <!-- ==================== IN-PAGE PRESENTATION LAUNCHER CONSOLE ==================== -->
        <div id="archContent-aml-workflow" class="arch-tab-content">
          <div style="background:var(--surface); border:1.5px solid var(--amber); border-radius:14px; padding:28px; margin-bottom:24px; box-shadow:0 8px 36px rgba(255,159,10,0.22);">
            
            <!-- HEADER -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:20px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span class="aml-badge amber">⚡ INTERVIEW-READY SIMULATOR</span>
                  <span class="aml-badge blue">FINANCIAL AML & FRAUD USE CASE</span>
                  <span class="aml-badge emerald">7-STAGE INTERACTIVE WORKFLOW</span>
                  <span class="aml-badge purple">HYBRID GRAPH-RAG</span>
                </div>
                <h2 style="color:var(--tx-0); font-size:24px; margin:0 0 8px; font-weight:800; letter-spacing:-0.01em;">
                  Interactive AML Knowledge Graph Simulator: Data Unification & Pattern Recognition
                </h2>
                <p style="color:var(--tx-2); font-size:13.5px; line-height:1.6; margin:0; max-width:1050px;">
                  Comprehensive executive & technical presentation demonstrating how heterogeneous relational banking databases (Oracle KYC, Postgres Accounts, Kafka SWIFT Wires, OFAC Sanctions) and unstructured compliance documents (FinCEN SAR PDFs, Commercial Loan Memos, Email alerts) map, transform, bind into Neo4j via canonical keys, and leverage <strong>Protégé OWL 2, ChromaDB, Neo4j, Cypher & Hybrid Graph-RAG</strong> to identify a <strong>$14.25M circular laundering ring</strong>.
                </p>
              </div>
              <div style="background:rgba(255,159,10,0.1); border:1px solid rgba(255,159,10,0.35); border-radius:10px; padding:10px 18px; text-align:right;">
                <div style="font-size:11px; color:var(--amber); font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">PANEL TALK-TRACK READY</div>
                <div style="font-size:18px; font-weight:800; color:var(--tx-0);">7-Step Master Simulation</div>
              </div>
            </div>

            <!-- PRIMARY CALL-TO-ACTION LAUNCH BUTTONS -->
            <div style="background:linear-gradient(135deg, rgba(255,159,10,0.12) 0%, rgba(96,165,250,0.12) 100%); border:1.5px solid var(--amber); border-radius:12px; padding:20px 24px; margin-bottom:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px; box-shadow:0 4px 20px rgba(0,0,0,0.25);">
              <div>
                <div style="font-size:15px; font-weight:800; color:#FFFFFF; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                  <span style="font-size:20px;">🚀</span> Dedicated Full-Scale Presentation Window
                </div>
                <div style="font-size:12.5px; color:#CBD5E1; max-width:750px;">
                  Launches a full-screen, high-definition modal overlay designed specifically for executive and technical interview panels. Includes real-time auto-play animations, countdown timer, clickable SVG elements, deep-dive technical mechanics, and Cypher queries.
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <button type="button" onclick="openAmlModal(false)" class="btn btn-primary" style="font-size:14px; font-weight:800; padding:11px 24px; background:linear-gradient(135deg, #FF9F0A 0%, #EA580C 100%); border:none; box-shadow:0 0 20px rgba(255,159,10,0.5); cursor:pointer;">
                  ⤢ Open Full-Scale Window
                </button>
                <button type="button" onclick="openAmlModal(true)" class="btn btn-secondary" style="font-size:13.5px; font-weight:700; padding:11px 20px; border:1.5px solid var(--amber); color:var(--amber); background:rgba(255,159,10,0.08); cursor:pointer;">
                  ▶ Launch Auto-Play Tour Directly
                </button>
              </div>
            </div>

            <!-- 4 SUMMARY PILLARS CARDS -->
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin-bottom:24px;">
              <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:16px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:18px;">🔗</span>
                  <strong style="color:#60A5FA; font-size:13px;">1. Multi-Source Joins</strong>
                </div>
                <p style="font-size:12px; color:#94A3B8; margin:0; line-height:1.5;">
                  Maps Oracle KYC foreign keys to Postgres Accounts and Kafka SWIFT wires. Converts expensive relational joins into $O(1)$ memory pointers via Neo4j index-free adjacency.
                </p>
              </div>

              <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:16px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:18px;">📄</span>
                  <strong style="color:#3DDC97; font-size:13px;">2. Unstructured Mapping</strong>
                </div>
                <p style="font-size:12px; color:#94A3B8; margin:0; line-height:1.5;">
                  Binds FinCEN SARs and loan memos using co-occurrence entity bridges, case citations, and ChromaDB cosine similarity (&gt; 0.82) to connect documents without natural primary keys.
                </p>
              </div>

              <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:16px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:18px;">⚙️</span>
                  <strong style="color:#A855F7; font-size:13px;">3. 3-Tier Transformation</strong>
                </div>
                <p style="font-size:12px; color:#94A3B8; margin:0; line-height:1.5;">
                  Deterministic ISO 7064 Mod-97 IBAN checksums + spaCy linguistic NER + OpenAI gpt-4o-mini Pydantic JSON schemas produce clean canonical keys for Cypher MERGE binding.
                </p>
              </div>

              <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:16px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:18px;">🚨</span>
                  <strong style="color:#F43F5E; font-size:13px;">4. Circular Ring Detection</strong>
                </div>
                <p style="font-size:12px; color:#94A3B8; margin:0; line-height:1.5;">
                  Detects a 3-hop circular wire trail ($4.5M ➔ $4.48M ➔ $4.46M ➔ Origin) and shared device MAC hubs in milliseconds, culminating in a FinCEN Form 111 filing package.
                </p>
              </div>
            </div>

            <!-- STEP DIRECTORY TABLE -->
            <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:18px;">
              <h3 style="color:#F8FAFC; font-size:14px; margin:0 0 12px; font-weight:700;">
                7 Simulation Stages (Click to Launch Stage in Full-Scale Window)
              </h3>
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:10px;">
                <button type="button" onclick="openAmlModalWithStep(1)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:var(--amber); color:#000; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">1</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Structured Joins via Relational Keys</div>
                    <div style="font-size:11px; color:#94A3B8;">KYC, Accounts, SWIFT, OFAC ➔ Graph</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(2)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">2</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Unstructured Inter-Document Mapping</div>
                    <div style="font-size:11px; color:#94A3B8;">Co-occurrence, Citations, ChromaDB cosine &gt; 0.82</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(3)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">3</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Transformation Pipeline (Text ➔ Schema)</div>
                    <div style="font-size:11px; color:#94A3B8;">Mod-97 checksum, spaCy NER, LLM JSON schema</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(4)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">4</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Canonical Key Binding Engine</div>
                    <div style="font-size:11px; color:#94A3B8;">Cypher MERGE binds text chunks via [:EVIDENCE_FOR]</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(5)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">5</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">5 Core Tools & Architectural Roles</div>
                    <div style="font-size:11px; color:#94A3B8;">Protégé OWL 2, ChromaDB, Neo4j, Cypher, Graph-RAG</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(6)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">6</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Topological Pattern Recognition</div>
                    <div style="font-size:11px; color:#94A3B8;">3-Hop wire loop ($14.25M), device hub, PageRank</div>
                  </div>
                </button>
                <button type="button" onclick="openAmlModalWithStep(7)" style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 14px; text-align:left; cursor:pointer; color:#E2E8F0; display:flex; align-items:center; gap:10px; grid-column:1 / -1;">
                  <span style="background:#374151; color:#FFF; font-weight:800; border-radius:50%; width:22px; height:22px; display:inline-flex; align-items:center; justify-content:center; font-size:11px;">7</span>
                  <div>
                    <div style="font-weight:700; font-size:12.5px; color:#FFF;">Executive Leadership Deliverables & FinCEN SAR Filing</div>
                    <div style="font-size:11px; color:#94A3B8;">$14.25M quantified exposure, unmasked syndicate, FinCEN Form 111 XML, and zero-hallucination executive brief</div>
                  </div>
                </button>
              </div>
            </div>

          </div>
        </div>

    '''

print("get_aml_workflow_html prepared.")
