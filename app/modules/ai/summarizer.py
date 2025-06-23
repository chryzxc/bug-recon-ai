import openai  # or your preferred AI provider
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
        Analyze these security findings and create a concise executive summary:
        
        Findings:
        {findings}
        
        The summary should:
        - Highlight critical issues first
        - Group similar findings
        - Provide a risk assessment
        - Be written for a non-technical audience
        - Be under 200 words
        """
        
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