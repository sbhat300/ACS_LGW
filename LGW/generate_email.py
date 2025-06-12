import requests
import os 
from dotenv import load_dotenv
from typing import List

def generate_ad(info: List[str]) -> str:
    """
        Generates a google search ad with a heading and description based off of the realtor's profile and inputs.

        Args:
            info (List[str]): A list of information about the realtor and their preferences

        Returns:
            str: The generated ad heading and description
            
        Raises:
            Exception: If the call to the Together AI API fails to fetch a response.
    """
    
    #TODO: Split headline and description generator in two parts
    load_dotenv()
    TAI_KEY = os.getenv('TAI_KEY')
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TAI_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = {
        'role': 'system',
        'content': (
            'You are an assistant that creates engaging and compelling text based ads for realtors that appear on Google searches.' 
            '''You will be provided some input from the realtor in the form of a list containing general information about them and what they want in the ad'''
            '**INSTRUCTIONS:**'
            '''1.  **Analyze Input:** Carefully review the realtor's details provided and include them in the ad you generate'''
            '''2.  **Generate Ad:** Create one ad, which should target things like speed/efficiency, expertise/trust, specific offers, etc.'''
            '''3.  **Follow Ad Structure:** The ad must consist of:'''
                '''* **Headline:** The headline must be **30 characters or less**.'''
                '''* **Description:** The description must be **90 characters or less**.'''
            '''4.  **Ad Guidelines:**'''
                    '''* **Include Keywords:** Naturally incorporate keywords.'''
                    '''* **Strong Call-to-Action (CTA):** The headline and description must contain a clear and compelling CTA (e.g., "Get a Free Valuation," "View Listings Now," "Schedule a Showing").'''
                    '''* **Highlight Unique Selling Propositions (USPs):** Emphasize what makes the realtor stand out (e.g., "Top 1% Agent," "Sell in 30 Days," "Local Expert Since 2005").'''
                    '''* **Create Urgency & Trust:** Use words that build trust ("Certified," "Expert," "Trusted") and create a sense of urgency ("Homes Sell Fast," "Market is Hot").'''
            '''5.  **Formatting:** Present the output clearly, with the headline and description you create. Do not include any other commentary.'''
        )
    }
    information = {
        'role': 'user',
        'content': (
            '\n'.join(info)
        )
    }
    messages = [system_prompt, information]
    
    payload = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.4,
        "top_p": 0.9,
        "repetition_penalty": 1.2,
        "stop": ["<|im_end|>", "<|endoftext|>"],
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()    
    if response.status_code != 200 or "choices" not in response_data:
        raise Exception("Failed to fetch response from Together AI API", response_data)
    
    return response_data["choices"][0]["message"]["content"]
    
if __name__ == '__main__':
    information = ['Name: Mike Jones', 'Location: California', '100 homes sold', 'fast response time', 'strong work ethic']
    print(generate_ad(information))