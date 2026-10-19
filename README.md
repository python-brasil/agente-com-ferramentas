# Agente com ferramentas (tool calling)

Um agente de IA que chama as suas funções Python. O modelo decide **qual**
função chamar e **com quais argumentos**; quem executa é o seu código, e o
resultado volta para o modelo até ele ter o que precisa para responder.

```
pip install openai
export OPENAI_API_KEY=...
python main.py
```

Funciona com qualquer provedor compatível com a API da OpenAI. Para usar o
OpenRouter, por exemplo:

```python
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
```

Três partes:

1. **Suas funções**, Python comum (`clima`, `converter`).
2. **O cardápio** em JSON Schema que o modelo lê para saber o que existe.
3. **O laço**: enquanto o modelo pedir uma ferramenta, execute e devolva.
   Quando vier texto sem `tool_calls`, é a resposta final.

Publicado pelo [@python_brasil](https://instagram.com/python_brasil).
