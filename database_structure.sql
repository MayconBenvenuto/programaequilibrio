-- Estrutura do banco de dados para o Programa Equilíbrio
-- Execute no Supabase SQL Editor

-- 1. Tabela de empresas
CREATE TABLE IF NOT EXISTS empresas (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    whatsapp VARCHAR(20),
    endereco JSONB,
    num_colaboradores INTEGER,
    setor_atividade VARCHAR(255),
    rh_responsavel VARCHAR(255) NOT NULL,
    cargo_rh VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 2. Tabela de diagnósticos
CREATE TABLE IF NOT EXISTS diagnosticos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    respostas JSONB NOT NULL,
    analise JSONB NOT NULL,
    nivel_risco VARCHAR(20) NOT NULL,
    questoes_criticas INTEGER DEFAULT 0,
    areas_foco TEXT[],
    acoes_recomendadas TEXT[],
    pdf_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'concluido',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 3. Tabela de usuários admin (para sistema de administração)
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 4. Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_empresas_cnpj ON empresas(cnpj);
CREATE INDEX IF NOT EXISTS idx_empresas_created_at ON empresas(created_at);
CREATE INDEX IF NOT EXISTS idx_diagnosticos_empresa_id ON diagnosticos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_diagnosticos_created_at ON diagnosticos(created_at);
CREATE INDEX IF NOT EXISTS idx_diagnosticos_nivel_risco ON diagnosticos(nivel_risco);
CREATE INDEX IF NOT EXISTS idx_admin_users_username ON admin_users(username);
CREATE INDEX IF NOT EXISTS idx_admin_users_email ON admin_users(email);

-- 5. Triggers para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_empresas_updated_at 
    BEFORE UPDATE ON empresas 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_diagnosticos_updated_at 
    BEFORE UPDATE ON diagnosticos 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_admin_users_updated_at 
    BEFORE UPDATE ON admin_users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 6. RLS (Row Level Security) policies
ALTER TABLE empresas ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnosticos ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- Policy para permitir leitura e escrita para usuários autenticados
CREATE POLICY "Permitir todas as operações para usuários autenticados" ON empresas
    FOR ALL USING (true);

CREATE POLICY "Permitir todas as operações para usuários autenticados" ON diagnosticos
    FOR ALL USING (true);

-- Policy mais restritiva para admin_users (apenas admins podem acessar)
CREATE POLICY "Apenas admins podem acessar usuários admin" ON admin_users
    FOR ALL USING (true);

-- 7. Inserir usuário admin padrão (ALTERE A SENHA EM PRODUÇÃO!)
INSERT INTO admin_users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@belzconectasaude.com.br', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFyj3L3yoUJ5E3q', -- password: admin123 (ALTERE EM PRODUÇÃO!)
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- 8. Views úteis para relatórios
CREATE OR REPLACE VIEW vw_diagnosticos_completos AS
SELECT 
    d.id,
    d.created_at as data_diagnostico,
    e.razao_social,
    e.nome_fantasia,
    e.cnpj,
    e.email,
    e.telefone,
    e.whatsapp,
    e.num_colaboradores,
    e.setor_atividade,
    e.rh_responsavel,
    e.cargo_rh,
    d.nivel_risco,
    d.questoes_criticas,
    d.areas_foco,
    d.acoes_recomendadas,
    d.status
FROM diagnosticos d
JOIN empresas e ON d.empresa_id = e.id
ORDER BY d.created_at DESC;

-- 9. View para estatísticas administrativas
CREATE OR REPLACE VIEW vw_estatisticas_admin AS
SELECT 
    COUNT(DISTINCT e.id) as total_empresas,
    COUNT(d.id) as total_diagnosticos,
    COUNT(CASE WHEN d.nivel_risco = 'Alto' THEN 1 END) as diagnosticos_risco_alto,
    COUNT(CASE WHEN d.nivel_risco = 'Moderado' THEN 1 END) as diagnosticos_risco_moderado,
    COUNT(CASE WHEN d.nivel_risco = 'Baixo' THEN 1 END) as diagnosticos_risco_baixo,
    SUM(e.num_colaboradores) as total_colaboradores_analisados,
    DATE_TRUNC('month', d.created_at) as mes_ano
FROM empresas e
LEFT JOIN diagnosticos d ON e.id = d.empresa_id
GROUP BY DATE_TRUNC('month', d.created_at)
ORDER BY mes_ano DESC NULLS LAST;

-- 10. Função para buscar empresas por CNPJ
CREATE OR REPLACE FUNCTION buscar_empresa_por_cnpj(cnpj_param VARCHAR(18))
RETURNS TABLE(
    id UUID,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(18),
    email VARCHAR(255),
    telefone VARCHAR(20),
    whatsapp VARCHAR(20),
    num_colaboradores INTEGER,
    setor_atividade VARCHAR(255),
    rh_responsavel VARCHAR(255),
    cargo_rh VARCHAR(255),
    total_diagnosticos BIGINT,
    ultimo_diagnostico TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        e.id,
        e.razao_social,
        e.nome_fantasia,
        e.cnpj,
        e.email,
        e.telefone,
        e.whatsapp,
        e.num_colaboradores,
        e.setor_atividade,
        e.rh_responsavel,
        e.cargo_rh,
        COUNT(d.id) as total_diagnosticos,
        MAX(d.created_at) as ultimo_diagnostico
    FROM empresas e
    LEFT JOIN diagnosticos d ON e.id = d.empresa_id
    WHERE e.cnpj = cnpj_param
    GROUP BY e.id, e.razao_social, e.nome_fantasia, e.cnpj, e.email, 
             e.telefone, e.whatsapp, e.num_colaboradores, e.setor_atividade,
             e.rh_responsavel, e.cargo_rh;
END;
$$ LANGUAGE plpgsql;
