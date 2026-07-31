import re

with open('c:/CBRE_Ontology/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_overview = """      <div class="view active" id="view-overview" style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: calc(100vh - 100px); padding: 40px; background: transparent; position: relative;">
        
        <!-- Header area within the overview -->
        <div style="position: absolute; top: 0; left: 0; width: 100%; padding: 20px 40px; display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <h2 style="margin: 0; font-size: 24px; font-weight: 800; color: var(--emerald);">GRAPHEN</h2>
            <div style="font-size: 12px; color: var(--tx-1); margin-top: 4px; max-width: 350px; line-height: 1.4;">
              <span style="color: var(--emerald); font-weight: bold;">G</span>raph-powered <span style="color: var(--emerald); font-weight: bold;">R</span>easoning <span style="color: var(--emerald); font-weight: bold;">A</span>gentic <span style="color: var(--emerald); font-weight: bold;">P</span>latform for <span style="color: var(--emerald); font-weight: bold;">H</span>ierarchical <span style="color: var(--emerald); font-weight: bold;">E</span>nterprise <span style="color: var(--emerald); font-weight: bold;">N</span>etworks
            </div>
            <div style="font-size: 11px; color: var(--tx-3); font-style: italic; margin-top: 8px;">
              Agent-driven SDLC · a CBRE AI product
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-weight: 700; font-size: 14px; color: var(--tx-0); display: flex; align-items: center; gap: 6px; justify-content: flex-end;">
              CBRE AI Practice <div style="width: 6px; height: 6px; background: var(--emerald); border-radius: 50%;"></div>
            </div>
            <div style="font-size: 12px; color: var(--tx-2); margin-top: 2px;">Solutions Architecture</div>
          </div>
        </div>

        <!-- Center Hero -->
        <div style="text-align: center; margin-top: 80px; margin-bottom: 40px;">
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 2px; color: var(--emerald); text-transform: uppercase; margin-bottom: 16px;">
            From Unstructured Documents to a Live Knowledge Graph
          </div>
          <h1 style="font-size: 56px; font-weight: 800; color: var(--tx-0); margin: 0 0 16px 0;">
            Meet <span style="color: var(--emerald);">GRAPHEN</span>.
          </h1>
          <p style="font-size: 16px; color: var(--tx-1); max-width: 700px; margin: 0 auto 24px auto; line-height: 1.6;">
            Introducing our niche area platform tailored to serve across the top 5 industries:<br/>
            <strong>BFSI, Pharma, Manufacturing, Healthcare / Life Sciences, and Real Estate</strong>.<br/>
            Turn complex requirements into live knowledge graphs with governance at every step.
          </p>
          <button class="btn btn-outline" style="border-radius: 4px; padding: 10px 24px; font-size: 14px; color: var(--tx-1); border: 1px solid var(--bg-3); background: var(--bg-1); cursor: pointer;">
            Choose your role to begin
          </button>
        </div>

        <!-- Two Cards -->
        <div style="display: flex; gap: 24px; max-width: 1000px; width: 100%;">
          
          <!-- Left Card -->
          <div style="flex: 1; border: 2px solid var(--emerald); border-radius: 8px; background: var(--bg-1); padding: 32px; display: flex; flex-direction: column;">
            <h2 style="font-size: 28px; font-weight: 800; color: var(--emerald); margin: 0 0 8px 0;">GRAPHEN</h2>
            <div style="font-size: 14px; font-style: italic; color: var(--emerald); margin-bottom: 24px;">Graph-powered document intelligence · ingest to query</div>
            <p style="font-size: 14px; color: var(--tx-1); margin: 0 0 24px 0; line-height: 1.5;">
              Fill intake, watch agents execute, and pass gates from discovery through deploy.
            </p>
            <ul style="list-style: none; padding: 0; margin: 0 0 40px 0; font-size: 13px; color: var(--tx-1); display: flex; flex-direction: column; gap: 12px;">
              <li style="display: flex; gap: 8px;"><span style="color: var(--emerald);">→</span> Interactive step-by-step pipeline</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--emerald);">→</span> Per-agent visualization and artifacts</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--emerald);">→</span> Extensible tools (pdfplumber, spaCy, Neo4j, ChromaDB, LLMs)</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--emerald);">→</span> Telemetry consolidated in Admin</li>
            </ul>
            <div style="margin-top: auto;">
              <button class="btn" onclick="nav('dashboard')" style="width: 100%; padding: 14px; background: var(--emerald); color: #fff; font-weight: 700; font-size: 16px; border: none; border-radius: 4px; cursor: pointer;">
                Start GRAPHEN run
              </button>
            </div>
          </div>

          <!-- Right Card -->
          <div style="flex: 1; border: 2px solid var(--blue); border-radius: 8px; background: var(--bg-1); padding: 32px; display: flex; flex-direction: column;">
            <h2 style="font-size: 28px; font-weight: 800; color: var(--blue); margin: 0 0 8px 0;">Admin</h2>
            <div style="font-size: 14px; font-style: italic; color: var(--blue); margin-bottom: 24px;">Fleet-wide observation</div>
            <p style="font-size: 14px; color: var(--tx-1); margin: 0 0 24px 0; line-height: 1.5;">
              Track journeys across AI Signal Layer, Infrastructure Dashboard, and Saved Projects archive.
            </p>
            <ul style="list-style: none; padding: 0; margin: 0 0 40px 0; font-size: 13px; color: var(--tx-1); display: flex; flex-direction: column; gap: 12px;">
              <li style="display: flex; gap: 8px;"><span style="color: var(--blue);">→</span> AI Signal Layer — runs, DORA, LLM cost, gates, QA/security</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--blue);">→</span> Infrastructure Dashboard — platform + tool health</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--blue);">→</span> Saved Projects — resume any persisted GRAPHEN journey</li>
              <li style="display: flex; gap: 8px;"><span style="color: var(--blue);">→</span> Cost, security posture, delivery metrics</li>
            </ul>
            <div style="margin-top: auto;">
              <button class="btn" onclick="nav('admin')" style="width: 100%; padding: 14px; background: var(--blue); color: #fff; font-weight: 700; font-size: 16px; border: none; border-radius: 4px; cursor: pointer;">
                Open Admin dashboard
              </button>
            </div>
          </div>

        </div>
      </div>"""

# Replace the block from <div class="view active" id="view-overview"> to the end of the div before <!-- ============ INGEST ============ -->
pattern = r'<div class="view active" id="view-overview">.*?</div>\s*<!-- ============ INGEST ============ -->'
match = re.search(pattern, content, re.DOTALL)
if match:
    new_content = content[:match.start()] + new_overview + '\n\n      <!-- ============ INGEST ============ -->' + content[match.end():]
    with open('c:/CBRE_Ontology/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced successfully!")
else:
    print("Could not find the overview block to replace.")
