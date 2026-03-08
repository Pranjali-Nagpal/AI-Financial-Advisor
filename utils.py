import re

# Split advice sections
def split_advice_sections(advice_text):
    # Clean up markdown formatting artifacts
    advice_text = advice_text.replace("*", "").replace("{", " ").replace("}", " ")
    
    # Define the headers to split by (Matching the prompt from ai_advisor.py and the screenshot)
    pattern = r'(Current Financial Health:|Existing Savings Utilization:|Monthly Savings Strategy:|Debt Plan:|Investment Advice:|Goal Guidance:|Budgeting:|Investment Action Plan:)'
    
    splits = re.split(pattern, advice_text)
    sections = []
    
    # Loop through the splits, grabbing the title and its corresponding content
    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        
        # Safety check to ensure content exists for the header
        if i + 1 < len(splits):
            content = splits[i+1].strip()
        else:
            content = ""
        
        # Format "Current Financial Health" as a standard paragraph
        if "Current Financial Health" in title:
            content_html = "<p style='margin:0; line-height:1.4em'>" + content.replace("\n", "<br>") + "</p>"
        else:
            # Format everything else as an unordered list
            content_html = "<ul style='margin:0; padding-left:18px; line-height:1.4em'>"
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("-"):
                    content_html += f"<li>{line[1:].strip()}</li>"
                elif line:
                    content_html += f"<li>{line}</li>"
            content_html += "</ul>"
            
        sections.append((title, content_html))
        
    return sections

# Split goal sections
def split_goal_sections(goal_text):
    # Clean up markdown artifacts
    goal_text = goal_text.replace("*", "")
    
    # Define the headers for the goal roadmap (From the screenshot)
    pattern = r'(Financial Impact Analysis:|Revised Goal Timeline:|Monthly Action Plan:|Resource Allocation Strategy:|Risk Assessment & Mitigation:)'
    
    splits = re.split(pattern, goal_text)
    sections = []
    
    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        
        if i + 1 < len(splits):
            content = splits[i+1].strip()
        else:
            content = ""
        
        # Format all goal sections as unordered lists
        content_html = "<ul style='margin:0; padding-left:18px; line-height:1.5em'>"
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                content_html += f"<li>{line[1:].strip()}</li>"
            elif line:
                content_html += f"<li>{line}</li>"
        content_html += "</ul>"
        
        sections.append((title, content_html))
        
    return sections