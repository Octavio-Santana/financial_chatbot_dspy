import dspy

TRAINSET = [

    # 📅 Totais
    dspy.Example(
        question="Quanto gastei em novembro de 2025?",
        current_date="27/03/2026",
        answer="Em novembro de 2025 você gastou R$ 2.440,00."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Qual foi meu gasto total em dezembro?",
        current_date="27/03/2026",
        answer="Em dezembro de 2025 você gastou R$ 3.200,00."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Total gasto em janeiro de 2026?",
        current_date="27/03/2026",
        answer="Em janeiro de 2026 você gastou R$ 2.865,90."
    ).with_inputs("question", "current_date"),

    # 📊 Comparações
    dspy.Example(
        question="Gastei mais em dezembro ou janeiro?",
        current_date="27/03/2026",
        answer="Você gastou mais em dezembro (R$ 3.200,00) do que em janeiro (R$ 2.865,90)."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Março está mais caro que fevereiro?",
        current_date="27/03/2026",
        answer="Sim, março está mais caro. Você gastou R$ 3.640,00 contra R$ 3.300,00 em fevereiro."
    ).with_inputs("question", "current_date"),

    # 📈 Tendência
    dspy.Example(
        question="Meus gastos aumentaram de novembro para dezembro?",
        current_date="27/03/2026",
        answer="Sim, seus gastos aumentaram de R$ 2.440,00 em novembro para R$ 3.200,00 em dezembro."
    ).with_inputs("question", "current_date"),

    # 🧾 Categoria dominante
    dspy.Example(
        question="Qual foi a categoria mais cara em fevereiro de 2026?",
        current_date="27/03/2026",
        answer="Em fevereiro a categoria mais cara foi moradia, com R$ 1.500,00."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Onde eu mais gastei dinheiro em dezembro?",
        current_date="27/03/2026",
        answer="Em dezembro você mais gastou em compras, com R$ 920,00."
    ).with_inputs("question", "current_date"),

    # 🍔 Categoria específica
    dspy.Example(
        question="Quanto gastei com alimentação em março?",
        current_date="27/03/2026",
        answer="Em março você gastou R$ 260,00 com alimentação."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Quanto foi gasto com transporte em novembro?",
        current_date="27/03/2026",
        answer="Em novembro você gastou R$ 170,00 com transporte."
    ).with_inputs("question", "current_date"),

    # 💰 Saldo
    dspy.Example(
        question="Quanto sobrou em dezembro?",
        current_date="27/03/2026",
        answer="Em dezembro você recebeu R$ 4.300,00 e gastou R$ 3.200,00, sobrando R$ 1.100,00."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Qual foi meu saldo em janeiro?",
        current_date="27/03/2026",
        answer="Em janeiro você recebeu R$ 4.500,00 e gastou R$ 2.865,90, sobrando R$ 1.634,10."
    ).with_inputs("question", "current_date"),

    # 🧠 Inferência
    dspy.Example(
        question="Qual mês foi o mais caro até agora?",
        current_date="27/03/2026",
        answer="O mês mais caro foi março de 2026, com R$ 3.640,00 em gastos."
    ).with_inputs("question", "current_date"),

    dspy.Example(
        question="Meu aluguel mudou ao longo dos meses?",
        current_date="27/03/2026",
        answer="Não, o valor do aluguel permaneceu constante entre R$ 1.400,00 e R$ 1.500,00 ao longo dos meses."
    ).with_inputs("question", "current_date"),
]

DEVSET = [

    # 🧠 Generalização
    dspy.Example(
        question="Qual mês eu tive o maior gasto?",
        current_date="27/03/2026",
        answer="O mês com maior gasto foi março de 2026, com R$ 3.640,00."
    ).with_inputs("question", "current_date"),

    # 📊 Comparação indireta
    dspy.Example(
        question="Fevereiro foi mais caro que janeiro?",
        current_date="27/03/2026",
        answer="Sim, fevereiro foi mais caro. Você gastou R$ 3.300,00 contra R$ 2.865,90 em janeiro."
    ).with_inputs("question", "current_date"),

    # 🧾 Categoria menos óbvia
    dspy.Example(
        question="Quanto gastei com educação em março?",
        current_date="27/03/2026",
        answer="Em março você gastou R$ 300,00 com educação."
    ).with_inputs("question", "current_date"),

    # 💰 Raciocínio composto
    dspy.Example(
        question="Em qual mês eu economizei mais dinheiro?",
        current_date="27/03/2026",
        answer="Você economizou mais em janeiro de 2026, com R$ 1.634,10 restantes."
    ).with_inputs("question", "current_date"),

    # 📉 Tendência
    dspy.Example(
        question="Existe uma tendência de aumento nos meus gastos?",
        current_date="27/03/2026",
        answer="Sim, há uma tendência geral de aumento, com picos em dezembro e março."
    ).with_inputs("question", "current_date"),

]