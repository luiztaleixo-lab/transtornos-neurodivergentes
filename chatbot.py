# chatbot.py - Logica de Respostas do NeuroGuia Interativo
import unicodedata

CHATBOT_TOPICS = {
    "neuro": {
        "title": "Neurodivergencia",
        "response": "A neurodivergencia reconhece que algumas pessoas possuem formas diferentes de funcionamento neurologico e cognitivo. O objetivo e combater preconceitos e promover inclusao, respeito e acessibilidade para todos."
    },
    "diagnostico": {
        "title": "Diagnostico",
        "response": "O diagnostico de uma neurodivergencia e clinico e realizado por profissionais especializados, como psicologos, psiquiatras, neurologistas e neuropediatras. Nao existem exames laboratoriais ou de imagem capazes de confirmar sozinho uma neurodivergencia. O NeuroGuia e uma plataforma educativa e de interacao: as informacoes disponibilizadas nao substituem avaliacao, diagnostico ou acompanhamento profissional."
    },
    "autodiagnostico": {
        "title": "Autodiagnostico",
        "response": "O autodiagnostico ocorre quando uma pessoa acredita possuir uma condicao apenas com base em informacoes da internet. Embora os conteudos online possam ajudar na conscientizacao, apenas profissionais qualificados podem realizar um diagnostico confiavel. O chatbot fornece informacoes educativas e orientacoes gerais, mas nao realiza diagnostico. Tambem e importante verificar a origem das informacoes e dar preferencia a instituicoes de saude, universidades, orgaos publicos e fontes cientificas confiaveis."
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

# ---------------------------------------------------------------------------
# Perguntas frequentes e orientacoes do dia a dia
# Formato: chave -> title (a propria pergunta), response, keywords
# ---------------------------------------------------------------------------
FAQ_TOPICS = {
    "faq_relaxar": {
        "title": "O que posso fazer quando estou com dificuldade para relaxar?",
        "response": "Procure diminuir os estímulos ao redor e reserve alguns minutos para uma atividade tranquila. Música calma, leitura, respiração lenta ou um ambiente confortável podem ajudar, dependendo do que funciona melhor para você.",
        "keywords": ["relaxar", "relaxamento", "acalmar", "ansioso", "ansiedade"]
    },
    "faq_compromisso": {
        "title": "Como posso me preparar para um compromisso ou situação diferente da rotina?",
        "response": "Verifique com antecedência onde será, quanto tempo deve durar e o que pode acontecer. Organizar essas informações pode tornar a situação mais previsível.",
        "keywords": ["compromisso", "fora da rotina", "situacao diferente", "me preparar", "evento novo"]
    },
    "faq_atividade_dificil": {
        "title": "O que fazer quando uma atividade parece muito difícil?",
        "response": "Divida a atividade em pequenas etapas e comece pela parte mais simples. Fazer uma etapa de cada vez pode tornar a tarefa mais fácil de organizar.",
        "keywords": ["atividade dificil", "tarefa dificil", "muito dificil", "nao consigo fazer"]
    },
    "faq_lembrar": {
        "title": "Como posso lembrar de compromissos e tarefas?",
        "response": "Utilize alarmes, calendários, aplicativos, listas ou lembretes visuais. Escolha o recurso que seja mais fácil de consultar durante sua rotina.",
        "keywords": ["lembrar", "esquecer", "esquecimento", "lembrete", "alarme", "agenda"]
    },
    "faq_dormir": {
        "title": "O que posso fazer quando tenho dificuldade para dormir?",
        "response": "Procure manter horários de sono regulares e criar uma rotina tranquila antes de dormir. Se a dificuldade persistir ou estiver prejudicando sua rotina, converse com um profissional de saúde.",
        "keywords": ["dormir", "sono", "insonia", "acordar a noite"]
    },
    "faq_barulho": {
        "title": "Como lidar com um ambiente muito barulhento?",
        "response": "Se possível, procure um local mais silencioso ou faça uma pausa do ambiente. Algumas pessoas também podem se sentir mais confortáveis utilizando recursos que diminuam os estímulos sonoros.",
        "keywords": ["barulho", "barulhento", "ruido", "som alto", "sobrecarga sonora"]
    },
    "faq_muitas_tarefas": {
        "title": "O que fazer quando muitas tarefas precisam ser realizadas ao mesmo tempo?",
        "response": "Anote todas as tarefas e organize-as por prioridade. Depois, concentre-se em uma tarefa por vez.",
        "keywords": ["muitas tarefas", "tarefas ao mesmo tempo", "sobrecarregado", "prioridade"]
    },
    "faq_limites": {
        "title": "Como posso estabelecer limites com outras pessoas?",
        "response": "Comunique de maneira clara o que você aceita ou não e explique suas necessidades quando se sentir confortável. Estabelecer limites pode ajudar a tornar as relações mais respeitosas.",
        "keywords": ["estabelecer limites", "impor limites", "colocar limites", "dizer nao"]
    },
    "faq_situacao_social": {
        "title": "O que fazer quando não consigo entender uma situação social?",
        "response": "Se possível, peça uma explicação ou esclarecimento. Também pode ser útil conversar posteriormente com alguém de confiança sobre o que aconteceu.",
        "keywords": ["situacao social", "entender pessoas", "interacao social", "nao entendi o que aconteceu"]
    },
    "faq_pedir_ajuda": {
        "title": "Como posso pedir ajuda?",
        "response": "Explique de forma objetiva o que está acontecendo e qual tipo de ajuda seria útil. Pedir ajuda quando necessário faz parte do cuidado consigo mesmo.",
        "keywords": ["pedir ajuda", "preciso de ajuda", "como peco ajuda"]
    },
    "faq_frustracao": {
        "title": "O que fazer quando estou frustrado(a) com uma tarefa?",
        "response": "Faça uma pausa e tente retomar a atividade depois. Também pode ser útil dividir a tarefa em partes menores ou pedir orientação.",
        "keywords": ["frustrado", "frustrada", "frustracao", "irritado com tarefa"]
    },
    "faq_mudanca_planos": {
        "title": "Como lidar com uma mudança de planos de última hora?",
        "response": "Primeiro, procure entender o que mudou. Depois, reorganize o que for necessário e dê a si mesmo um tempo para se adaptar à nova situação.",
        "keywords": ["mudanca de planos", "mudanca de ultima hora", "plano mudou", "imprevisto", "mudanca de rotina"]
    },
    "faq_ambiente_confortavel": {
        "title": "Como posso tornar meu ambiente mais confortável?",
        "response": "Observe quais elementos do ambiente causam desconforto e, quando possível, faça pequenas mudanças na iluminação, nos sons, na organização ou em outros estímulos.",
        "keywords": ["ambiente confortavel", "deixar o ambiente", "iluminacao", "luz forte"]
    },
    "faq_expressar_sentimentos": {
        "title": "O que posso fazer quando estou com dificuldade para expressar o que sinto?",
        "response": "Você pode escrever o que está sentindo, utilizar mensagens ou conversar com alguém de confiança. Não é necessário encontrar as palavras imediatamente.",
        "keywords": ["expressar o que sinto", "expressar sentimentos", "falar o que sinto", "dificuldade para expressar"]
    },
    "faq_estudos": {
        "title": "Como posso melhorar minha organização nos estudos?",
        "response": "Organize as atividades por prioridade, estabeleça horários e divida conteúdos maiores em partes menores. Pausas durante os estudos também podem ajudar na organização da rotina.",
        "keywords": ["estudos", "estudar", "organizacao nos estudos", "concentrar para estudar"]
    },
    "faq_acompanhar_conversa": {
        "title": "O que fazer quando estou tendo dificuldade para acompanhar uma conversa?",
        "response": "Você pode pedir para a pessoa repetir ou explicar novamente. Também pode escolher um ambiente com menos distrações, quando possível.",
        "keywords": ["acompanhar uma conversa", "acompanhar conversa", "me perco na conversa", "perdi o fio da conversa"]
    },
    "faq_falar_publico": {
        "title": "Como lidar com situações em que preciso falar em público?",
        "response": "Prepare previamente o que deseja falar e pratique antes da situação. Ter um roteiro ou algumas palavras-chave pode ajudar a organizar as ideias.",
        "keywords": ["falar em publico", "apresentacao", "apresentar trabalho", "seminario"]
    },
    "faq_desconforto_lugar": {
        "title": "O que fazer quando estou me sentindo desconfortável em um lugar?",
        "response": "Se for possível e seguro, afaste-se da situação por alguns minutos e procure um ambiente mais confortável. Depois, avalie se consegue retornar ou se precisa de ajuda.",
        "keywords": ["desconfortavel em um lugar", "desconfortavel", "quero sair do lugar", "mal em um lugar"]
    },
    "faq_registrar_desconforto": {
        "title": "Como posso registrar situações que me causam desconforto?",
        "response": "Você pode utilizar um bloco de notas ou aplicativo para registrar a situação, o que aconteceu antes, quais estímulos estavam presentes e como você se sentiu.",
        "keywords": ["registrar situacoes", "registrar desconforto", "diario", "anotar o que aconteceu"]
    },
    "faq_compartilhar_experiencia": {
        "title": "Posso compartilhar minha experiência com outras pessoas?",
        "response": "Sim. O compartilhamento de experiências pode favorecer a troca entre pessoas, mas experiências individuais não devem ser consideradas como substitutas de informações ou orientações profissionais.",
        "keywords": ["compartilhar minha experiencia", "compartilhar experiencia", "contar minha historia", "trocar experiencias"]
    },
    "faq_informacao_preocupa": {
        "title": "O que devo fazer se uma informação do chatbot me preocupar?",
        "response": "Evite tirar conclusões sozinho(a). Procure uma fonte confiável e, se necessário, converse com um profissional de saúde sobre a situação.",
        "keywords": ["informacao me preocupou", "informacao me preocupar", "fiquei preocupado", "fiquei com medo", "me assustou"]
    },
    "faq_ajudar_alguem": {
        "title": "Como posso ajudar alguém que está passando por uma situação difícil?",
        "response": "Escute sem julgamentos, respeite os limites da pessoa e pergunte de que maneira você pode ajudar. Quando necessário, incentive a busca por apoio profissional.",
        "keywords": ["ajudar alguem", "ajudar um amigo", "ajudar uma pessoa", "situacao dificil"]
    },
}

CHATBOT_TOPICS.update({k: {"title": v["title"], "response": v["response"]} for k, v in FAQ_TOPICS.items()})

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

# Perguntas que ja eram cobertas por topicos existentes (evita respostas repetidas).
# Pergunta (normalizada) -> chave do topico existente.
QUESTION_ALIASES = {
    "o chatbot pode dizer se eu tenho algum transtorno?": "autodiagnostico",
    "posso confiar em qualquer informacao que encontro na internet?": "autodiagnostico",
    "posso usar o neuroguia para substituir um profissional?": "diagnostico",
}

# Palavras-chave das FAQs que apontam para topicos existentes.
FAQ_EXTRA_KEYWORDS = {
    "autodiagnostico": [
        "chatbot pode dizer", "tenho algum transtorno", "voce diagnostica",
        "confiar na internet", "confiar em qualquer informacao", "informacao da internet"
    ],
    "diagnostico": [
        "substituir um profissional", "substituir o profissional",
        "substitui o medico", "no lugar do profissional"
    ],
}


def _normalize(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    ).lower().strip()


def _build(topic_key: str) -> dict:
    item = CHATBOT_TOPICS[topic_key]
    return {
        "topic": topic_key,
        "title": item["title"],
        "response": item["response"]
    }


def get_response(topic_or_query: str) -> dict:
    cleaned = topic_or_query.strip().lower()

    # 1) Chave exata de topico (botoes do site)
    if cleaned in CHATBOT_TOPICS:
        return _build(cleaned)

    normalized_query = _normalize(cleaned)

    # 2) Pergunta exata (FAQ ou alias de pergunta ja coberta)
    if normalized_query in QUESTION_ALIASES:
        return _build(QUESTION_ALIASES[normalized_query])
    for key, item in FAQ_TOPICS.items():
        if normalized_query == _normalize(item["title"]):
            return _build(key)

    # 3) Palavras-chave das FAQs (frases mais especificas, por isso vem antes)
    for key, item in FAQ_TOPICS.items():
        for kw in item["keywords"]:
            if _normalize(kw) in normalized_query:
                return _build(key)
    for topic_key, keywords in FAQ_EXTRA_KEYWORDS.items():
        for kw in keywords:
            if kw in normalized_query:
                return _build(topic_key)

    # 4) Palavras-chave dos topicos originais
    for topic_key, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in normalized_query:
                return _build(topic_key)

    return {
        "topic": "geral",
        "title": "Orientacao Geral",
        "response": "Selecione um dos temas dos botoes acima ou consulte a secao de condicoes no menu superior para acessar as informacoes detalhadas sobre cada diagnostico."
    }