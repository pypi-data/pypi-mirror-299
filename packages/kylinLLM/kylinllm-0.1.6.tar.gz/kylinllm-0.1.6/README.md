kylinLLM

kylinLLM 是一个用于处理大型语言模型（Large Language Models）相关任务的 Python 库。它提供了记忆管理、认知增强、分类和角色扮演等功能。

## 安装

使用 pip 安装该包：

```
pip install kylinLLM
```

## 功能模块

### dialogue_summarize()

生成用于对话总结的提示。

## Returns:

- `str`: 返回一个提示文本，用于引导模型总结对话的关键点。

## Example:
```
from kylinLLM.memory import Prompt 
summary_prompt = Prompt.dialogue_summarize() 
print(summary_prompt) 
```


### targeted_extraction()

生成用于定向信息提取的提示。

## Returns:

- `str`: 返回一个提示文本，用于引导模型提取与当前上下文最相关的信息。

## Example:

```
from kylinLLM.memory import Prompt
extraction_prompt = Prompt.targeted_extraction() 
print(extraction_prompt) 
```



### memory_organize()

生成用于记忆整理的提示。

## Returns:

- `str`: 返回一个提示文本，用于引导模型识别对话历史中的模式或重复主题。

## Example:

```
from kylinLLM.memory import Prompt 
organize_prompt = Prompt.memory_organize() 
print(organize_prompt) 
```



### introspection_summary()

生成用于自省总结的提示。

## Returns:

- `str`: 返回一个提示文本，用于引导模型识别可能对未来参考重要的细节。

## Example:

```
from kylinLLM.memory import Prompt 
introspection_prompt = Prompt.introspection_summary() print(introspection_prompt) 
```



### information_timeliness()

生成一个用于评估给定信息时效性的提示。

**返回：**
- `str`：返回一个提示文本，引导模型评估信息在当前上下文中的时效性或相关性。

**示例：**
```python
from kylinLLM.memory import Prompt
timeliness_prompt = Prompt.information_timeliness()
print(timeliness_prompt)
```

### user_impression()

生成一个基于交互历史分析用户印象的提示。

**返回：**
- `str`：返回一个提示文本，指导模型根据过去的交互评估用户的观点或态度。

**示例：**
```python
from kylinLLM.memory import Prompt
impression_prompt = Prompt.user_impression()
print(impression_prompt)
```

### problem_decomposition()

生成一个将复杂问题分解为较小子问题的提示。

**返回：**
- `str`：返回一个提示文本，指导模型将复杂问题分解为更易管理的部分。

**示例：**
```python
from kylinLLM.memory import Prompt
decomposition_prompt = Prompt.problem_decomposition()
print(decomposition_prompt)
```

### proactive_problem_solving()

生成一个用于识别潜在问题并提出解决方案的提示。

**返回：**
- `str`：返回一个提示文本，指导模型预测问题并提出预防性解决方案。

**示例：**
```python
from kylinLLM.memory import Prompt
proactive_prompt = Prompt.proactive_problem_solving()
print(proactive_prompt)
```

### divergent_questioning()

生成一个创建多样化和发人深省的问题的提示。

**返回：**
- `str`：返回一个提示文本，指导模型就给定主题提出各种有见地的问题。

**示例：**
```python
from kylinLLM.memory import Prompt
questioning_prompt = Prompt.divergent_questioning()
print(questioning_prompt)
```

### problem_classification()

生成一个将给定问题分类到适当类型或领域的提示。

**返回：**
- `str`：返回一个提示文本，指导模型将问题分类到合适的类别或领域。

**示例：**
```python
from kylinLLM.memory import Prompt
classification_prompt = Prompt.problem_classification()
print(classification_prompt)
```

### introspection_summary()

生成一个用于对话内省和总结的提示。

**返回：**
- `str`：返回一个提示文本，指导模型识别和总结交互中的重要细节。

**示例：**
```python
from kylinLLM.memory import Prompt
introspection_prompt = Prompt.introspection_summary()
print(introspection_prompt)
```

### traffic_diversion()

生成一个用于对传入请求进行分类和导向的提示。

**返回：**
- `str`：返回一个提示文本，指导模型将传入请求分类并导向适当的处理渠道或部门。

**示例：**
```python
from kylinLLM.classification import Prompt
diversion_prompt = Prompt.traffic_diversion()
print(diversion_prompt)
```

### attention_level()

生成一个用于评估信息或请求应受到的关注度或优先级的提示。

**返回：**
- `str`：返回一个提示文本，指导模型评估信息或请求的重要性和紧急程度。

**示例：**
```python
from kylinLLM.classification import Prompt
attention_prompt = Prompt.attention_level()
print(attention_prompt)
```

### dialogue_completion()

生成一个用于预测对话或会话最可能的延续或完成的提示。

**返回：**
- `str`：返回一个提示文本，指导模型预测对话的下一步发展或结束。

**示例：**
```python
from kylinLLM.classification import Prompt
completion_prompt = Prompt.dialogue_completion()
print(completion_prompt)
```

### sentence_structure()

生成一个用于分析和分类给定句子的语法结构或类型的提示。

**返回：**
- `str`：返回一个提示文本，指导模型分析句子的语法结构并进行分类。

**示例：**
```python
from kylinLLM.classification import Prompt
structure_prompt = Prompt.sentence_structure()
print(structure_prompt)
```

### memory_tagging()

生成一个用于为信息生成适当标签的提示，以便于未来检索和分类。

**返回：**
- `str`：返回一个提示文本，指导模型为给定信息生成合适的标签或分类。

**示例：**
```python
from kylinLLM.classification import Prompt
tagging_prompt = Prompt.memory_tagging()
print(tagging_prompt)
```


### qa_matching()

生成一个用于将给定问题与知识库中最合适的答案匹配的提示。

**返回：**
- `str`：返回一个提示文本，指导模型从可用知识库中找到最适合给定问题的答案。

**示例：**
```python
from kylinLLM.strategy import Prompt
matching_prompt = Prompt.qa_matching()
print(matching_prompt)
```

### search_public_knowledge()

生成一个用于搜索和检索公共知识库中相关信息的提示。

**返回：**
- `str`：返回一个提示文本，指导模型从公共知识库中搜索和提取与当前查询相关的信息。

**示例：**
```python
from kylinLLM.strategy import Prompt
search_prompt = Prompt.search_public_knowledge()
print(search_prompt)
```

### strategy_matching()

生成一个用于识别和选择最适合给定情况或问题的策略的提示。

**返回：**
- `str`：返回一个提示文本，指导模型为给定情况选择最合适的策略。

**示例：**
```python
from kylinLLM.strategy import Prompt
strategy_match_prompt = Prompt.strategy_matching()
print(strategy_match_prompt)
```

### strategy_objective()

生成一个用于为选定策略定义明确和可实现目标的提示。

**返回：**
- `str`：返回一个提示文本，指导模型为选定的策略制定清晰、可达成的目标。

**示例：**
```python
from kylinLLM.strategy import Prompt
objective_prompt = Prompt.strategy_objective()
print(objective_prompt)
```

### strategy_completion()

生成一个用于制定完整计划以完成和实施所选策略的提示。

**返回：**
- `str`：返回一个提示文本，指导模型开发一个全面的计划来实施选定的策略。

**示例：**
```python
from kylinLLM.strategy import Prompt
completion_prompt = Prompt.strategy_completion()
print(completion_prompt)
```

### strategy_impact()

生成一个用于分析和预测实施所选策略的潜在影响的提示。

**返回：**
- `str`：返回一个提示文本，指导模型分析实施选定策略可能带来的影响。

**示例：**
```python
from kylinLLM.strategy import Prompt
impact_prompt = Prompt.strategy_impact()
print(impact_prompt)
```

### emotional_impact()

生成一个用于评估策略或回应对用户或受众可能产生的情感影响的提示。

**返回：**
- `str`：返回一个提示文本，指导模型评估策略或回应可能带来的情感影响。

**示例：**
```python
from kylinLLM.strategy import Prompt
emotional_prompt = Prompt.emotional_impact()
print(emotional_prompt)
```

### knowledge_extraction()

生成一个用于从给定信息或上下文中提取关键知识点或见解的提示。

**返回：**
- `str`：返回一个提示文本，指导模型从给定内容中提取重要的知识点或洞见。

**示例：**
```python
from kylinLLM.strategy import Prompt
extraction_prompt = Prompt.knowledge_extraction()
print(extraction_prompt)
```

### entity_extraction()

生成一个用于从给定文本中识别和提取重要实体的提示。

**返回：**
- `str`：返回一个提示文本，指导模型从文本中识别并提取重要实体（如名称、地点、组织等）。

**示例：**
```python
from kylinLLM.strategy import Prompt
entity_prompt = Prompt.entity_extraction()
print(entity_prompt)
```

### noise_identification()

生成一个用于检测和识别输入数据或上下文中任何噪声或无关信息的提示。

**返回：**
- `str`：返回一个提示文本，指导模型识别输入中的噪声或不相关信息。

**示例：**
```python
from kylinLLM.strategy import Prompt
noise_prompt = Prompt.noise_identification()
print(noise_prompt)
```

### plugin_selection()

生成一个用于选择最合适的插件或工具来协助执行当前任务或策略的提示。

**返回：**
- `str`：返回一个提示文本，指导模型选择最适合执行当前任务的插件或工具。

**示例：**
```python
from kylinLLM.strategy import Prompt
plugin_prompt = Prompt.plugin_selection()
print(plugin_prompt)
```
### education()

生成一个用于扮演教育者角色的提示。

**返回：**
- `str`：返回一个提示文本，指导模型提供清晰且引人入胜的解释以促进学习。

**示例：**
```python
from kylinLLM.role import Prompt
education_prompt = Prompt.education()
print(education_prompt)
```

### companionship()

生成一个用于扮演支持性伙伴角色的提示。

**返回：**
- `str`：返回一个提示文本，指导模型作为一个理解和支持的伙伴，提供同理心和友好的交谈。

**示例：**
```python
from kylinLLM.role import Prompt
companionship_prompt = Prompt.companionship()
print(companionship_prompt)
```

### medical()

生成一个用于提供医疗信息和建议的提示，同时包含免责声明。

**返回：**
- `str`：返回一个提示文本，指导模型提供医疗信息和建议，并声明非专业医疗人士的身份。

**示例：**
```python
from kylinLLM.role import Prompt
medical_prompt = Prompt.medical()
print(medical_prompt)
```

### super_ai()

生成一个用于展示高级问题解决和分析能力的提示。

**返回：**
- `str`：返回一个提示文本，指导模型在广泛的主题范围内展示先进的问题解决和分析能力。

**示例：**
```python
from kylinLLM.role import Prompt
super_ai_prompt = Prompt.super_ai()
print(super_ai_prompt)
```

### mystical()

生成一个用于提供神秘和精神传统见解的提示。

**返回：**
- `str`：返回一个提示文本，指导模型从各种神秘和精神传统中提供见解和观点，同时保持尊重和开放的态度。

**示例：**
```python
from kylinLLM.role import Prompt
mystical_prompt = Prompt.mystical()
print(mystical_prompt)
```

### psychological_counseling()

生成一个用于提供心理支持和一般建议的提示。

**返回：**
- `str`：返回一个提示文本，指导模型提供支持性倾听和一般建议，同时强调严重问题需要寻求专业帮助的重要性。

**示例：**
```python
from kylinLLM.role import Prompt
counseling_prompt = Prompt.psychological_counseling()
print(counseling_prompt)
```

### beauty()

生成一个用于提供美容和化妆技巧的提示。

**返回：**
- `str`：返回一个提示文本，指导模型提供美容和化妆建议，考虑各种皮肤类型、肤色和个人风格。

**示例：**
```python
from kylinLLM.role import Prompt
beauty_prompt = Prompt.beauty()
print(beauty_prompt)
```

### fitness_coach()

生成一个用于提供健身建议和动力支持的提示。

**返回：**
- `str`：返回一个提示文本，指导模型提供激励支持和一般健身建议，同时强调在开始任何新的锻炼计划前咨询医生的重要性。

**示例：**
```python
from kylinLLM.role import Prompt
fitness_prompt = Prompt.fitness_coach()
print(fitness_prompt)
```

### streamer()

生成一个用于扮演直播主播角色的提示。

**返回：**
- `str`：返回一个提示文本，指导模型以富有娱乐性和互动性的内容吸引观众，保持活跃和平易近人的形象。

**示例：**
```python
from kylinLLM.role import Prompt
streamer_prompt = Prompt.streamer()
print(streamer_prompt)
```

