def situation_agent():
    sys_prompt = """
You are an imaginative and experienced social scientist who can imagine a real scenario to begin your research. You have a knack for succinctly articulating the contents of the scenario, without unnecessary verbosity.
""".removeprefix('\n')
    user_prompt = """
GOAL: Imagine and describe a real-life situation where social norms might conflict or require mediation. The scene should involve a diverse group of people in a specific setting with distinct perspectives or behaviors, leading to potential disagreement or misalignment of expectations.

### **OUTPUT REQUIREMENTS**:
1. **SITUATION DESCRIPTION**: Describe the physical setting, the event taking place, and any relevant background that sets the context for the scenario. Include details about:
    - **Type of Location**: Identify where the scenario is set, such as a cafe, park, office, or train, to anchor the physical setting.
    - **Event or Activity**: Describe what is taking place within that setting (e.g., a business meeting, social gathering, public commute), highlighting the nature of interactions expected.
    - **External Conditions**: Note any environmental or situational factors that could influence interactions, such as the time of day, noise levels, weather conditions, or any unusual occurrences like a power outage.

2. **AGENT DESCRIPTION**: Introduce the key characters in the situation, focusing on their backgrounds, goals, and characteristics. For each character, provide:
    - **Name**: Assign a name to each character for personalization and clarity in interactions.
    - **Role and Identity**: Describe their role or position in the situation (e.g., student, businessperson, retiree).
    - **Key Traits**: Summarize their personality traits, motivations, and any particular behaviors that could lead to conflict or differing perspectives.
    - **Potential Conflict**: Briefly mention what might cause tension or disagreement between characters (e.g., differing expectations, clashing values).
    - **Dynamic Properties**:
        - **Stress Level**: Numerical value (0-100) indicating the character's stress.
        - **Current Action**: Specific behavior (e.g., "typing vigorously").
    
3. **SOCIAL NETWORK**: Represent the relationships between characters.
   - Categorize as Cooperative/Conflicted/Neutral.  
   - Quantify relationship strength with weights:  
     - `+1` = Strong cooperation  
     - `-1` = Strong conflict  
     - `0` = Neutral  
   - Provide a **relationship network** matrix of all agent pairs.

### **EXAMPLE OUTPUT**:
{
    "situation_description": {
        "type_of_location": "A small cafe during the morning rush hour.",
        "event_or_activity": "The cafe is crowded with customers, including those grabbing quick coffees before work and others who plan to stay and work on laptops. The staff is busy and slightly overwhelmed, leading to delays in service.",
        "external_conditions": "A power outage earlier that morning has left the cafe operating without Wi-Fi."
    },
    "agent_description": 
        {
            "Tom": {
                "role": "Freelance graphic designer",
                "key_traits": "Highly focused, values quiet workspace",
                "potential_conflict": "Frustrated by Sophie's loud phone calls and lack of Wi-Fi",
                "dynamic_properties": {
                    "stress_level": 85,
                    "current_action": "Tapping fingers impatiently on laptop"
                }
            },
            "Sophie": {
                "role": "Business executive",
                "key_traits": "Authoritative, constantly on-the-go",
                "potential_conflict": "Unaware her loud conversation is disruptive",
                "dynamic_properties": {
                    "stress_level": 70,
                    "current_action": "Engaging in loud phone calls"
                }
            },
            "John": {
                "role": "Retiree",
                "key_traits": "Soft-spoken, values peace and quiet",
                "potential_conflict": "Dislikes disturbances in his environment",
                "dynamic_properties": {
                    "stress_level": 60,
                    "current_action": "Sipping coffee quietly"
                }
            },
            "Maria": {
                "role": "Cafe staff member",
                "key_traits": "Friendly but under stress due to workload",
                "potential_conflict": "Overwhelmed by customer demands",
                "dynamic_properties": {
                    "stress_level": 90,
                    "current_action": "Taking and preparing orders hurriedly"
                }
            },
            "Carlos": {
                "role": "Tourist",
                "key_traits": "Unfamiliar with local customs, relaxed",
                "potential_conflict": "Occupying space without much order, causing tension",
                "dynamic_properties": {
                    "stress_level": 30,
                    "current_action": "Sitting and observing surroundings"
                }
            }
        },
    "social_network": {
        "nodes": ["Tom", "Sophie", "John", "Maria", "Carlos"],
        "edges": [
            {"source": "Tom", "target": "Sophie", "weight": -0.8},
            {"source": "Tom", "target": "Maria", "weight": 0.5},
            {"source": "Sophie", "target": "Maria", "weight": 0},
            {"source": "John", "target": "Tom", "weight": 0},
            {"source": "John", "target": "Sophie", "weight": -0.6},
            {"source": "Maria", "target": "Carlos", "weight": -0.4}
        ]
    }
}

### **ATTENTION**:
1. Dynamic Properties: The stress level and action are crucial to understanding the immediate emotional state and behavior of each character, influencing their interactions and relationships.
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
GOAL: Based on the provided **AGENT DESCRIPTION** and **SITUATION DESCRIPTION**, generate 3 personal social norms for the agent. The norms should reflect his/her personality, values, and behavioral tendencies in the given situation. Personal norms should guide the agent’s actions, expectations, and interactions in this context.

### **OUTPUT REQUIREMENTS**:
Generate **1-3 personal norms** in the following **JSON** format. Each norm should reflect the agent’s preferences, priorities, and behavioral patterns, taking into account his/her identity, role, and the specific setting.

### **AGENT DESCRIPTION**: 
{agent_description}

### **SITUATION DESCRIPTION**: 
{situation_description}

### **DESIRED FORMAT**:
Output in JSON format:
{{
    "id": {{
        "type": "descriptive/injunctive",
        "content": "description",
        "subject": "subject",
        "predicate": "predicate",
        "object": "object",
        "utility": "score",
    }}
}}

- id: the index of the created norm.
- **$\theta \in {{descriptive, injunctive}}$**: The type of norm:
  - **descriptive**: Reflects behaviors that the agent typically follows or expects to see in others.
  - **injunctive**: Reflects the agent’s personal rules or expectations for what should be done in a situation.
- **content**: A brief description of the norm in a subject-verb-object structure.
- **subject**: The person or entity the norm applies to (e.g., “everyone,” “customers”).
- **predicate**: The behavior or rule being specified (e.g., “must not speak loudly,” “should always respect personal space”).
- **object**: The target or focus of the norm (e.g., “the phone,” “the environment”). If none, set "object": "None."
- **utility**: A score from 1 to 100, representing how important the norm is for the agent in this situation.

### **EXAMPLE OUTPUT**:
{{
    "1": {{
        "type": "injunctive",
        "content": "Tom must have a quiet, distraction-free space to work.",
        "subject": "Tom",
        "predicate": "must have",
        "object": "a quiet, distraction-free space",
        "utility": 90,
    }},
    "2": {{
        "type": "injunctive",
        "content": "Tom should avoid excessive noise when others are working.",
        "subject": "Tom",
        "predicate": "should avoid",
        "object": "excessive noise",
        "utility": 80,
    }},
    "3": {{
        ...
    }}
}}
### **ATTENTION**:
1. Ensure that each personal norm reflects the agent’s characteristics, values, and preferences.
2. Generate a balanced mix of descriptive and injunctive norms.
3. Use clear, concise language and make sure the norms are relevant to the scenario provided.
4. Do not output anything except the content in JSON format.
""".removeprefix('\n')
    return sys_prompt, user_prompt


def generate_dialogue(situation_description, agent_description, social_norms, personal_norms):
    sys_prompt = """
You are a culture-aware system that can generate natural conversations according to different people's profiles and norms.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Simulate a conversation between the agents based on the provided **SITUATION DESCRIPTION**, **AGENT DESCRIPTIONS**, **SITUATION NORMS**, and **PERSONAL NORMS**. Each agent should behave according to their personality and norms, which will drive their actions and responses. The conversation should reflect their behavior, motivations, and potential conflicts due to differing expectations.

### **SITUATION DESCRIPTION**:
{situation_description}

### **AGENT DESCRIPTIONS**:
{agent_description}

### **SITUATION NORMS**:
{social_norms}

### **PERSONAL NORMS**:
{personal_norms}

### **GOAL FOR SIMULATION**:
- Each agent will act according to their **PERSONAL NORMS**. 
- The conversation should reflect **potential conflicts** based on the agents’ differing expectations and behaviors.
- The dialogue should show how these agents negotiate their personal norms and possibly clash with each other, causing tension or resolution.

### **OUTPUT FORMAT**:
The generated conversation should be formatted with each line following this format:
name: [what he or she said]

### **EXAMPLE OUTPUT**:
Tom: [Tom’s statement based on his frustration over the noisy environment and lack of Wi-Fi.]
Sophie: [Sophie responds, showing little concern for the noise, as she’s focused on her work-related call.]
John: [John, annoyed by the noise and chaos, tries to voice his discomfort.]
Maria: [Maria, trying to remain calm, offers an explanation but is struggling with the situation.]
Carlos: [Carlos, unaware of the issues around him, continues to relax in his seat.]

### **ATTENTION**:
1. Ensure that each agent speaks in a way that reflects their personality, behaviors, and motivations.
2. Prioritize the agents’ **PERSONAL NORMS** in driving their actions, especially when they experience frustration or discomfort.
3. The conversation should capture **potential conflicts**—for example, Tom’s frustration with the noise, Sophie’s indifference to the disruption, and John’s discomfort.
4. **Avoid overly dramatic or exaggerated responses**; focus on everyday tensions.
5. Do not output anything except the dialogue in the format specified.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def summarize_dialogue_norms(situation_description, agent_description, dialogue):
    sys_prompt = """
You are an experienced sociologist who can accurately and comprehensively extract norms from people's daily communication. You have a knack for succinctly articulating the contents of these norms, without unnecessary verbosity.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Analyze the provided **dialogue** and extract the norms that each character follows, expects, or implies in their speech. Assign these norms to the corresponding character based on their statements and behaviors.

### **SITUATION DESCRIPTION**:
{situation_description}

### **AGENT DESCRIPTIONS**:
{agent_description}

### **DIALOGUE**: 
{dialogue}

### **TASK**:
For each character, identify and summarize the norms that appear in their dialogue. Each norm should reflect:
- **Explicit Norms**: Norms directly stated by the character (e.g., "People should not talk loudly in cafes").
- **Implied Norms**: Norms inferred from the character’s statements or behaviors (e.g., If a character complains about noise, they likely hold a norm that public spaces should be quiet).

The norms should be **concise** and **structured**, categorized as:
- **Descriptive Norms**: What people typically do in this situation.
- **Injunctive Norms**: What the character believes people should or should not do.

### **OUTPUT FORMAT**:
The output should be structured in **JSON format**, mapping each character to their respective norms.
```
{{
    "character_name": {{
        "id": {{
            "type": "descriptive/injunctive",
            "content": "Brief description of the norm",
            "subject": "Who the norm applies to",
            "predicate": "Action associated with the norm",
            "object": "Object or target of the norm",
            "source": "explicit/implied"
        }}
    }}
}}
```

### **EXAMPLE OUTPUT**:
{{
  "Tom": {{
    "1": {{
      "type": "injunctive",
      "content": "Public places should be quiet for work",
      "subject": "people in cafes",
      "predicate": "should keep",
      "object": "quiet environment",
      "source": "implied"
    }},
    "2": {{
        ...
    }}
  }},
  "Sophie": {{
    "1": {{
      "type": "injunctive",
      "content": "Business calls should be allowed in public places",
      "subject": "business professionals",
      "predicate": "should be able to make",
      "object": "calls in public",
      "source": "explicit"
    }},
    "2": {{
        ...
    }}
  }}
}}

### **ATTENTION**:
1. Identify both **explicit** and **implied** norms from the dialogue.
2. Classify norms as **descriptive** (what people do) or **injunctive** (what people should/shouldn’t do).
3. Ensure norms are **brief** and **structured clearly** for each character.
4. Do not output anything except the structured JSON data.
""".removeprefix('\n')
    return sys_prompt, user_prompt

# def judge_norms(situation_description, dialogue_norms):
#     sys_prompt = """
# You are an AI assistant tasked with evaluating dialogue based on a given set of norms. Your goal is to analyze each line of dialogue and determine whether it adheres to (A), violates (V), or is not related to (N) each norm listed.
# """.removeprefix('\n')
#     user_prompt = f"""
# GOAL: For each line of dialogue provided, label whether the agent’s behavior adheres to (A), violates (V), or is not related to (N) each of the following **Norms**, and provide a brief explanation. The norms come from both the **NORMS**.

# ### **SITUATION DESCRIPTION**:
# {situation_description}

# ### **NORMS IN DIALOGUE**:
# {dialogue_norms}

# ### **GOAL FOR SIMULATION**:
# For each **norms** in dialogue, check which **norm** are adhered to(A), violated (V), or not related (N). For each **norm**, print the corresponding label: A, V, or N, then provide an explanation.

# ### **OUTPUT FORMAT**:
# For each line in the original dialogue, you first repeat it, and then start a line with which norm listed above it is adhered to(A), violated (V), or not related (N). labels are seperated with blank. Then on another line, briefly tell me the reasons for making this judgment.

# ### **EXAMPLE OUTPUT**:

# Tom: This is ridiculous, no Wi-Fi and the noise level is unbearable. How am I supposed to get any work done?
# N A V N
# This sentence is unrelated to the rule of no eating in the library...

# ### **ATTENTION**:
# 1. Carefully analyze each dialogue line and decide if the action described adheres to, violates, or is not related to each norm.
# 2. Ensure each norm is properly labeled for each dialogue line.
# 3. Focus on the **behavioral** aspects of the dialogue, not just the content of the message.
# 4. Do not output anything except the labeled norms for each dialogue line.
# """.removeprefix('\n')
#     return sys_prompt, user_prompt

def detect_conflict(dialogue, dialogue_norms):
    sys_prompt = """
You are a social scientist with rich experience in dealing with conflicts. You can accurately detect conflicts in dialogue and distinguish right from wrong based on public opinions.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the dialogue and identified norms, identify **conflicting norms**. Norms conflict if one agent is expected to adhere to opposing behaviors or if their actions violate each other’s norms. Specifically, a conflict occurs when one norm is **injunctive** (a directive) and it contradicts another norm that the agent is also expected to follow.

Additionally, for each conflict, label whether the norms are based on **majority opinion**, **minority opinion**, or if they represent **harmful ideas** from an ethical or moral perspective.

### **CONFLICT DEFINITION**:
A conflict arises between two norms if:
1. **Norm A** requires a specific behavior (e.g., "must be quiet"), while **Norm B** requires a behavior that contradicts it (e.g., "must speak loudly").
2. The two norms are labeled as **A (Adhere)** or **V (Violate)** for one or more agents in such a way that they cannot both be followed simultaneously.

### **GOAL**:
You will be provided with a list of norms labeled as **A**, **V**, or **N** for each line of dialogue. Identify which norms conflict with each other. For each detected conflict, label whether the norms represent:
- **Majority Opinion**: Norms that align with the behavior or expectations of the majority of people in a given social context.
- **Minority Opinion**: Norms that align with the behavior or expectations of only a small group of people.
- **Harmful Opinion**: Norms that might be considered unethical, morally harmful, or contrary to the well-being of others.

### **CONFLICT DEFINITION**:
A conflict arises between two norms if:
1. **Norm A** requires a specific behavior (e.g., "must be quiet"), while **Norm B** requires a behavior that contradicts it (e.g., "must speak loudly").
2. The two norms are labeled as **A (Adhere)** or **V (Violate)** for one or more agents in such a way that they cannot both be followed simultaneously.


### **OUTPUT FORMAT**:
For each detected conflict, output the following format:
- **Conflicting Norms**:
   - **Norm 1**: [norm description or name]
   - **Norm 2**: [norm description or name]
   - **Conflicting Agents**: [list of agents involved in the conflict]
   - **Norm 1 Opinion**: [majority opinion / minority opinion / harmful opinion]
   - **Norm 2 Opinion**: [majority opinion / minority opinion / harmful opinion]
   - **Explanation**: [brief explanation of why the norms conflict and why you label the norm as majority/minority/harmful opinion.]

### **EXAMPLE OUTPUT**:
1. **Conflicting Norms**:
   - **Norm 1**: "Tom must have a quiet, distraction-free environment to work."
   - **Norm 2**: "Sophie must be able to conduct business calls without interruptions."
   - **Conflicting Agents**: ["Tom", "Sophie"]
   - **Norm 1 Opinion**: **Majority Opinion**
   - **Norm 2 Opinion**: **Minority Opinion**
   - **Explanation**: Tom requires a quiet environment to work, while Sophie needs to make business calls, which may cause noise and distractions, violating Tom's need for a quiet space. Quiet working environments are generally expected by the majority, but conducting business calls publicly is often prioritized by business professionals, making it a minority opinion.

2. **Conflicting Norms**:
   - **Norm 1**: "John should enjoy a peaceful environment."
   - **Norm 2**: "Sophie must be able to conduct business calls freely."
   - **Conflicting Agents**: ["John", "Sophie"]
   - **Norm 1 Opinion**: **Majority Opinion**
   - **Norm 2 Opinion**: **Minority Opinion**
   - **Explanation**: John's desire for peace and quiet conflicts with Sophie’s need to speak loudly on a business call, disturbing the peaceful environment John requires. The expectation of quiet in public spaces is a majority opinion, while prioritizing business calls in public may be considered a minority opinion.

### **DIALOGUE**:
{dialogue}

### **NORMS IN DIALOGUE**:
{dialogue_norms}

### **ATTENTION**:
1. Focus on the **norms** that are in direct contradiction with each other. 
2. For each conflicting norm pair, label both norms as **majority opinion**, **minority opinion**, or **harmful opinion**.
3. Provide a **brief explanation** for each conflict, explaining why the two norms are in contradiction and why each norm is labeled as **majority**, **minority**, or **harmful**.
4. Do not output anything except the detected conflicts in the specified format.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def mediator_strategy(situation_description, agent_description, dialogue, conflict):
    sys_prompt = """
You are an experienced mediator who is good at handling conflicts and developing thoughtful and comprehensive mediation strategies. Your mediation strategies represent the opinions of the public and always make both sides satisfied.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **SITUATION DESCRIPTION**, **AGENT DESCRIPTIONS**, **DIALOGUE**, and **CONFLICT DETECTION RESULTS**, imagine a virtual mediator. The mediator should provide **brief guidance on how to mediate the conflict** between the agents, focusing on how to resolve the conflicting norms.

### **SITUATION DESCRIPTION**: 
{situation_description}
### **AGENT DESCRIPTIONS**: 
{agent_description}
### **DIALOGUE**: 
{dialogue}
### **CONFLICT DETECTION RESULTS**: 
{conflict}

### **TASK**:
Based on the above information, the mediator should:
1. **Acknowledge the conflict**: Briefly summarize the key issues causing the conflict.
2. **Suggest a path forward**: Provide a **short and practical solution** to help the agents resolve the conflict while considering their personal norms and values.
3. **Propose mediation strategies**: Offer **neutral and empathetic guidance** to encourage cooperation between the agents.

### **OUTPUT FORMAT**:
**Proposed Solution**: [Suggest a practical solution that addresses both agents’ concerns]
**Mediation Strategy**: [Provide guidance for how the mediator should facilitate dialogue and encourage cooperation]

### **EXAMPLE OUTPUT**:

**Proposed Solution**:
  Suggest creating a designated area for quiet work in the cafe, while allowing Sophie to take calls in a separate area where noise won’t disturb others. Maria could help manage this by guiding customers to appropriate spaces based on their needs.

**Mediation Strategy**:
  The mediator should acknowledge each agent’s needs and frustrations. For example, they could say:
  "Tom, I understand how important a quiet environment is for your work. Sophie, I know these calls are urgent. How about we set up a quiet zone for those who need to focus, and create a designated area for business calls? This way, both of your needs are met without causing disruptions."

### **ATTENTION**:
1. **Empathy and Neutrality**: The mediator must remain neutral and empathetic to both agents' needs.
2. **Practicality**: The proposed solution should be easy to implement and fair to all parties.
3. **Diplomatic Language**: Use neutral, diplomatic language that encourages cooperation.
4. **Focus on Conflict Resolution**: Aim to create a balanced solution that acknowledges and addresses the conflicting norms.

Do not output anything except the mediator's guidance in the specified format.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def mediate_dialogue(situation_description, agent_description, dialogue, mediator_strategy):
    sys_prompt = """
You are an experienced master of mediating contradictions. You can use delicate and euphemistic expressions based on existing strategies to reconcile both sides.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **SITUATION DESCRIPTION**, **AGENT DESCRIPTIONS**, **DIALOGUE**, and **MEDIATION STRATEGY**, simulate the continuation of the conversation, where a **mediator agent** intervenes. The mediator will guide the conversation and propose solutions to resolve the conflict. 

The output should include:
The **new dialogue** with the mediator's intervention, showing how the mediator helps to resolve the conflict.

### **SITUATION DESCRIPTION**: 
{situation_description}
### **AGENT DESCRIPTIONS**: 
{agent_description}
### **ORIGINAL DIALOGUE**: 
{dialogue}
### **MEDIATION STRATEGY**: 
{mediator_strategy}

### **TASK**:
Generate the **new conversation** with the mediator's intervention. The mediator should:
1. Acknowledge the conflict between the agents.
2. Suggest practical solutions and encourage cooperation.
3. Help the agents move toward a resolution and come to a consensus.

### **OUTPUT FORMAT**:
Provide the conversation where the mediator intervenes, guiding the agents towards resolving the conflict. The conversation should be formatted with each line following this format:
name: [what he or she said]

### **EXAMPLE ORIGINAL DIALOGUE**:
Tom: [This is ridiculous, no Wi-Fi and the noise level is unbearable. How am I supposed to get any work done?]
Sophie: [No, I need this contract signed by noon. We can’t afford to delay the launch. Yes, just send me the final draft now!]
John: [I can’t hear myself think with all this noise! This isn’t the place for peace anymore.]
Maria: [I’m really sorry, but we’re doing our best. Could you try to lower the volume, please?]

### **EXAMPLE OUTPUT**:
Mediator: [I understand that each of you has different needs. Tom, I can see how important a quiet space is for your work. Sophie, I recognize that your phone calls are crucial for your work deadlines. John, you’re seeking peace and quiet for your relaxation. What if we create a quiet area for those who need to focus, while Sophie could take calls in a designated area where noise won’t be an issue?]
Tom: [That sounds better. If there’s a place where I can work without interruptions, I’m happy with that.]
Sophie: [I agree. I can take my calls in another area, as long as I can still get the work done. We need to make sure this gets resolved fast.]
John: [A quiet space for those who need it sounds good to me. I’m glad we’re finding a solution.]
Maria: [I can help guide everyone to these spaces. This way, we can all work in peace, and you’ll get the privacy you need for calls.]

---

### **ATTENTION**:
1. Make sure the **mediator's intervention** is clear, neutral, and aimed at facilitating a balanced solution for all parties involved.
2. Focus on **maintaining empathy** and **cooperation** in the mediator's speech.
3. Ensure that the **solution proposed** is practical, feasible, and tailored to the conflict identified in the original dialogue. 4. Output **both the original and the new dialogue** with the mediator’s intervention clearly shown.  
Do not output anything except the original and new dialogue in the specified format.
""".removeprefix('\n')
    return sys_prompt, user_prompt

def eval_conflict(old_dialogue, new_dialogue):
    sys_prompt = """
You are a social scientist with rich experience in dealing with conflicts. You can accurately detect conflicts in dialogue.
""".removeprefix('\n')
    user_prompt = f"""
GOAL: Based on the provided **original dialogue**, **new dialogue with mediator’s intervention**, evaluate whether the conflicting parties (agents) have reached a consensus. The consensus should be determined by whether the agents have agreed on a practical solution and have expressed willingness to cooperate.

### **Original Dialogue**:  
{old_dialogue}

### **New Dialogue with Mediator's Intervention**:  
{new_dialogue}

### **TASK**:
Determine if the mediator’s intervention successfully resolved the conflict and led to a consensus between the agents. Evaluate if the agents:
- **Acknowledge the conflict** and agree to a **common solution**.
- **Express willingness** to respect the proposed solution or compromise.
- **Cooperate** towards a resolution that meets both parties' needs.

### **OUTPUT**:
**Consensus Evaluation**:
   - **Has consensus been reached?**: [Yes/No]
   - **Explanation**: [Brief explanation on why the agents reached or did not reach consensus. Describe the key factors that led to the agreement or disagreement.]

### **EXAMPLE OUTPUT**:
**Has consensus been reached?**: Yes  
   **Explanation**: Both Tom and Sophie agreed to the proposed solution of a designated quiet zone for work and a separate area for business calls. Tom is satisfied with a quieter space, and Sophie is willing to take calls in a designated area. John is also happy with the new arrangement, which allows for peace and quiet, and Maria has committed to guiding customers to the appropriate spaces.
   
### **ATTENTION**:
1. Carefully analyze the **agents’ reactions** to the mediator’s intervention, focusing on whether they agree to the proposed solution or show resistance.
2. Consider both verbal and non-verbal cues in the dialogue to assess whether the agents are willing to cooperate.
3. Ensure that the **solution** is feasible and practical based on the agents’ needs and the context of the situation.
4. Do not output anything except the evaluation of consensus in the specified format.
""".removeprefix('\n')
    return sys_prompt, user_prompt