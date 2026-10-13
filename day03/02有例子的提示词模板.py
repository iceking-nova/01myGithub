# 补充导入 FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

# 1. 准备示例数据
examples = [
    {"input": "高兴", "output": "愉悦"},
    {"input": "快速", "output": "迅猛"},
    {"input": "美丽", "output": "绚丽"}
]

# 2. 构建提示词模板 (用于格式化每一个单独的示例)
example_prompt = PromptTemplate.from_template(
    "输入: {input}\n输出: {output}"
)

# 3. 创建 FewShotPromptTemplate (少样本提示词模板)
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据以下示例，将输入词语转换为同义词",
    suffix="基于示例回答问题。用户输入: {word}\n输出: ", # 这里的 {word} 是留给用户实际输入的占位符
    input_variables=["word"] # 声明需要用户输入的变量名
)

# 准备调用大语言模型的客户端
llm = Tongyi(model="qwen-max")

chain = few_shot_prompt | llm

result = chain.invoke({"word": "勇敢"})

print(result)