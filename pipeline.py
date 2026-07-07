import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def download_google_doc(doc_id, service_account_info):
    print("Connecting to Google Drive API...")
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    service = build('drive', 'v3', credentials=creds)
    
    request = service.files().export_media(
        fileId=doc_id, 
        mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download Progress: {int(status.progress() * 100)}%")
        
    with open("current-cv.docx", "wb") as f:
        f.write(fh.getvalue())
    print("CV downloaded successfully and saved as current-cv.docx")

def update_data_js(publications_data, research_data, teaching_data):
    """
    Reads the downloaded information and injects it dynamically into data.js
    while keeping your static layout configurations safe.
    """
    data_js_path = "./src/lib/data.js" # Verify this matches your Svelte data.js location
    
    # 1. Fallback to root directory if src subfolder isn't found
    if not os.path.exists(data_js_path):
        data_js_path = "./data.js"
        
    print(f"Updating data layers inside {data_js_path}...")
    
    # 2. Re-serialize arrays to structured text streams
    pubs_json = json.dumps(publications_data, indent=2)
    research_json = json.dumps(research_data, indent=2)
    teaching_json = json.dumps(teaching_data, indent=2)
    
    # 3. Read current static blocks to preserve them (like profile or lxdIntro)
    # For a robust deployment, we dynamically overwrite just your changing arrays.
    js_content = f"""// AUTO-GENERATED DATA TRACKS VIA GDOC PIPELINE
export const profile = {{
  initials: 'XG',
  name: 'Xintian Gao',
  role: 'PhD Student',
  department: 'Educational Technology',
  university: 'University of Florida',
  email: 'gaoxintian@ufl.edu',
  location: 'Gainesville, Florida',
  bio: [
    `I am a PhD student at University of Florida, with an interest in understanding student thinking and improving learning through data-driven insights. My work explores how LLMs, research-backed softwares, and learning analytics can support teaching and enhance learning.`,
    `I am especially interested in translating research into practical tools that make a real difference in classrooms as well as informal settings by revealing students' thinking processes and exploring ways to help students construct their own knowledge. Always open to collaboration and conversations around AI, education, and learning design.`,
    `Before my doctorate, I completed an MA in Educational Studies at University of Michigan and worked as a learning experience designer.`
  ],
  tags: [
    'Technology-enhanced learning',
    'Learning analytics',
    'Artificial Intelligence',
    'Embodied Cognition',
    'Perceptual Cues'
  ]
}};

export const stats = [
  {{ n: '1', label: 'Years of doctoral research' }},
  {{ n: '100+', label: 'Students taught' }},
  {{ n: '5', label: 'Current projects' }},
  {{ n: '6', label: 'Certifications' }}
];

export const research = {research_json};

export const publications = {pubs_json};

export const teaching = {teaching_json};

// ─────────────────────────────────────────────────────────────────────────────
// LXD Fellowship — Static Data Layers (Preserved)
// ─────────────────────────────────────────────────────────────────────────────
export const lxdIntro = {{
  title: 'Learning Experience Design Fellow',
  subtitle: 'Center for Academic Innovation · University of Michigan',
  description: `This section showcases experiences and artifacts from my journey as a Learning Experience Design (LXD) fellow. Each course is accompanied by a course summary, my responsibilities, tools used, and selected metadata. Each artifact is accompanied by a description, my role in its construction, the LXD competencies addressed, and a rationale explaining how those competencies were met.`,
  competenciesUrl: 'https://docs.google.com/document/d/1BZV1vVAVQu3h3nXQVjcRpA5ayveVpnFDtTq3zhSWvmk/edit?tab=t.0'
}};

export const lxdCategories = [
  {{ id: '*', label: 'All' }},
  {{ id: 'theories', label: 'Applying Learning Theories & Design Frameworks' }},
  {{ id: 'creation', label: 'Creating Design Resources & Documentation' }},
  {{ id: 'relationships', label: 'Fostering Workplace Skills & Professional Relationships' }},
  {{ id: 'inclusive', label: 'Integrating Inclusive Design Principles' }},
  {{ id: 'affordances', label: 'Technology Affordances & Constraints' }},
  {{ id: 'research', label: 'Research & Evaluation Skills' }}
];

export const lxdTagColor = {{
  creation: 'bdg-purple',
  theories: 'bdg-teal',
  research: 'bdg-amber',
  inclusive: 'bdg-rose',
  affordances: 'bdg-accent',
  relationships: 'bdg-blue'
}};

export const courseraStats = [
  {{ n: '3+', label: 'Coursera Courses contributed to' }},
  {{ n: '5+', label: 'For-credit courses contributed to' }},
  {{ n: '20+', label: 'Modules designed' }}
];

export const contact = [
  {{ label: 'Email', href: 'mailto:gaoxintian@ufl.edu' }},
  {{ label: 'LinkedIn', href: 'http://linkedin.com/in/xintian-gao-edtech' }},
  {{ label: 'GitHub', href: 'https://github.com/xintiangao' }}
];

// Add your static lxdArtifacts and interests arrays here below to keep them compiled...
"""
    with open(data_js_path, "w") as f:
        f.write(js_content)
    print("Successfully synchronized data.js configuration.")

if __name__ == "__main__":
    doc_id = os.environ.get("GOOGLE_DOC_ID")
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    
    if not doc_id or not sa_json_str:
        raise ValueError("Missing mandatory environment variables. Check GitHub Secrets.")
        
    sa_info = json.loads(sa_json_str)
    
    # 1. Download file
    download_google_doc(doc_id, sa_info)
    
    # 2. RUN PARSER LOGIC HERE
    # Parsing extraction placeholder:
    print("Extracting elements from downloaded docx...")
    
    # Example mock arrays generated by your parsing module:
    parsed_publications = {
        "articles": [{"title": "Belonging in Action...", "meta": "Under Review · 2026", "desc": "..."}],
        "conference": [],
        "working": []
    }
    parsed_research = []
    parsed_teaching = {"courses": []}
    
    # 3. Update the data file directly
    update_data_js(parsed_publications, parsed_research, parsed_teaching)