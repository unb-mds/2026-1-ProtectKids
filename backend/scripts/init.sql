-- tabela pai
CREATE TABLE IF NOT EXISTS parlamentares (
    id_parlamentar INT PRIMARY KEY, -- ID único < API da camara fornece
    nome VARCHAR(100) NOT NULL, --NOT NULL proíbe que uma lei sejá salva sem essa categoria
    partido VARCHAR(20) NOT NULL, --VARCHAR aloca espaço de tamanho(X)
    uf CHAR(2) NOT NULL --sigla do estado, DF, SP etc
);

-- tabela filha
CREATE TABLE IF NOT EXISTS proposicoes (
    id_proposicao INT PRIMARY KEY,
    id_externo INT NOT NULL UNIQUE,
    id_autor INT NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    numero INT NOT NULL,
    ano INT NOT NULL,
    ementa TEXT NOT NULL, --TEXT porque não sabemos o tamanho do texto
    tema VARCHAR(50),
    data_apresentacao DATE,
    
    -- configuração da chave estrangeira
    CONSTRAINT fk_autor 
        FOREIGN KEY (id_autor) 
        REFERENCES parlamentares(id_parlamentar)
        ON DELETE CASCADE
);
--  inserindo os Autores primeiro (para respeitar a Foreign Key)
INSERT INTO parlamentares (id_parlamentar, nome, partido, uf) VALUES --valores ficticios para teste
(1, 'Augusto Garcia', 'PL', 'SP'),
(2, 'Ryan Lira', 'PT', 'MG');
ON CONFLICT DO NOTHING

--  inserindo as Proposições (Focadas no escopo  do projeto: Cyberbullying/Proteção Digital)
INSERT INTO proposicoes (id_proposicao, id_autor, tipo, numero, ano, ementa, tema, data_apresentacao) VALUES
(101, 1, 'PL', 1234, 2026, 'Altera o Estatuto da Criança e do Adolescente para tipificar o crime de cyberbullying em plataformas de jogos online.', 'Proteção Infantil Digital', '2026-04-10'),
(102, 2, 'PL', 5678, 2026, 'Cria diretrizes rigorosas para moderação de conteúdo sensível em redes sociais frequentadas por menores de 18 anos.', 'Segurança Digital', '2026-04-15');
ON CONFLICT DO NOTHING