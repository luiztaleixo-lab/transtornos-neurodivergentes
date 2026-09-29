# chatbot.py - Logica de Respostas do NeuroGuia Interativo

CHATBOT_TOPICS = {
    "neuro": {
        "title": "Neurodivergencia",
        "response": "A neurodivergencia reconhece que algumas pessoas possuem formas diferentes de funcionamento neurologico e cognitivo. O objetivo e combater preconceitos e promover inclusao, respeito e acessibilidade para todos."
    },
    "diagnostico": {
        "title": "Diagnostico",
        "response": "O diagnostico de uma neurodivergencia e clinico e realizado por profissionais especializados, como psicologos, psiquiatras, neurologistas e neuropediatras. Nao existem exames laboratoriais ou de imagem capazes de confirmar sozinho uma neurodivergencia."
    },
    "autodiagnostico": {
        "title": "Autodiagnostico",
        "response": "O autodiagnostico ocorre quando uma pessoa acredita possuir uma condicao apenas com base em informacoes da internet. Embora os conteudos online possam ajudar na conscientizacao, apenas profissionais qualificados podem realizar um diagnostico confiavel."
    },
    "superdotacao": {
        "title": "Altas Habilidades / Superdotacao",
        "response": "As Altas Habilidades/Superdotacao estao relacionadas a capacidades intelectuais, criativas, academicas ou artisticas acima da media. Cada pessoa pode apresentar talentos em areas diferentes."
    },
    "bipolar": {
        "title": "Transtorno Bipolar",
        "response": "O transtorno bipolar provoca alteracoes significativas de humor, variando entre periodos de depressao e episodios de mania ou hipomania. O tratamento normalmente envolve acompanhamento medico, psicoterapia e medicamentos."
    },
    "intelectual": {
        "title": "Deficiencia Intelectual",
        "response": "A deficiencia intelectual e um transtorno do neurodesenvolvimento que pode afetar habilidades cognitivas, sociais, academicas e praticas, exigindo apoio adequado para promover autonomia e inclusao."
    },
    "tea": {
        "title": "TEA (Autismo)",
        "response": "O Transtorno do Espectro Autista (TEA) afeta principalmente a comunicacao, a interacao social e alguns padroes de comportamento. Cada pessoa autista possui caracteristicas e necessidades proprias."
    },
    "tdah": {
        "title": "TDAH",
        "response": "O Transtorno do Deficit de Atencao e Hiperatividade (TDAH) e caracterizado por sintomas de desatencao, impulsividade e hiperatividade. O acompanhamento profissional pode auxiliar no desenvolvimento de estrategias para o dia a dia."
    },
    "borderline": {
        "title": "Borderline",
        "response": "A sindrome de borderline e caracterizada por instabilidade emocional, medo intenso de abandono, impulsividade e dificuldades nos relacionamentos interpessoais."
    },
    "discalculia": {
        "title": "Discalculia",
        "response": "A discalculia e um transtorno especifico de aprendizagem que afeta a compreensao de numeros, calculos matematicos e raciocinio logico relacionado a matematica."
    },
    "dislexia": {
        "title": "Dislexia",
        "response": "A dislexia e um transtorno especifico da aprendizagem que afeta principalmente a leitura, a escrita e a interpretacao textual. O acompanhamento especializado auxilia no desenvolvimento das habilidades academicas."
    },
    "tod": {
        "title": "TOD",
        "response": "O Transtorno Opositor Desafiador (TOD) e caracterizado por comportamentos desafiadores, irritabilidade frequente e dificuldade em aceitar regras e figuras de autoridade."
    },
    "tourette": {
        "title": "Sindrome de Tourette",
        "response": "A Sindrome de Tourette e uma condicao neurologica caracterizada por tiques motores e vocais involuntarios. O acompanhamento medico ajuda a controlar os sintomas e melhorar a qualidade de vida."
    }
}

KEYWORD_MAP = {
    "neuro": ["neuro", "neurodivergencia", "neurotipico", "atipico", "espectro"],
    "diagnostico": ["diagnostico", "como diagnosticar", "laudo", "exame", "avaliacao", "medico"],
    "autodiagnostico": ["autodiagnostico", "internet", "teste online", "desconfio"],
    "superdotacao": ["superdotacao", "altas habilidades", "ah/sd", "ah", "sd", "inteligencia alta", "qi"],
    "bipolar": ["bipolar", "bipolaridade", "mania", "hipomania", "humor oscilante", "tb"],
    "intelectual": ["intelectual", "deficiencia intelectual", "cognitiva", "di"],
    "tea": ["tea", "autismo", "autista", "asperger", "sensorial", "stimming"],
    "tdah": ["tdah", "deficit de atencao", "hiperatividade", "desatencao", "foco"],
    "borderline": ["borderline", "tpb", "limite", "instabilidade emocional", "abandono"],
    "discalculia": ["discalculia", "calculo", "matematica", "numeros", "contas"],
    "dislexia": ["dislexia", "leitura", "escrita", "fonemas", "letras"],
    "tod": ["tod", "opositor", "desafiador", "regras", "autoridade", "raiva"],
    "tourette": ["tourette", "tiques", "tique", "tique motor", "tique vocal"]
}

def get_response(topic_or_query: str) -> dict:
    cleaned = topic_or_query.strip().lower()
    
    if cleaned in CHATBOT_TOPICS:
        item = CHATBOT_TOPICS[cleaned]
        return {
            "topic": cleaned,
            "title": item["title"],
            "response": item["response"]
        }
    
    import unicodedata
    def normalize(text):
        return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn").lower()
    
    normalized_query = normalize(cleaned)
    for topic_key, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in normalized_query:
                item = CHATBOT_TOPICS[topic_key]
                return {
                    "topic": topic_key,
                    "title": item["title"],
                    "response": item["response"]
                }
                
    return {
        "topic": "geral",
        "title": "Orientacao Geral",
        "response": "Selecione um dos temas dos botoes acima ou consulte a secao de condicoes no menu superior para acessar as informacoes detalhadas sobre cada diagnostico."
    }
