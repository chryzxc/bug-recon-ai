from typing import List, Dict
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class AISummarizer:
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"), 
        )
    
    def summarize_findings(self, findings: List[Dict]) -> str:
        """Use AI to generate a executive summary of findings"""
        if not findings:
            return "No security findings detected during the scan."
        
        # Prepare prompt
        prompt = f"""  
**Role**: You are an experienced **bug bounty hunter** and **security researcher**. Analyze the provided findings and generate a **concise, actionable summary** (max 400 words) with the following structure:  

### **1. Attack Simulation Steps**  
- Provide a **step-by-step method** to replicate/exploit the findings (e.g., "If X is vulnerable, try Y to escalate privileges").  
- Include **realistic attack scenarios** (e.g., "Chain this with SSRF to access internal systems").
- Put your shoes on the hacker perspective

### **2. Tools for Testing**  
- List **specific tools** (e.g., `Burp Suite`, `Nuclei`, `sqlmap`) and **commands/scripts** relevant to the findings.  
- Mention **automation tips** (e.g., "Use `ffuf` for brute-forcing endpoints").  

### **3. Prevention & Mitigation**  
- Provide **defensive recommendations** (e.g., "Enable WAF rules to block XXE attacks").  
- Include **secure coding practices** or **configuration fixes** (e.g., "Sanitize inputs using OWASP CheatSheet").  

### **Findings Input**:  
{findings}
**Rules**:  
- Be **technical but concise** (avoid fluff).  
- Prioritize **high-impact vulnerabilities** first.  
- Use **bullet points** for readability.
- Add some links that is related to the exploit.
"""  
        # prompt = f"""
        # Analyze these security findings and create a concise executive summary and steps as well on how to prevent the attack and simulate how the attackers would attack:
        
        # Findings:
        # {findings}
        
        # The summary should:
        # - Highlight critical issues first
        # - Group similar findings
        # - Provide a risk assessment
        # - Simulate and provide steps how the attackers will attack to prevent the exploit
        # - Be written for a non-technical audience
        # - Be under 400 words
        # """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                {"role": "system", "content": "You are a security analyst summarizing scan results."},
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
)
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI summarization failed: {e}")
            return "AI summary unavailable. Please review the detailed findings."