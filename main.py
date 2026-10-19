"""Um agente de IA que chama as SUAS funcoes Python.

O modelo nao executa nada: ele devolve "quero chamar `clima` com cidade=X".
Quem roda a funcao e devolve o resultado e voce. Esse vai e volta e o que o
mercado chama de "tool calling" ou "function calling".

    pip install openai
    export OPENAI_API_KEY=...        # ou OPENROUTER_API_KEY + base_url
    python main.py
"""
import json

from openai import OpenAI

client = OpenAI()
MODELO = "gpt-4.1-mini"


# ---- 1. suas funcoes, Python normal ----------------------------------------

def clima(cidade: str) -> dict:
    """Aqui entraria uma chamada real a uma API de clima."""
    tabela = {"sao paulo": 19, "recife": 29, "curitiba": 14}
    return {"cidade": cidade, "graus": tabela.get(cidade.lower(), 25)}


def converter(valor: float, de: str, para: str) -> dict:
    taxas = {("BRL", "USD"): 0.18, ("USD", "BRL"): 5.55}
    return {"resultado": round(valor * taxas[(de, para)], 2), "moeda": para}


FUNCOES = {"clima": clima, "converter": converter}

# ---- 2. o "cardapio" que o modelo le ---------------------------------------

FERRAMENTAS = [
    {"type": "function", "function": {
        "name": "clima",
        "description": "Temperatura atual de uma cidade",
        "parameters": {"type": "object", "properties": {
            "cidade": {"type": "string"}}, "required": ["cidade"]}}},
    {"type": "function", "function": {
        "name": "converter",
        "description": "Converte um valor entre moedas (BRL, USD)",
        "parameters": {"type": "object", "properties": {
            "valor": {"type": "number"},
            "de": {"type": "string"}, "para": {"type": "string"}},
            "required": ["valor", "de", "para"]}}},
]


# ---- 3. o laco do agente ---------------------------------------------------

def agente(pergunta):
    mensagens = [{"role": "user", "content": pergunta}]
    while True:
        resposta = client.chat.completions.create(
            model=MODELO, messages=mensagens, tools=FERRAMENTAS)
        msg = resposta.choices[0].message
        mensagens.append(msg)

        if not msg.tool_calls:          # sem chamada = resposta final
            return msg.content

        for chamada in msg.tool_calls:  # pode pedir varias de uma vez
            nome = chamada.function.name
            args = json.loads(chamada.function.arguments)
            print(f"  -> {nome}({args})")
            resultado = FUNCOES[nome](**args)
            mensagens.append({"role": "tool",
                              "tool_call_id": chamada.id,
                              "content": json.dumps(resultado)})


if __name__ == "__main__":
    print(agente("Quantos graus faz em Recife? E quanto é 100 reais em dólar?"))
