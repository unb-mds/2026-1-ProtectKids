import { Shield, Target, Users, Code } from 'lucide-react';

export default function Sobre() {
  return (
    <div className="flex flex-col w-full">
      {/* CABEÇALHO */}
      <section className="bg-pk-dark text-white py-16 px-8 flex justify-center shadow-inner">
        <div className="max-w-4xl w-full text-center">
          <h1 className="text-3xl md:text-5xl font-bold tracking-wide leading-tight mb-4 uppercase font-serif">
            Sobre o <span className="text-pk-red">Projeto</span>
          </h1>
          <p className="text-gray-300 font-medium text-sm md:text-base max-w-2xl mx-auto uppercase tracking-wider">
            Conheça o contexto, a missão e a equipe por trás da plataforma ProtectKids.
          </p>
        </div>
      </section>

      {/* CONTEÚDO PRINCIPAL */}
      <section className="py-16 px-4 max-w-4xl mx-auto w-full flex flex-col gap-12">
        
        {/* Nossa Missão */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 flex flex-col md:flex-row gap-6 items-start">
          <div className="bg-red-50 p-4 rounded-full">
            <Target size={32} className="text-pk-red" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3 font-serif">Nossa Missão</h2>
            <p className="text-gray-600 leading-relaxed">
              O ProtectKids nasceu com o objetivo de democratizar o acesso à informação legislativa. 
              Monitoramos e centralizamos propostas da Câmara dos Deputados que impactam diretamente 
              a segurança digital, combatem o cyberbullying e garantem a proteção de crianças e adolescentes.
            </p>
          </div>
        </div>

        {/* Arquitetura e Tecnologia */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 flex flex-col md:flex-row gap-6 items-start">
          <div className="bg-blue-50 p-4 rounded-full">
            <Code size={32} className="text-blue-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3 font-serif">Tecnologia (MVP)</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              A plataforma foi construída focando em alta disponibilidade e integração de ponta a ponta.
            </p>
            <ul className="list-disc list-inside text-gray-600 space-y-1 font-medium">
              <li><strong>Frontend:</strong> React + Vite + Tailwind CSS v4</li>
              <li><strong>Backend:</strong> FastAPI + Axios + Python + spaCy + PostgreSQL</li>
              <li><strong>Infraestrutura:</strong> Contêinerização completa com Docker</li>
              <li><strong>Inteligência:</strong> Classificação via NLP (Processamento de Linguagem Natural)</li>
            </ul>
          </div>
        </div>

        {/* Equipe */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 flex flex-col md:flex-row gap-6 items-start">
          <div className="bg-gray-100 p-4 rounded-full">
            <Users size={32} className="text-gray-700" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3 font-serif">Equipe de Desenvolvimento</h2>
            <p className="text-gray-600 leading-relaxed">
              Este projeto é mantido pelo <strong>Squad 10</strong> da turma de MDS da Professora Carla Rocha. Nossa equipe atua na idealização, 
              arquitetura de dados, design de interface e implementação de infraestrutura ágil para entregar 
              uma solução de impacto social.
            </p>
          </div>
        </div>

      </section>
    </div>
  );
}