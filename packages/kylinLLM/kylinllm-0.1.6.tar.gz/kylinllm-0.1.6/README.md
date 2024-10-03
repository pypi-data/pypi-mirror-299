kylinLLM

kylinLLM ��һ�����ڴ����������ģ�ͣ�Large Language Models���������� Python �⡣���ṩ�˼��������֪��ǿ������ͽ�ɫ���ݵȹ��ܡ�

## ��װ

ʹ�� pip ��װ�ð���

```
pip install kylinLLM
```

## ����ģ��

### dialogue_summarize()

�������ڶԻ��ܽ����ʾ��

## Returns:

- `str`: ����һ����ʾ�ı�����������ģ���ܽ�Ի��Ĺؼ��㡣

## Example:
```
from kylinLLM.memory import Prompt 
summary_prompt = Prompt.dialogue_summarize() 
print(summary_prompt) 
```


### targeted_extraction()

�������ڶ�����Ϣ��ȡ����ʾ��

## Returns:

- `str`: ����һ����ʾ�ı�����������ģ����ȡ�뵱ǰ����������ص���Ϣ��

## Example:

```
from kylinLLM.memory import Prompt
extraction_prompt = Prompt.targeted_extraction() 
print(extraction_prompt) 
```



### memory_organize()

�������ڼ����������ʾ��

## Returns:

- `str`: ����һ����ʾ�ı�����������ģ��ʶ��Ի���ʷ�е�ģʽ���ظ����⡣

## Example:

```
from kylinLLM.memory import Prompt 
organize_prompt = Prompt.memory_organize() 
print(organize_prompt) 
```



### introspection_summary()

����������ʡ�ܽ����ʾ��

## Returns:

- `str`: ����һ����ʾ�ı�����������ģ��ʶ����ܶ�δ���ο���Ҫ��ϸ�ڡ�

## Example:

```
from kylinLLM.memory import Prompt 
introspection_prompt = Prompt.introspection_summary() print(introspection_prompt) 
```



### information_timeliness()

����һ����������������ϢʱЧ�Ե���ʾ��

**���أ�**
- `str`������һ����ʾ�ı�������ģ��������Ϣ�ڵ�ǰ�������е�ʱЧ�Ի�����ԡ�

**ʾ����**
```python
from kylinLLM.memory import Prompt
timeliness_prompt = Prompt.information_timeliness()
print(timeliness_prompt)
```

### user_impression()

����һ�����ڽ�����ʷ�����û�ӡ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�͸��ݹ�ȥ�Ľ��������û��Ĺ۵��̬�ȡ�

**ʾ����**
```python
from kylinLLM.memory import Prompt
impression_prompt = Prompt.user_impression()
print(impression_prompt)
```

### problem_decomposition()

����һ������������ֽ�Ϊ��С���������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ͽ���������ֽ�Ϊ���׹���Ĳ��֡�

**ʾ����**
```python
from kylinLLM.memory import Prompt
decomposition_prompt = Prompt.problem_decomposition()
print(decomposition_prompt)
```

### proactive_problem_solving()

����һ������ʶ��Ǳ�����Ⲣ��������������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��Ԥ�����Ⲣ���Ԥ���Խ��������

**ʾ����**
```python
from kylinLLM.memory import Prompt
proactive_prompt = Prompt.proactive_problem_solving()
print(proactive_prompt)
```

### divergent_questioning()

����һ�������������ͷ�����ʡ���������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�;͸���������������м��ص����⡣

**ʾ����**
```python
from kylinLLM.memory import Prompt
questioning_prompt = Prompt.divergent_questioning()
print(questioning_prompt)
```

### problem_classification()

����һ��������������ൽ�ʵ����ͻ��������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ͽ�������ൽ���ʵ���������

**ʾ����**
```python
from kylinLLM.memory import Prompt
classification_prompt = Prompt.problem_classification()
print(classification_prompt)
```

### introspection_summary()

����һ�����ڶԻ���ʡ���ܽ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��ʶ����ܽύ���е���Ҫϸ�ڡ�

**ʾ����**
```python
from kylinLLM.memory import Prompt
introspection_prompt = Prompt.introspection_summary()
print(introspection_prompt)
```

### traffic_diversion()

����һ�����ڶԴ���������з���͵������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ͽ�����������ಢ�����ʵ��Ĵ����������š�

**ʾ����**
```python
from kylinLLM.classification import Prompt
diversion_prompt = Prompt.traffic_diversion()
print(diversion_prompt)
```

### attention_level()

����һ������������Ϣ������Ӧ�ܵ��Ĺ�ע�Ȼ����ȼ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��������Ϣ���������Ҫ�Ժͽ����̶ȡ�

**ʾ����**
```python
from kylinLLM.classification import Prompt
attention_prompt = Prompt.attention_level()
print(attention_prompt)
```

### dialogue_completion()

����һ������Ԥ��Ի���Ự����ܵ���������ɵ���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��Ԥ��Ի�����һ����չ�������

**ʾ����**
```python
from kylinLLM.classification import Prompt
completion_prompt = Prompt.dialogue_completion()
print(completion_prompt)
```

### sentence_structure()

����һ�����ڷ����ͷ���������ӵ��﷨�ṹ�����͵���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ͷ������ӵ��﷨�ṹ�����з��ࡣ

**ʾ����**
```python
from kylinLLM.classification import Prompt
structure_prompt = Prompt.sentence_structure()
print(structure_prompt)
```

### memory_tagging()

����һ������Ϊ��Ϣ�����ʵ���ǩ����ʾ���Ա���δ�������ͷ��ࡣ

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��Ϊ������Ϣ���ɺ��ʵı�ǩ����ࡣ

**ʾ����**
```python
from kylinLLM.classification import Prompt
tagging_prompt = Prompt.memory_tagging()
print(tagging_prompt)
```


### qa_matching()

����һ�����ڽ�����������֪ʶ��������ʵĴ�ƥ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ʹӿ���֪ʶ�����ҵ����ʺϸ�������Ĵ𰸡�

**ʾ����**
```python
from kylinLLM.strategy import Prompt
matching_prompt = Prompt.qa_matching()
print(matching_prompt)
```

### search_public_knowledge()

����һ�����������ͼ�������֪ʶ���������Ϣ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ʹӹ���֪ʶ������������ȡ�뵱ǰ��ѯ��ص���Ϣ��

**ʾ����**
```python
from kylinLLM.strategy import Prompt
search_prompt = Prompt.search_public_knowledge()
print(search_prompt)
```

### strategy_matching()

����һ������ʶ���ѡ�����ʺϸ������������Ĳ��Ե���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��Ϊ�������ѡ������ʵĲ��ԡ�

**ʾ����**
```python
from kylinLLM.strategy import Prompt
strategy_match_prompt = Prompt.strategy_matching()
print(strategy_match_prompt)
```

### strategy_objective()

����һ������Ϊѡ�����Զ�����ȷ�Ϳ�ʵ��Ŀ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��Ϊѡ���Ĳ����ƶ��������ɴ�ɵ�Ŀ�ꡣ

**ʾ����**
```python
from kylinLLM.strategy import Prompt
objective_prompt = Prompt.strategy_objective()
print(objective_prompt)
```

### strategy_completion()

����һ�������ƶ������ƻ�����ɺ�ʵʩ��ѡ���Ե���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�Ϳ���һ��ȫ��ļƻ���ʵʩѡ���Ĳ��ԡ�

**ʾ����**
```python
from kylinLLM.strategy import Prompt
completion_prompt = Prompt.strategy_completion()
print(completion_prompt)
```

### strategy_impact()

����һ�����ڷ�����Ԥ��ʵʩ��ѡ���Ե�Ǳ��Ӱ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ͷ���ʵʩѡ�����Կ��ܴ�����Ӱ�졣

**ʾ����**
```python
from kylinLLM.strategy import Prompt
impact_prompt = Prompt.strategy_impact()
print(impact_prompt)
```

### emotional_impact()

����һ�������������Ի��Ӧ���û������ڿ��ܲ��������Ӱ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���������Ի��Ӧ���ܴ��������Ӱ�졣

**ʾ����**
```python
from kylinLLM.strategy import Prompt
emotional_prompt = Prompt.emotional_impact()
print(emotional_prompt)
```

### knowledge_extraction()

����һ�����ڴӸ�����Ϣ������������ȡ�ؼ�֪ʶ���������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ʹӸ�����������ȡ��Ҫ��֪ʶ��򶴼���

**ʾ����**
```python
from kylinLLM.strategy import Prompt
extraction_prompt = Prompt.knowledge_extraction()
print(extraction_prompt)
```

### entity_extraction()

����һ�����ڴӸ����ı���ʶ�����ȡ��Ҫʵ�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ʹ��ı���ʶ����ȡ��Ҫʵ�壨�����ơ��ص㡢��֯�ȣ���

**ʾ����**
```python
from kylinLLM.strategy import Prompt
entity_prompt = Prompt.entity_extraction()
print(entity_prompt)
```

### noise_identification()

����һ�����ڼ���ʶ���������ݻ����������κ��������޹���Ϣ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��ʶ�������е������������Ϣ��

**ʾ����**
```python
from kylinLLM.strategy import Prompt
noise_prompt = Prompt.noise_identification()
print(noise_prompt)
```

### plugin_selection()

����һ������ѡ������ʵĲ���򹤾���Э��ִ�е�ǰ�������Ե���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ��ѡ�����ʺ�ִ�е�ǰ����Ĳ���򹤾ߡ�

**ʾ����**
```python
from kylinLLM.strategy import Prompt
plugin_prompt = Prompt.plugin_selection()
print(plugin_prompt)
```
### education()

����һ�����ڰ��ݽ����߽�ɫ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ṩ������������ʤ�Ľ����Դٽ�ѧϰ��

**ʾ����**
```python
from kylinLLM.role import Prompt
education_prompt = Prompt.education()
print(education_prompt)
```

### companionship()

����һ�����ڰ���֧���Ի���ɫ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ����Ϊһ������֧�ֵĻ�飬�ṩͬ���ĺ��ѺõĽ�̸��

**ʾ����**
```python
from kylinLLM.role import Prompt
companionship_prompt = Prompt.companionship()
print(companionship_prompt)
```

### medical()

����һ�������ṩҽ����Ϣ�ͽ������ʾ��ͬʱ��������������

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ṩҽ����Ϣ�ͽ��飬��������רҵҽ����ʿ����ݡ�

**ʾ����**
```python
from kylinLLM.role import Prompt
medical_prompt = Prompt.medical()
print(medical_prompt)
```

### super_ai()

����һ������չʾ�߼��������ͷ�����������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ڹ㷺�����ⷶΧ��չʾ�Ƚ����������ͷ���������

**ʾ����**
```python
from kylinLLM.role import Prompt
super_ai_prompt = Prompt.super_ai()
print(super_ai_prompt)
```

### mystical()

����һ�������ṩ���غ;���ͳ�������ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ�ʹӸ������غ;���ͳ���ṩ����͹۵㣬ͬʱ�������غͿ��ŵ�̬�ȡ�

**ʾ����**
```python
from kylinLLM.role import Prompt
mystical_prompt = Prompt.mystical()
print(mystical_prompt)
```

### psychological_counseling()

����һ�������ṩ����֧�ֺ�һ�㽨�����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ṩ֧����������һ�㽨�飬ͬʱǿ������������ҪѰ��רҵ��������Ҫ�ԡ�

**ʾ����**
```python
from kylinLLM.role import Prompt
counseling_prompt = Prompt.psychological_counseling()
print(counseling_prompt)
```

### beauty()

����һ�������ṩ���ݺͻ�ױ���ɵ���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ṩ���ݺͻ�ױ���飬���Ǹ���Ƥ�����͡���ɫ�͸��˷��

**ʾ����**
```python
from kylinLLM.role import Prompt
beauty_prompt = Prompt.beauty()
print(beauty_prompt)
```

### fitness_coach()

����һ�������ṩ������Ͷ���֧�ֵ���ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���ṩ����֧�ֺ�һ�㽡���飬ͬʱǿ���ڿ�ʼ�κ��µĶ����ƻ�ǰ��ѯҽ������Ҫ�ԡ�

**ʾ����**
```python
from kylinLLM.role import Prompt
fitness_prompt = Prompt.fitness_coach()
print(fitness_prompt)
```

### streamer()

����һ�����ڰ���ֱ��������ɫ����ʾ��

**���أ�**
- `str`������һ����ʾ�ı���ָ��ģ���Ը��������Ժͻ����Ե������������ڣ����ֻ�Ծ��ƽ�׽��˵�����

**ʾ����**
```python
from kylinLLM.role import Prompt
streamer_prompt = Prompt.streamer()
print(streamer_prompt)
```

