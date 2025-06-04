import requests
import os 
from dotenv import load_dotenv

'''
Output Structure:
[
    receiver: email address of the receiver
    sender: email address of the sender
    body: the body of the email
    subject: the subject of the email
    type: outbound-email or inbound-email
]
THESE EMAILS ARE IN ORDER FROM OLDEST TO NEWEST
'''

_good_email = [
    {
        'receiver': 'ai@yahoo.com',
        'sender': 'buyer@gmail.com',
        'subject': 'Inquiry About 123 Maple Street',
        'body': '''Dear John,  
I came across the listing for 123 Maple Street and really like what I see. The location and layout seem like a great fit, but I have a few questions before deciding if I want to move forward.  
Could you tell me about the condition of the roof, HVAC, and any major systems? Also, how competitive is the market right now—would I need to move quickly if I’m interested?  
Best,  
Alex Carter''',
        'type': 'inbound-email'
    },
    {
        'receiver': 'buyer@gmail.com',
        'sender': 'ai@yahoo.com',
        'subject': 'Re: Inquiry About 123 Maple Street',
        'body': '''Dear Alex,  
I’m glad you like the home! Here’s a quick breakdown of the major systems:  
- **Roof:** Replaced in **2018**, still in excellent condition.  
- **HVAC:** Central air and heating system updated in **2021**.  
- **Plumbing & Electrical:** Both systems are up to code with no reported issues.  
As for the market, **homes in this price range are moving fairly quickly**, but there’s still time to make an informed decision. This property has **received some interest**, so I’d recommend scheduling a showing soon if you’d like to see it in person.  
Would **this Saturday or Sunday work for a tour**?  
Best,  
John  
ACS Realty''',
        'type': 'outbound-email'
    },
    {
        'receiver': 'ai@yahoo.com',
        'sender': 'buyer@gmail.com',
        'subject': 'Re: Inquiry About 123 Maple Street',
        'body': '''Dear John,  
Thanks for the details! That’s good to know. I do like the home, and I’d be interested in seeing it in person before making a decision.  
Saturday could work for a tour—what times do you have available? Also, are there any similar homes nearby that I should check out while I’m in the area?  
Best,  
Alex''',
    'type': 'inbound-email'
    },
    {
        'receiver': 'buyer@gmail.com',
        'sender': 'ai@yahoo.com',
        'subject': 'Re: Inquiry About 123 Maple Street',
        'body': '''Dear Alex,  
Great! I have availability for a **private showing this Saturday at 11 AM or 2 PM**—let me know which works best for you.  
I also found **two similar homes nearby** that might interest you. One has a **larger backyard**, and the other features a **fully finished basement**. I’d be happy to set up back-to-back tours so you can compare them all at once.  
Let me know what works best for you, and I’ll get everything scheduled!  
Best,  
John  
ACS Realty''',
        'type': 'outbound-email'
    }
]

def parse_messages(realtor_email: str, emails: list[dict[str,str]]) -> list[dict[str, str]]:
    """
        Parses messages so they can be sent and interpreted by the LLM

        Args:
            realtor_email (str): The email of the realtor.
            emails (list[dict[str, str]]): The chain of emails.

        Returns:
            list[dict[str, str]]: The correctly formatted list of emails.
    """
    messages = []
    
    for email in emails:
        if email['sender'].split('@')[1] == 'lgw.automatedconsultancy.com':
            continue
        messages.append({'role': 'user', 'content':  
                                        ('REALTOR: ' if email['sender'] == realtor_email else 'BUYER: ')
                                        + email['body']})
    return messages

def calc_ev(messages: list[dict[str, str]]) -> int:
    """
        Calculates the EV based off of a list of messages

        Args:
            messages (list[dict[str, str]]): The formatted list of emails.

        Returns:
            int: The calculated EV score.
            
        Raises:
            ValueError: If the LLM does not return a valid int
    """
    load_dotenv()
    tai_key = os.getenv('TAI_KEY')
    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
            "Authorization": f"Bearer {tai_key}",
            "Content-Type": "application/json"
    }
    payload_messages = [{
        "role": "system",
        "content": '''The assistant should only respond with a number. This number will be in the range from 0-100. This number will indicate how interested a prospective buyer of a property is interested in it. The assistant will do this buy looking at a series of emails. These emails will be from the prospective buyer and an realtor helping the buyer. Each email will be sent as a separate message by the user, and the first word will indicate if the email was sent by a buyer or an realtor. 
                    If the first word is BUYER: the email that follows is sent by a buyer. 
                    If the first word is REALTOR: the email that follows is sent by a realtor. 
                    The assistant will analyze this series of emails, and reply with the number that indicates the interest of the prospective buyer of the property'''
    }]
    payload_messages.extend(messages)
    print(payload_messages)
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": payload_messages,
        "max_tokens": 5,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|im_end|>", "<|endoftext|>"],
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
        
    if response.status_code != 200 or "choices" not in response_data:
        raise Exception("Failed to fetch response from Together AI API", response_data)

    try:
        ev = int(response_data["choices"][0]["message"]["content"])
        return ev
    except ValueError:
        raise ValueError('The AI did not return a valid number')

if __name__ == '__main__':
    realtor_email = 'ai@yahoo.com'
    inp = parse_messages(realtor_email, _good_email)
    ev = calc_ev(inp)