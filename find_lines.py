import re

def main():
    with open('c:/CBRE_Ontology/index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    out = open('c:/CBRE_Ontology/lines.txt', 'w', encoding='utf-8')
        
    start_hero = -1
    end_hero = -1
    for i, line in enumerate(lines):
        if '<div class="hero-actions">' in line:
            start_hero = i
        if start_hero != -1 and '</div>' in line and i > start_hero:
            if i - start_hero <= 5:
                end_hero = i
                break
                
    out.write(f"Hero Actions: Lines {start_hero+1} to {end_hero+1}\n")
    for i in range(start_hero, end_hero+1):
        out.write(f"{i+1}: {lines[i].rstrip()}\n")

    start_eval = -1
    end_eval = -1
    for i, line in enumerate(lines):
        if '<div class="view" id="view-eval">' in line:
            start_eval = i
        if start_eval != -1 and '</div>' in line and i > start_eval:
            end_eval = i
            
    out.write(f"\nEval View: Line {start_eval+1}\n")
    for i in range(start_eval, start_eval+10):
        out.write(f"{i+1}: {lines[i].rstrip()}\n")

    # Topnav
    start_nav = -1
    end_nav = -1
    for i, line in enumerate(lines):
        if '<div class="topnav" id="topnav">' in line:
            start_nav = i
        if start_nav != -1 and '</div>' in line and i > start_nav:
            end_nav = i
            break
            
    out.write(f"\nTopnav: Lines {start_nav+1} to {end_nav+1}\n")
    for i in range(start_nav, end_nav+1):
        out.write(f"{i+1}: {lines[i].rstrip()}\n")
        
    out.close()

if __name__ == '__main__':
    main()
