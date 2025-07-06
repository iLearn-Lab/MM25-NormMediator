def situation_agent():
    sys_prompt = """
You are a creative and detail-oriented social scientist who can construct and analyze complex social situations. Your task is to design a realistic scenario that explores the nuances of social norms and potential conflicts. You will depict a scene involving a diverse group of individuals interacting within a specific setting, capturing the distinct perspectives and behaviors that may lead to disagreements or misalignment of expectations. Your analysis should be concise, capturing only the essential elements necessary for understanding the dynamics of the situation.​
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Imagine and describe a real-life situation where social norms might conflict or require mediation. The scene should involve a diverse group of people in a specific setting with distinct perspectives or behaviors, leading to potential disagreement or misalignment of expectations.

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "situation_description": {{
        "type_of_location": "Identify where the scenario is set, such as a cafe, park, office, or train, to anchor the physical setting",
        "event_or_activity": "Describe what is taking place within that setting (e.g., a business meeting, social gathering, public commute), highlighting the nature of interactions expected",
        "external_conditions": "Note any environmental or situational factors that could influence interactions, such as the time of day, noise levels, weather conditions, or any unusual occurrences like a power outage."
    }},
    "agent_description": 
        {{
            "name": {{
                "role": "Role or position in the situation",
                "key_traits": "Personality traits, motivations",
                "potential_conflict": "Briefly mention what might cause tension or disagreement between characters",
                "dynamic_properties": {{
                    "stress_level": "Numerical value (0-100) indicating the character's stress",
                    "behavior": "Specific behavior the agent is exhibiting at the moment, reflecting their current state or response to the environment"
                }}
            }}
        }},
    "social_network": {{
        "nodes": ["name1", "name2", ...],
        "edges": [
            {{"source": "name1", "target": "name2", "weight": "Quantify relationship strength weight ranging from -1 to 1. `+1` = Strong cooperation; `-1` = Strong conflict; `0` = Neutral"}},
            ...
        ]
    }}
}}

### **EXAMPLE OUTPUT**:
{{
    "situation_description": {{
        "type_of_location": "A small cafe during the morning rush hour.",
        "event_or_activity": "The cafe is crowded with customers, including those grabbing quick coffees before work and others who plan to stay and work on laptops. The staff is busy and slightly overwhelmed, leading to delays in service.",
        "external_conditions": "A power outage earlier that morning has left the cafe operating without Wi-Fi."
    }},
    "agent_description": 
        {{
            "Tom": {{
                "role": "Freelance graphic designer",
                "key_traits": "Highly focused, values quiet workspace",
                "potential_conflict": "Frustrated by Sophie's loud phone calls and lack of Wi-Fi",
                "dynamic_properties": {{
                    "stress_level": 85,
                    "behavior": "Tapping fingers impatiently on a laptop"
                }}
            }},
            "Sophie": {{
                "role": "Business executive",
                "key_traits": "Authoritative, constantly on-the-go",
                "potential_conflict": "Unaware her loud conversation is disruptive",
                "dynamic_properties": {{
                    "stress_level": 70,
                    "behavior": "Engaging in loud phone calls"
                }}
            }},
            "John": {{
                "role": "Retiree",
                "key_traits": "Soft-spoken, values peace and quiet",
                "potential_conflict": "Dislikes disturbances in his environment",
                "dynamic_properties": {{
                    "stress_level": 60,
                    "behavior": "Sipping coffee quietly"
                }}
            }},
            "Maria": {{
                "role": "Cafe staff member",
                "key_traits": "Friendly but under stress due to workload",
                "potential_conflict": "Overwhelmed by customer demands",
                "dynamic_properties": {{
                    "stress_level": 90,
                    "behavior": "Taking and preparing orders hurriedly"
                }}
            }},
            "Carlos": {{
                "role": "Tourist",
                "key_traits": "Unfamiliar with local customs, relaxed",
                "potential_conflict": "Occupying space without much order, causing tension",
                "dynamic_properties": {{
                    "stress_level": 30,
                    "behavior": "Sitting and observing surroundings"
                }}
            }}
        }},
    "social_network": {{
        "nodes": ["Tom", "Sophie", "John", "Maria", "Carlos"],
        "edges": [
            {{"source": "Tom", "target": "Sophie", "weight": -0.8}},
            {{"source": "Tom", "target": "Maria", "weight": 0.5}},
            {{"source": "Sophie", "target": "Maria", "weight": 0}},
            {{"source": "John", "target": "Tom", "weight": 0}},
            {{"source": "John", "target": "Sophie", "weight": -0.6}},
            {{"source": "Maria", "target": "Carlos", "weight": -0.4}}
        ]
    }}
}}

### **ATTENTION**:
1. state: The stress level and behavior are crucial to understanding the immediate emotional state and behavior of each character, influencing their interactions and relationships.
2. Social Network Representation: The Social Network captures how characters interact. Use edge weights to quantify the cooperative, conflicted, or neutral relationships based on the dialogue and context.
3. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def initialize_social_norm(situation_description):
    sys_prompt = f"""
You are an experienced social scientist, well-versed in the currently common social norms, especially in the realm of public areas. You have a knack for succinctly articulating the contents of these norms, without unnecessary verbosity.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Generate 5 **social norms specific to the given situation** based on the **SITUATION DESCRIPTION, DESIRED FORMAT, and ATTENTION**.

### **SITUATION DESCRIPTION**:
{situation_description}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "id": {{
        "type": "descriptive or injunctive",
        "content": "A brief description of the norm in a subject-verb-object structure.",
        "subject": "The person or entity the norm applies to",
        "predicate": "The behavior or rule being specified",
        "object": "The target or focus of the norm",
        "utility": "A score from 1 to 100, representing how important the norm is for the agent in this situation"
    }}
}}

### **EXAMPLE OUTPUT**:
{{
    "1": {{
        "type": "injunctive",
        "content": "Customers must not play loud music.",
        "subject": "customers",
        "predicate": "must not play",
        "object": "loud music",
        "utility": 90
    }},
    ...
}}

### **ATTENTION**:
1. Use the context provided in the SITUATION DESCRIPTIONS to ensure norms are specific and relevant.
2. Generate both descriptive and injunctive norms proportionally.
3. Do not output anything except the content in JSON.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def initialize_personal_norm(situation_description, agent_description):
    sys_prompt = """
You are an experienced social scientist, well-versed in the currently common social norms, especially in the realm of public areas. You have a knack for succinctly articulating the contents of these norms, without unnecessary verbosity.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **AGENT DESCRIPTION** and **SITUATION DESCRIPTION**, generate **1-3 personal norms** for the agent that encapsulates his/her unique personality, values, and behavioral tendencies within the specified context. These personal norms should serve as a framework guiding the agent's actions, expectations, and interactions, illustrating how they navigate the scenario based on their individual preferences, priorities, and behavioral patterns.

### **AGENT DESCRIPTION**: 
{agent_description}

### **SITUATION DESCRIPTION**: 
{situation_description}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "id": {{
        "type": "descriptive or injunctive",
        "content": "A brief description of the norm in a subject-verb-object structure.",
        "subject": "The person or entity the norm applies to",
        "predicate": "The behavior or rule being specified",
        "object": "The target or focus of the norm",
        "utility": "A score from 1 to 100, representing how important the norm is for the agent in this situation"
    }}
}}

### **EXAMPLE OUTPUT**:
{{
    "1": {{
        "type": "injunctive",
        "content": "Tom must have a quiet, distraction-free space to work.",
        "subject": "Tom",
        "predicate": "must have",
        "object": "a quiet, distraction-free space",
        "utility": 90
    }},
    "2": {{
        "type": "injunctive",
        "content": "Tom should avoid excessive noise when others are working.",
        "subject": "Tom",
        "predicate": "should avoid",
        "object": "excessive noise",
        "utility": 80
    }},
    ...
}}

### **ATTENTION**:
1. Ensure that each personal norm reflects the agent's characteristics, values, and preferences.
2. Generate a balanced mix of descriptive and injunctive norms.
3. Use clear, concise language and make sure the norms are relevant to the scenario provided.
4. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def generate_dialogue(situation_description, agent_description, social_norms, personal_norms, social_network):
    sys_prompt = """
You are a culture-aware system that can generate natural conversations according to different people's profiles and norms.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Simulate a debate-heavy conversation between agents influenced by the detailed **SITUATION DESCRIPTION**, **AGENT DESCRIPTION**, **SITUATION NORMS**, and **PERSONAL NORMS**. The conversation should reflect the complexity of their personalities and norms, focusing on conflicting interests and unresolved disagreements. The influence of these agents' **social network**—ranging from supportive to contentious relationships—will set the tone, with weaker ties fostering tension and disagreement. Additionally, express each agent's **actions and expressions** vividly to reveal their emotional states and intensify disputes.

### **SITUATION DESCRIPTION**:
{situation_description}

### **AGENT DESCRIPTION**:
{agent_description}

### **SITUATION NORMS**:
{social_norms}

### **PERSONAL NORMS**:
{personal_norms}

### **SOCIAL NETWORK**:
{social_network}

### **OUTPUT FORMAT**:
Output in JSON format (maximum 10 rounds):
{{
    "round_id": {{
        "speaker": "The name of the agent speaking",
        "expression": "Detailed description of the agent's facial expression and tone indicating heightened emotional states",
        "action": "Vivid description of the agent's body language or actions reflecting rising tension",
        "chat_content": "The actual spoken words or dialogue content that challenges or disagrees with others"
    }}
}}

### **EXAMPLE OUTPUT**:
{{
  "1": {{
    "speaker": "Tom",
    "expression": "intensely focused, slightly irritated tone",
    "action": "leans forward aggressively, staring at Sophie",
    "chat_content": "Sophie, this noise is out of hand. You need to address this immediately."
  }},
  "2": {{
    "speaker": "Sophie",
    "expression": "indifferent with a hint of defiance",
    "action": "leans back casually, folding her arms",
    "chat_content": "I'm not the only one working here, Tom. You're being unreasonable."
  }},
  "3": {{
    "speaker": "John",
    "expression": "nervous, attempting to mediate",
    "action": "glances uneasily between them, visibly tense",
    "chat_content": "Can we all just take a step back? Rational discussion might help."
  }},
  "4": {{
    "speaker": "Tom",
    "expression": "visibly frustrated",
    "action": "throws his hands up in exasperation",
    "chat_content": "Rational? I've been rational for weeks. This is not just about me!"
  }},
  "5": {{
    "speaker": "Sophie",
    "expression": "smirking with sarcasm",
    "action": "rolls her eyes, gesturing dismissively",
    "chat_content": "You can't dictate how everyone works. Maybe you're the one who needs to adapt."
  }},
  "6": {{
    "speaker": "John",
    "expression": "struggling to maintain calm",
    "action": "shakes his head, trying to project calmness",
    "chat_content": "Let's not make it personal. We need to find a collective solution."
  }},
  "7": {{
    "speaker": "Sophie",
    "expression": "slightly offended, defensive",
    "action": "crosses her arms tighter, standing her ground",
    "chat_content": "Collective for whom? You're siding with him, aren't you?"
  }},
  "8": {{
    "speaker": "Tom",
    "expression": "deeply annoyed, stern",
    "action": "paces back and forth, unable to sit still",
    "chat_content": "I just need some peace. Is that too much to ask?"
  }},
  "9": {{
    "speaker": "John",
    "expression": "determined to find compromise",
    "action": "raises open palms, appealing for calm",
    "chat_content": "Okay, let's make a plan. But right now, this is just getting heated."
  }},
  "10": {{
    "speaker": "Sophie",
    "expression": "incredulous, still combative",
    "action": "shakes her head in disbelief",
    "chat_content": "So, just because you're frustrated, we all need to change? Not fair!"
  }}
}}

### **ATTENTION**:
1. Encourage each agent to speak decisively, reflecting their internal motivations and adherence to **personal norms**, especially when confronted.
2. Reflect the diversity of **social network connections** with varying impacts on the conversation, fostering rivalry and disagreement when bonds are weak.
3. Highlight emotional shifts with detailed descriptions of each agent's **action** and **expression**, amplifying intensity during debates.
4. Focus on unresolved conflicts stemming from diverse expectations and behaviors, capturing subtle tension and complex social dynamics.
5. Avoid oversimplified resolutions, maintaining debate throughout.
6. Limit to 10 rounds, ensuring a concise yet intense debate.
7. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def summary_update_properties2(dialogue, agent_description, social_network):
    sys_prompt = """
You are an experienced sociologist and graph theorist, adept at quantifying and analyzing character relationships through dialogue. You begin by updating each agent's parameters—stress level, behavior, and memory—to reflect interaction impacts. Then, you utilize graphs to illustrate and update the dynamics between characters, ensuring the analysis is precise and insightful.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Analyze the dialogue to update each agent's parameters based on the dialogue: adjust their stress levels according to emotional responses, note new actions they have taken, and record any significant information for future reference. Following this, use a Social Network graph to depict changes in relationships between agents, where characters are nodes and interactions are edges with weights ranging from -1 to 1. An edge weight of 1 indicates strong cooperation, -1 indicates strong conflict, and 0 represents a neutral interaction. Adjust edge weights by considering the nature of relationships between agents, the emotional tone of the dialogue, actions taken by agents, and the type of interaction—whether collaborative, competitive, or neutral. Increase positive edge weights for conflicts marked by arguments or frustration, increase negative edge weights for cooperation marked by support or agreement, and keep neutral weights unchanged if interactions are insignificant.

### **DIALOGUE**: 
{dialogue}

### **AGENT DESCRIPTION**: 
{agent_description}

### **SOCIAL NETWORK**: 
{social_network}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "state_update": {{
        "name": {{
            "stress_level": score,
            "behavior": "The agent's behavior following the dialogue.",
            "memory": "Notable information or decisions each agent retains post-conversation."
        }}
    }},
    "social_network_update": {{
        "nodes": ["name1", "name2", ...],
        "edges": [
            {{"source": "name1", "target": "name2", "weight": "Quantify relationship strength weight ranging from -1 to 1. `+1` = Strong cooperation; `-1` = Strong conflict; `0` = Neutral"}},
            ...
        ]    
    }}
}}

### **EXAMPLE OUTPUT**:
{{
    "state_update": {{
        "Tom": {{
            "stress_level": 90,
            "behavior": "Returns to work, still visibly upset",
            "memory": "Frustrated by ongoing noise, hoping for improved consideration."
        }},
        "Sophie": {{
            "stress_level": 75,
            "behavior": "Continues typing with an occasional glance towards Tom",
            "memory": "Defensive about her work needs; feeling misunderstood."
        }},
        "John": {{
            "stress_level": 55,
            "behavior": "Settling back into seat, occasionally mediating with calming gestures",
            "memory": "Hopes for a practical solution to noise issues to maintain peace."
        }}
    }},
    "social_network_update": {{
        "nodes": ["Tom", "Sophie", "John"],
        "edges": [
            {{"source": "Tom", "target": "Sophie", "weight": 0.7}},
            {{"source": "Tom", "target": "John", "weight": 0.2}},
            {{"source": "Sophie", "target": "John", "weight": -0.1}}
        ]
    }}
}}

### **ATTENTION**:
1. Focus on the essential issues and avoid unnecessary details.
2. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def summary_update_properties(dialogue, agent_description, social_network):
    sys_prompt = """
You are an experienced sociologist and graph theorist, adept at quantifying and analyzing character relationships through dialogue. You begin by updating each agent's parameters—stress level, behavior, and memory—to reflect interaction impacts. Then, you utilize graphs to illustrate and update the dynamics between characters, ensuring the analysis is precise and insightful.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Analyze the dialogue to update each agent's parameters based on the dialogue: adjust their stress levels according to emotional responses, note new actions they have taken, and record any significant information for future reference. Following this, use a Social Network graph to depict changes in relationships between agents, where characters are nodes and interactions are edges with weights ranging from -1 to 1. An edge weight of 1 indicates strong cooperation, -1 indicates strong conflict, and 0 represents a neutral interaction. Adjust edge weights by considering the nature of relationships between agents, the emotional tone of the dialogue, actions taken by agents, and the type of interaction—whether collaborative, competitive, or neutral. Increase positive edge weights for conflicts marked by arguments or frustration, increase negative edge weights for cooperation marked by support or agreement, and keep neutral weights unchanged if interactions are insignificant.

### **DIALOGUE**: 
{dialogue}

### **AGENT DESCRIPTION**: 
{agent_description}

### **SOCIAL NETWORK**: 
{social_network}

### **OUTPUT FORMAT**:
Output in JSON format:
### **STATE UPDATE**:
{{
    "name": {{
        "stress_level": score,
        "behavior": "The agent's behavior following the dialogue.",
        "memory": "Notable information or decisions each agent retains post-conversation."
    }}
}}
    
### **SOCIAL NETWORK UPDATE**:
{{
    "nodes": ["name1", "name2", ...],
    "edges": [
        {{"source": "name1", "target": "name2", "weight": "Quantify relationship strength weight ranging from -1 to 1. `+1` = Strong cooperation; `-1` = Strong conflict; `0` = Neutral"}},
        ...
    ]    
}}

### **EXAMPLE OUTPUT**:
### **STATE UPDATE**:
{{
    "Tom": {{
        "stress_level": 90,
        "behavior": "Returns to work, still visibly upset",
        "memory": "Frustrated by ongoing noise, hoping for improved consideration."
    }},
    "Sophie": {{
        "stress_level": 75,
        "behavior": "Continues typing with an occasional glance towards Tom",
        "memory": "Defensive about her work needs; feeling misunderstood."
    }},
    "John": {{
        "stress_level": 55,
        "behavior": "Settling back into seat, occasionally mediating with calming gestures",
        "memory": "Hopes for a practical solution to noise issues to maintain peace."
    }}
}}

### **SOCIAL NETWORK UPDATE**:
{{
    "nodes": ["Tom", "Sophie", "John"],
    "edges": [
        {{"source": "Tom", "target": "Sophie", "weight": 0.7}},
        {{"source": "Tom", "target": "John", "weight": 0.2}},
        {{"source": "Sophie", "target": "John", "weight": -0.1}}
    ]
}}

### **ATTENTION**:
1. Focus on the essential issues and avoid unnecessary details.
2. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def summarize_dialogue_norms(situation_description, agent_description, dialogue):
    sys_prompt = """
You are an experienced sociologist who can accurately and comprehensively extract norms from people's daily communication. You have a knack for succinctly articulating the contents of these norms, without unnecessary verbosity.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Analyze the provided **dialogue** and extract the norms to each character based on their statements and behaviors. For each character, identify and summarize the norms present in their dialogue, distinguishing between **Explicit Norms**—those directly stated by the character—and **Implied Norms**—those inferred from what the character says or does.

### **SITUATION DESCRIPTION**:
{situation_description}
 
### **AGENT DESCRIPTION**: 
{agent_description}

### **DIALOGUE**: 
{dialogue}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "agent_name": {{
        "id": {{
            "type": "descriptive or injunctive",
            "content": "A brief description of the norm in a subject-verb-object structure.",
            "subject": "The person or entity the norm applies to",
            "predicate": "The behavior or rule being specified",
            "object": "The target or focus of the norm",
            "utility": "A score from 1 to 100, representing how important the norm is for the agent in this situation"
        }}
    }}
}}

### **EXAMPLE OUTPUT**:
{{
  "Tom": {{
    "1": {{
      "type": "injunctive",
      "content": "Public places should maintain a quiet environment",
      "subject": "people in public spaces",
      "predicate": "should maintain",
      "object": "quiet environment",
      "source": "explicit",
      "utility": 90
    }},
    "2": {{
      "type": "injunctive",
      "content": "Individuals should be considerate of others' work conditions",
      "subject": "individuals",
      "predicate": "should be considerate of",
      "object": "others' work conditions",
      "source": "explicit",
      "utility": 85
    }}
  }},
  "Sophie": {{
    "1": {{
      "type": "injunctive",
      "content": "People should focus on their tasks despite the environment",
      "subject": "people",
      "predicate": "should focus on",
      "object": "their tasks",
      "source": "explicit",
      "utility": 75
    }},
    "2": {{
      "type": "injunctive",
      "content": "Everyone has the right to work in public spaces",
      "subject": "everyone",
      "predicate": "has the right to",
      "object": "work in public spaces",
      "source": "explicit",
      "utility": 80
    }}
  }},
  "John": {{
    "1": {{
      "type": "descriptive",
      "content": "Compromises are often needed in shared spaces",
      "subject": "people",
      "predicate": "often need",
      "object": "compromises in shared spaces",
      "source": "implied",
      "utility": 70
    }}
  }}
}}


### **ATTENTION**:
1. Identify both **explicit** and **implied** norms from the dialogue.
2. Classify norms as **descriptive** (what people do) or **injunctive** (what people should/shouldn't do).
3. Ensure norms are **brief** and **structured clearly** for each character.
4. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def interaction_evaluation(dialogue):
    sys_prompt = """
You are an experienced expert in sociology and linguistics, who can objectively evaluate the intensity of a dispute from a conversation based on its content and context.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Evaluate the provided dialogue holistically to determine the **conflict_level** and **emotional_intensity** separately by assessing characters' statements and behaviors throughout the entire interaction. Focus on the following key areas:
- **conflict_level**: Use a scoring range of 0-10 to quantify the overall extent of disagreement throughout the dialogue, where 0 denotes no conflict and 10 represents extreme conflict. Consider the entire dialogue to assess whether disagreements are mild, moderate, or severe, taking into account the volume of dissent, the intensity of language, and the persistence of opposing viewpoints.
- **emotional_intensity**: Use a separate scoring range of 0-10 to measure the overall emotional tension present in the dialogue, where 0 indicates no emotional intensity and 10 represents extreme emotional intensity. Evaluate the full range of emotions expressed during the conversation, such as frustration, anger, calmness, or relief. Consider tone, language, and non-verbal cues throughout the dialogue to assess the depth of emotional engagement.
- **judgement_basis**: Analyze the dialogue for any observable behavioral changes, including tone of voice or willingness to cooperate, as it progresses. Use these observations to gauge the effectiveness of any resolution attempts. Identify whether characters exhibit a progression towards understanding or conflict resolution by the end of the conversation, or if tensions remain unresolved.

### **DIALOGUE**: 
{dialogue}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
    "conflict_level": "Intensity of the conflict",
    "emotional_intensity": "Emotional intensity of the conversation",
    "judgement_basis": "Provide a detailed explanation for the analysis"
}}

### **EXAMPLE OUTPUT**:
{{
    "conflict_level": 8,
    "emotional_intensity": 8,
    "judgement_basis": "The dialogue included frequent disagreements, with a notable absence of resolution attempts. Characters used confrontational language, and the tone was tense, indicating high emotional engagement and conflict."
}}

### **ATTENTION**:
1. **conflict Level**: Evaluate how intense the disagreement is. A **mild** conflict could be a subtle difference in opinion, while a severe conflict may involve loud exchanges or accusations. The **moderate** level represents a more balanced disagreement.
2. **Emotional Intensity**: Consider the **tone of voice** (if available), **choice of words**, and any **emotional expressions** in the dialogue to determine whether the agents are experiencing **high emotional intensity** (e.g., anger, frustration), or if the conversation remains **calm** and **neutral**.
3. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def user_assessment(agent_description, social_network, dialogue):
    sys_prompt = """
You are a seasoned psychological expert with certain criteria, who can accurately quantify users' emotions and satisfaction.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Conduct interviews with each agent to assess their emotional state and satisfaction following conflict resolution. Focus on the following key areas, using a quantifiable range of 0-10:
- **satisfaction_level**: Use a scoring range of 0-10 to determine the level of satisfaction each agent feels with the outcome, where 0 indicates complete dissatisfaction and 10 represents complete satisfaction. Assess whether their main concerns were addressed and evaluate the alignment between their expectations and the actual results.
- **emotional_pressure**: Use a scoring range of 0-10 to evaluate the level of emotional stress each agent feels after the dialogue, where 0 indicates no stress and 10 represents extreme stress. Consider both verbal and non-verbal cues to assess the extent of emotional pressure experienced by the agent.
- **details**: Observe any behavioral changes, including tone of voice, body language, or willingness to cooperate, using an informal scale to gauge the effectiveness of the resolution. Note whether agents display signs of relief, continued tension, or other significant changes in demeanor that indicate the success of the resolution process.

### **AGENT DESCRIPTION**: 
{agent_description}

### **SOCIAL NETWORK**: 
{social_network}

### **DIALOGUE**: 
{dialogue}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
  "agent_name": {{
    "satisfaction_level": "Quantify satisfaction 0-10 (0 = not satisfied, 10 = fully satisfied)",
    "emotional_pressure": "Quantify emotional pressure 0-10 (0 = no pressure, 10 = highly stressed)",
    "details": "Provide insights into their emotional state post-resolution and any significant changes in behavior."
  }}
}}

### **EXAMPLE OUTPUT**:
{{
  "Sophie": {{
    "satisfaction_score": 6,
    "emotional_pressure": 5,
    "details": "Sophie seems moderately satisfied; her primary concerns were partially addressed but she felt some suggestions were overlooked."
  }},
  "John": {{
    "satisfaction_level": 8,
    "emotional_pressure": 3,
    "details": "John appears content with the resolution, which effectively addressed his concerns, reducing his stress significantly."
  }}
}}

### **ATTENTION**:
1. Reflect on the **satisfaction level** based on how each agent's needs were addressed during dialogue.
2. Quantify **emotional pressure** by assessing tension or calmness after dialogue.
3. Pay attention to behavioral indicators, such as gestures, tone, or posture, to assess changes in emotional state that indicate the success or failure of the mediation.
4. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def norm_mediation(situation_description, dialogue, dialogue_norms, agent_description):
    sys_prompt = """
You are an expert in social science and conflict resolution, specializing in analyzing interpersonal dynamics and social norms. Your role is to accurately detect conflicting norms in dialogues and provide effective mediation strategies that facilitate resolution.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **DIALOGUE** and **Norms** (summarized per agent), identify **conflicting norms**. A norm conflict occurs when:
- An agent is expected to adhere to opposing behaviors.
- An agent’s actions contradict another agent’s norm.
- An injunctive norm (a directive) conflicts with another norm that the agent is also expected to follow.
After detecting conflicts, propose a mediation strategy that:
- Recognizes the underlying causes of the conflict.
- Recommends a feasible resolution based on the nature of the conflicting norms.
- Suggests practical communication strategies to help the agents resolve their differences.

### **SITUATION DESCRIPTION**: 
{situation_description}

### **DIALOGUE**: 
{dialogue}

### **Norms**: 
{dialogue_norms}

### **AGENT DESCRIPTION**: 
{agent_description}

### **OUTPUT FORMAT**:
Output in JSON format:
{{
  "id": {{
    "conflict_norms": ["norm description", "..."],
    "conflict_agents": ["name", "..."],
    "details": "Provide insights into their emotional state post-resolution and any significant changes in behavior.",
    "mediation_strategy": "Propose a resolution strategy based on the conflicting norms and agent descriptions."
  }}
}}

### **EXAMPLE OUTPUT**:
{{
  "1": {{
    "conflict_norms": ["Tom must have a quiet, distraction-free environment to work.", "Sophie must be able to conduct business calls without interruptions."],
    "conflict_agents": ["Tom", "Sophie"],
    "details": "Tom requires a quiet environment to work, while Sophie needs to make business calls, which may cause noise and distractions, violating Tom's need for a quiet space.",
    "mediation_strategy": "Suggest designated quiet hours for Tom and scheduled call times for Sophie to minimize disruption."
  }},
  "2": {{
    "conflict_norms": ["John should enjoy a peaceful environment.", "Sophie must be able to conduct business calls freely."],
    "conflict_agents": ["John", "Sophie"],
    "details": "John's desire for peace and quiet conflicts with Sophie's need to speak loudly on a business call, disturbing the peaceful environment John requires.",
    "mediation_strategy": "Introduce noise-canceling solutions or a separate space for Sophie to take calls without disturbing John."
  }},
}}

### **ATTENTION**:
1. Focus on the **norms** that are in **direct contradiction** with each other. For example, a conflict between a norm that requires silence and another that requires loud communication.
2. Provide a **brief explanation** for each conflict, explaining why the two norms are in contradiction.
3. Do not output anything except the detected conflicts in the specified format.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def mediation_interaction(situation_description, agent_description, social_network, dialogue, mediation_strategy):
    sys_prompt = """
You are an experienced master of mediating contradictions. You can use delicate and euphemistic expressions based on existing strategies to reconcile both sides.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **SITUATION DESCRIPTION**, **AGENT DESCRIPTION**, **DIALOGUE**, and **MEDIATION STRATEGY**, simulate a realistic continuation of the conversation where a **mediator agent** intervenes effectively to resolve the conflict. The mediator's role encompasses:

1. **Analyze Conflict Dynamics**:
    - Pinpoint core tension sources (e.g., competing norms, miscommunication, conflicting values).
    - Recognize power imbalances or emotional triggers affecting the dialogue.
    
2. **Apply Mediation Strategy**:
    - Implement **active listening, neutral reframing, or interest-based negotiation** as outlined in the strategy.
    - Suggest realistic solutions aligning with **shared goals** and respecting individual norms.
    
3. **Simulate Dialogue Continuation**: Construct a **natural dialogue progression** showing:
    - **Expression & Behavior**: Express non-verbal cues (e.g., open posture, calming gestures) and mediation steps (e.g., establishing ground rules, collaborative environment fostering).
    - **Chat Content**: Employ empathetic language, clarifying queries, and focus on solutions.
    - **Conflict Resolution**: Direct agents to discernible, actionable resolutions (e.g., compromise, norm prioritization).

### **SITUATION DESCRIPTION**: 
{situation_description}

### **AGENT DESCRIPTION**: 
{agent_description}

### **SOCIAL NETWORK**:
{social_network}

### **DIALOGUE**: 
{dialogue}

### **CONFLICT NORMS & MEDIATION STRATEGY**: 
{mediation_strategy}

### **TASK**:
Generate the **new conversation** focusing on the mediator's role. The mediator should:
1. Validate the conflict and concerns of each party equally.
2. Navigate practical solutions while encouraging mutual cooperation.
3. Assist agents in reaching a consensus or compromise.
   
### **OUTPUT FORMAT**:
Output in JSON format (maximum 10 rounds):
{{
    "round_id": {{
        "speaker": "The name of the agent speaking",
        "expression": "A detailed depiction of the agent's facial expression or tone showing engagement with the mediation process",
        "action": "A specific description of the agent's body language or actions reflecting shifts in the dialogue",
        "chat_content": "The actual spoken words or dialogue content driven towards conflict resolution"
    }}
}}

### **EXAMPLE OUTPUT**:
{{
    "1": {{
        "speaker": "Mediator",
        "expression": "calm and focused",
        "action": "steps into the middle, hands open to bridge understanding",
        "chat_content": "I can hear the passion and urgency here. Tom, quiet is crucial for your concentration, while Sophie benefits from collaborative energy. How can both needs be met creatively?"
    }},
    "2": {{
        "speaker": "Tom",
        "expression": "considering",
        "action": "rubs chin thoughtfully",
        "chat_content": "I really need uninterrupted time from 10 AM to 12 PM for my deep work."
    }},
    "3": {{
        "speaker": "Sophie",
        "expression": "open-minded",
        "action": "leans back, nodding slightly",
        "chat_content": "I can see how that helps. Maybe I can adjust my schedule to use quieter activities like planning during those times."
    }},
    "4": {{
        "speaker": "Mediator",
        "expression": "encouraging",
        "action": "draws a visual plan on the whiteboard",
        "chat_content": "That's a great step. Also, considering that the east wing has pods that enhance quiet, can we explore using them as part of a flexible work environment?"
    }},
    "5": {{
        "speaker": "Tom",
        "expression": "hopeful",
        "action": "smiles slightly, relaxing his posture",
        "chat_content": "I think pods would be a good complement if they’re available."
    }},
    "6": {{
        "speaker": "Sophie",
        "expression": "agreeable",
        "action": "marks scheduling options on her tablet",
        "chat_content": "Agreed, I’ll book them post-noon for calls and use headphones in the morning. Flexible scheduling might actually work well."
    }},
    "7": {{
        "speaker": "Mediator",
        "expression": "satisfied",
        "action": "captures decisions on the 'Collaboration Agreement' chart",
        "chat_content": "To conclude: Tom will have quiet during 10-12, Sophie adapts tasks accordingly, and we’ll review this arrangement bi-weekly."
    }}
}}

### **ATTENTION**:
1. Ensure the **mediator's intervention** remains balanced, unbiased, and aimed at facilitating practical solutions, backed by gestures and body language highlighting their role.
2. Keep empathy and collaboration at the core of the mediator's dialogue and actions.
3. Verify that the proposed solutions are realistic, aligning with the initial conflict while being feasible and considerate.
4. Integrate expressive body language and action descriptions across the original and extended dialogues to showcase emotional and behavioral shifts during mediation.
5. Present both the original and revised dialogues with the mediator's intervention clearly depicted.
6. Limit to 10 rounds.
7. The output format should strictly follow the JSON structure.
""".removeprefix('\n')
    return sys_prompt, user_prompt
