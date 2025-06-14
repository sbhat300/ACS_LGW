import requests
import os 
from dotenv import load_dotenv
from typing import List, Tuple

def generate_headline(info: List[str]) -> str:
    """
        Generates a google search ad heading based off of the realtor's profile and inputs.

        Args:
            info (List[str]): A list of information about the realtor and their preferences

        Returns:
            heading (str): The generated ad heading
            
        Raises:
            Exception: If the call to the Together AI API fails to fetch a response.
    """
    
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
            '''You are an assistant that creates engaging and compelling text based ads for realtors that appear on Google searches.
You will be provided some input from the realtor in the form of a list containing general information about them and what they want in the ad
INSTRUCTIONS:
1.  Analyze Input: Carefully review the realtor's details provided and include them in the ad you generate
2.  Generate Ad: Create one ad, which should target things like speed/efficiency, expertise/trust, specific offers, etc.
3.  Follow Ad Structure: The ad must be 30 characters or less.
4.  Ad Guidelines:
        * Include Keywords: Naturally incorporate keywords.
        * Strong Call-to-Action (CTA): The ad must contain a clear and compelling CTA (e.g., Get a Free Valuation, View Listings Now, Schedule a Showing).
        * Highlight Unique Selling Propositions (USPs): Emphasize what makes the realtor stand out (e.g., Top 1% Agent, Sell in 30 Days, Local Expert Since 2005).
        * Create Urgency & Trust: Use words that build trust (Certified, Expert, Trusted) and create a sense of urgency (Homes Sell Fast, Market is Hot).
5.  Formatting: Present the ad you create clearly. Do not include any other commentary.'''
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
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": 30,
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
    
    return response_data["choices"][0]["message"]["content"].strip()

def generate_description(info: List[str]) -> str:
    """
        Generates a google search ad description based off of the realtor's profile and inputs.

        Args:
            info (List[str]): A list containing the headline and information about the realtor and their preferences

        Returns:
            description (str): The generated ad description
            
        Raises:
            Exception: If the call to the Together AI API fails to fetch a response.
    """
    
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
            '''You are an assistant that creates engaging and compelling text based ads for realtors that appear on Google searches.
You will be provided some input from the realtor in the form of a list containing general information about them and what they want in the ad
INSTRUCTIONS:
1.  Analyze Input: The initial line you are provided with is the ad's headline. Afterwards, you will recieve information about the realtor. Carefully review the realtor's details provided and include them in the ad you generate
2.  Generate Ad: Create one ad, which should target things like speed/efficiency, expertise/trust, specific offers, etc.
3.  Follow Ad Structure: The ad must be 90 characters or less.
4.  Ad Guidelines:
        * Include Keywords: Naturally incorporate keywords.
        * Strong Call-to-Action (CTA): The ad must contain a clear and compelling CTA (e.g., Get a Free Valuation, View Listings Now, Schedule a Showing).
        * Highlight Unique Selling Propositions (USPs): Emphasize what makes the realtor stand out (e.g., Top 1% Agent, Sell in 30 Days, Local Expert Since 2005).
        * Create Urgency & Trust: Use words that build trust (Certified, Expert, Trusted) and create a sense of urgency (Homes Sell Fast, Market is Hot).
5.  Formatting: Present the ad you create clearly. Do not include any other commentary.'''
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
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": 90,
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
    
    return response_data["choices"][0]["message"]["content"].strip()

def shorten(inp: str, length: int) -> str:
    '''
        Attempts to shorten a message that is above the character limit for the ad
        
        Args:
            inp (str): The input that needs to be shortened
            length (int): The max length
            
        Returns:
            shortened (str): The shorter string
    '''
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
            f'''You are an assistant that shortens text to fit in the character limit while maintaining the meaning and tone of the text. The text must be less than {length} characters long\n
            Formatting: Provide only the shortened text as the output. Do not include any other commentary'''
        )
    }

    messages = [system_prompt, {
        'role': 'user',
        'content': (
            inp
        )
    }]
    
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": length,
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
    
    return response_data["choices"][0]["message"]["content"].strip()
    
def generate_ad(information: List[str]) -> Tuple[str, str]:
    """
        Generates a Google Ad with a headline and description given some information
        
        Args:
            info (List[str]): A list containing information about the realtor and their preferences

        Returns:
            heading, description (Tuple[str, str]): The heading and description of the ad
            
        Raises:
            Exception: If the call to the Together AI API fails to fetch a response.
            Exception: If the headline or description could not be shortened
    """
    headline = generate_headline(information)
    if len(headline) > 30:
        headline = shorten(headline, 30)
    if len(headline) > 30:
        raise Exception('Failed to generate a valid headline')
    information.insert(0, headline)
    description = generate_description(information)
    if len(description) > 90:
        description = shorten(description, 90)
    if len(description) > 90:
        raise Exception('Failed to generate a valid description')
    return headline, description
    
if __name__ == '__main__':
    information = ['Name: Mike Jones', 'Location: California', '100 homes sold', 'fast response time', 'strong work ethic']
    
    heading, description = generate_ad(information)
    print(f'{heading}\n{description}')
        