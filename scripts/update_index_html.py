import re

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Scale down the UI (inject CSS into the head or adjust body zoom)
    # The simplest way to "resize the overall design of the page" globally on chromium is zoom, 
    # but a better standard approach is font-size scaling. 
    # I'll just add `zoom: 0.85;` to body in CSS for a quick overall resize.
    if 'zoom: 0.85;' not in html:
        html = html.replace('body {', 'body {\n  zoom: 0.85;')

    # 2. Replace the upload actions
    old_actions = '''<div class="upload-actions">
                <button class="btn btn-orange" onclick="event.stopPropagation(); document.getElementById('multiFileInput').click()">📁 Browse Files</button>
                <button class="btn btn-secondary" onclick="event.stopPropagation(); loadSampleFiles()">⚡ Load all Files</button>
              </div>'''
    
    new_actions = '''<div class="upload-actions">
                <button class="btn btn-orange" onclick="event.stopPropagation(); document.getElementById('multiFileInput').click()">📁 Browse Files</button>
                <button class="btn btn-secondary" id="btnUploadFiles" onclick="event.stopPropagation(); uploadSelectedFiles()">📤 Upload Files</button>
              </div>
              <div id="recent-uploads" style="margin-top: 20px; text-align: left; width: 100%; display: none;">
                 <strong style="color: var(--white); margin-bottom: 8px; display: block; font-size: 14px;">Recent Uploads (Tracking IDs):</strong>
                 <div id="tracking-id-list" style="display: flex; gap: 10px; flex-wrap: wrap;"></div>
              </div>'''
    html = html.replace(old_actions, new_actions)

    # 3. Add the file preview pane just below the dataset container
    preview_pane = '''
            <div id="file-preview-pane" style="display:none; margin-top: 20px; width: 100%; height: 350px; background: var(--bg-surface); border: 1px solid var(--border); border-radius: 8px; padding: 15px; overflow-y: auto;">
               <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid var(--border); padding-bottom: 10px;">
                   <h3 id="preview-filename" style="margin:0; color: var(--emerald); font-size: 16px;">File Preview</h3>
                   <button class="btn" style="padding: 4px 10px; font-size: 12px;" onclick="document.getElementById('file-preview-pane').style.display='none'">Close</button>
               </div>
               <div id="preview-content" style="color: var(--text-secondary); white-space: pre-wrap; font-family: monospace; font-size: 13px;"></div>
            </div>
    '''
    
    # We want to insert it after the end of dataset-container
    dataset_container_end = '</div>\n            </div>\n            \n            <div class="dataset-container">'
    # Wait, it's better to just append it to the end of view-ingest content.
    # Let's find view-ingest and append at the bottom of its content.
    view_ingest_end = '<!-- ============ ASK AI ============ -->'
    html = html.replace(view_ingest_end, preview_pane + '\n' + view_ingest_end)

    # 4. Inject Javascript logic for uploads
    js_logic = '''
    let currentTrackingId = null;

    async function fetchRecentUploads() {
        try {
            const res = await fetch('/api/uploads/recent');
            if(res.ok) {
                const data = await res.json();
                const list = document.getElementById('tracking-id-list');
                const container = document.getElementById('recent-uploads');
                if(data.recent && data.recent.length > 0) {
                    container.style.display = 'block';
                    list.innerHTML = data.recent.map(r => 
                        `<span style="background: var(--bg-elevated); padding: 5px 10px; border-radius: 4px; cursor: pointer; border: 1px solid var(--border);" onclick="loadTrackingSession('${r.tracking_id}')" title="Created: ${r.created_at}">${r.tracking_id}</span>`
                    ).join('');
                }
            }
        } catch(e) {
            console.error("Failed to fetch recent uploads", e);
        }
    }

    async function uploadSelectedFiles() {
        const input = document.getElementById('multiFileInput');
        if(!input.files || input.files.length === 0) {
            alert('Please browse and select files first.');
            return;
        }
        
        const formData = new FormData();
        for(let i=0; i<input.files.length; i++) {
            formData.append('files', input.files[i]);
        }

        try {
            let url = '/api/uploads';
            if (currentTrackingId) {
                url = `/api/uploads/${currentTrackingId}/append`;
            }
            const res = await fetch(url, {
                method: 'POST',
                body: formData
            });
            if(res.ok) {
                const data = await res.json();
                alert(`Successfully uploaded to Tracking ID: ${data.tracking_id}`);
                currentTrackingId = data.tracking_id;
                fetchRecentUploads();
                loadTrackingSession(data.tracking_id);
                // Clear file input
                input.value = '';
            } else {
                alert('Upload failed.');
            }
        } catch(e) {
            console.error(e);
            alert('Error during upload.');
        }
    }

    async function loadTrackingSession(trackingId) {
        currentTrackingId = trackingId;
        try {
            const res = await fetch(`/api/uploads/${trackingId}/files`);
            if(res.ok) {
                const data = await res.json();
                // Clear existing lists
                uploadedCsvFiles = [];
                uploadedPdfFiles = [];
                
                // Sort files by type based on extension
                data.files.forEach(f => {
                    const name = f.filename.toLowerCase();
                    const fileObj = { name: f.filename, id: f.id };
                    if (name.endsWith('.csv') || name.endsWith('.xlsx') || name.endsWith('.xls')) {
                        uploadedCsvFiles.push(fileObj);
                    } else {
                        uploadedPdfFiles.push(fileObj);
                    }
                });
                renderIngestGrids();
            }
        } catch(e) {
            console.error(e);
        }
    }

    async function previewFile(fileId, filename) {
        if(!fileId) return;
        const pane = document.getElementById('file-preview-pane');
        const contentDiv = document.getElementById('preview-content');
        document.getElementById('preview-filename').innerText = `File: ${filename}`;
        contentDiv.innerText = "Loading...";
        pane.style.display = 'block';
        pane.scrollIntoView({behavior: "smooth"});

        try {
            const res = await fetch(`/api/files/${fileId}`);
            if(res.ok) {
                const text = await res.text();
                // If it's a CSV or tabular, we could format it nicely, but pre-wrap text is fine for a glance
                contentDiv.innerText = text.substring(0, 10000) + (text.length > 10000 ? '\\n... (truncated for preview)' : '');
            } else {
                contentDiv.innerText = "Failed to load file content.";
            }
        } catch(e) {
            contentDiv.innerText = "Error loading file content.";
        }
    }

    // Call fetchRecentUploads on load
    document.addEventListener("DOMContentLoaded", () => {
        fetchRecentUploads();
    });
    '''

    # Inject the JS logic before the closing script tag
    html = html.replace('</script>\n</body>', js_logic + '\n</script>\n</body>')

    # Now we must update renderIngestGrids to include onclick="previewFile(id, name)"
    # The existing template:
    # <div class="dataset-card">
    #    <div class="card-icon">...</div>
    #    <div class="card-title">${f.name}</div>...
    
    # Let's replace the innerHTML map parts
    # CSV Grid:
    csv_old_str = 'csvGrid.innerHTML = uploadedCsvFiles.map((f, i) => `\\n        <div class="dataset-card">'
    csv_new_str = 'csvGrid.innerHTML = uploadedCsvFiles.map((f, i) => `\\n        <div class="dataset-card" onclick="previewFile(${f.id}, \\\'${f.name}\\\')" style="cursor: pointer;">'
    html = html.replace(csv_old_str, csv_new_str)
    
    # Just in case there is no newline:
    csv_old_str2 = 'csvGrid.innerHTML = uploadedCsvFiles.map((f, i) => `<div class="dataset-card">'
    csv_new_str2 = 'csvGrid.innerHTML = uploadedCsvFiles.map((f, i) => `<div class="dataset-card" onclick="previewFile(${f.id}, \\\'${f.name}\\\')" style="cursor: pointer;">'
    html = html.replace(csv_old_str2, csv_new_str2)

    pdf_old_str = 'pdfGrid.innerHTML = uploadedPdfFiles.map((f, i) => `\\n        <div class="dataset-card">'
    pdf_new_str = 'pdfGrid.innerHTML = uploadedPdfFiles.map((f, i) => `\\n        <div class="dataset-card" onclick="previewFile(${f.id}, \\\'${f.name}\\\')" style="cursor: pointer;">'
    html = html.replace(pdf_old_str, pdf_new_str)
    
    pdf_old_str2 = 'pdfGrid.innerHTML = uploadedPdfFiles.map((f, i) => `<div class="dataset-card">'
    pdf_new_str2 = 'pdfGrid.innerHTML = uploadedPdfFiles.map((f, i) => `<div class="dataset-card" onclick="previewFile(${f.id}, \\\'${f.name}\\\')" style="cursor: pointer;">'
    html = html.replace(pdf_old_str2, pdf_new_str2)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html successfully.")

update_index_html()
