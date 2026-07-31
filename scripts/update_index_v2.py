def update():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Fix the height for the preview pane
    html = html.replace('height: 350px;', 'height: 75vh;')
    
    # 2. Add detailed error logging to the JS
    old_catch = """        } catch(e) {
            console.error(e);
            alert('Error during upload.');
        }"""
    
    new_catch = """        } catch(e) {
            console.error('Upload Error:', e);
            alert(`Error during upload: ${e.message}`);
        }"""
    html = html.replace(old_catch, new_catch)
    
    old_else = """            } else {
                alert('Upload failed.');
            }"""
            
    new_else = """            } else {
                const errText = await res.text();
                alert(`Upload failed. Server responded with: ${res.status} ${errText}`);
            }"""
    html = html.replace(old_else, new_else)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
update()
