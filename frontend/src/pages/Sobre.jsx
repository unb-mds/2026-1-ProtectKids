import { Shield, Target, Users, Code } from 'lucide-react';

export default function Sobre() {
  return (
    <div className="flex flex-col w-full">
      {/* CABEÇALHO */}
    <div className="block w-full bg-[#FBBF24] py-10 px-4 text-center select-none clearfix">
      <div className="max-w-7xl mx-auto flex flex-col items-center justify-center">
        {/* Container do Título Principal */}
        <h1 className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-2xl sm:text-3xl md:text-4xl uppercase tracking-wide">
          {/* "SOBRE O" em tom azul escuro e fonte serifada */}
          <span className="font-serif font-bold text-[#1E3A8A]">
            Sobre o
          </span>
          
          {/* "PROTECT" em branco e fonte sans-serif */}
          <span className="font-sans font-extrabold text-white">
            Protect
          </span>
          
          {/* "KIDS" dentro do badge azul escuro */}
          <span className="bg-[#1E3A8A] text-[#FBBF24] font-sans font-black px-3 py-1 rounded-xl text-xl sm:text-2xl md:text-3xl tracking-wider inline-block">
            Kids
          </span>
        </h1>

        {/* Subtítulo */}
        <p className="mt-4 text-[#1E3A8A]/90 text-xs sm:text-sm md:text-base font-bold tracking-normal max-w-2xl font-sans">
          Plataforma de transparência e monitoramento legislativo focada em proteção infantil
        </p>
      </div>
    </div>

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