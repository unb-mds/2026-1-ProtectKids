import { Search, TrendingUp, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Inicio() {
  // Dados estáticos baseados no design para garantir o carregamento instantâneo do MVP
  const destaques = [
    {
      id: "2814-2026",
      numero: "2814",
      ano: "2026",
      status: "Em Tramitação",
      statusColor: "bg-yellow-100 text-yellow-800 border-yellow-200",
      nlp: "Proteção Digital Infantil",
      ementa: "Altera o Estatuto da Criança e do Adolescente para incluir proteções específicas contra crimes digitais, estabelecendo responsabilidades para plataformas e ...",
      data: "15/03/2026",
      autor: "Dep. Maria Silva - PT/SP"
    },
    {
      id: "1823-2026",
      numero: "1823",
      ano: "2026",
      status: "Em Tramitação",
      statusColor: "bg-yellow-100 text-yellow-800 border-yellow-200",
      nlp: "Combate ao Cyberbullying",
      ementa: "Tipifica o cyberbullying como crime autônomo e estabelece penas específicas para casos envolvendo menores de idade, incluindo medidas educativas e...",
      data: "08/02/2026",
      autor: "Dep. João Santos - PSDB/RJ"
    },
    {
      id: "945-2025",
      numero: "945",
      ano: "2025",
      status: "Aprovada",
      statusColor: "bg-green-100 text-green-800 border-green-200",
      nlp: "Segurança em Redes Sociais",
      ementa: "Determina que plataformas digitais implementem mecanismos de verificação de idade e controle parental obrigatório para usuários menores de 13 anos.",
      data: "20/12/2025",
      autor: "Dep. Ana Paula Costa - PDT/MG"
    }
  ];

  return (
    <div className="flex flex-col w-full">
      
      {/* HERO SECTION */}
      <section className="bg-pk-dark text-white py-16 px-8 flex justify-center shadow-inner">
        <div className="max-w-6xl w-full flex flex-col items-start">
          <h1 className="text-3xl md:text-5xl font-bold tracking-wide leading-tight mb-6 max-w-4xl uppercase font-serif">
            Monitorando Leis de <span className="text-[#22c55e]">Proteção</span><br />
            <span className="text-[#22c55e]">Infantil</span> e Combate ao Cyberbullying
          </h1>
          <p className="text-gray-300 font-semibold text-sm md:text-base mb-10 max-w-3xl uppercase tracking-wider">
            Acompanhe em tempo real as proposições legislativas da Câmara dos Deputados voltadas para a segurança digital e proteção de crianças e adolescentes.
          </p>
          <div className="flex flex-wrap gap-4 w-full">
            <Link to="/leis" className="bg-white text-gray-900 px-6 py-3 rounded shadow hover:bg-gray-100 transition flex items-center gap-2 font-bold">
              <Search size={20} /> Explorar Legislações
            </Link>
            <Link to="/sobre" className="bg-transparent border border-gray-400 text-gray-200 px-6 py-3 rounded hover:bg-gray-800 transition flex items-center gap-2 font-bold">
              <TrendingUp size={20} /> Sobre o Projeto
            </Link>
          </div>
        </div>
      </section>

      {/* SEÇÃO PRINCIPAIS LEGISLAÇÕES */}
      <section className="py-16 px-4 max-w-6xl mx-auto w-full flex flex-col items-center text-center">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2 uppercase font-serif tracking-wide">
          Principais Legislações em Andamento
        </h2>
        <p className="text-gray-500 font-semibold text-sm uppercase tracking-widest mb-6">
          Acompanhe as proposições mais relevantes relacionadas à proteção de crianças e adolescentes no ambiente digital.
        </p>
        
        <span className="inline-flex items-center gap-2 bg-blue-50 text-blue-600 border border-blue-200 px-4 py-1.5 rounded-full text-sm font-bold mb-12 shadow-sm">
          <TrendingUp size={16} /> Proposições em Destaque
        </span>

        {/* GRID DE CARDS MOCKADOS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full text-left mb-10">
          {destaques.map((lei) => (
            <div key={lei.id} className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6 flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-gray-900">PL {lei.numero}/{lei.ano}</h3>
                <span className={`text-[10px] font-bold px-2 py-1 rounded-full border uppercase ${lei.statusColor}`}>
                  {lei.status}
                </span>
              </div>
              
              <span className="inline-block bg-blue-50 text-blue-600 text-xs font-bold px-3 py-1 rounded w-max mb-4 border border-blue-100">
                {lei.nlp}
              </span>

              <p className="text-gray-700 text-sm mb-6 flex-grow leading-relaxed">
                {lei.ementa}
              </p>

              <div className="text-xs text-gray-600 mb-4 font-medium">
                <p>Apresentada em {lei.data}</p>
                <p>{lei.autor}</p>
              </div>

              <Link to="/leis" className="w-full bg-pk-red hover:bg-red-900 text-white font-bold py-2.5 rounded flex justify-center items-center gap-2 transition shadow-md">
                Ver Detalhes Completos <ArrowRight size={16} />
              </Link>
            </div>
          ))}
        </div>

        <Link to="/leis" className="bg-pk-red hover:bg-red-900 text-white px-8 py-3 rounded shadow-md transition font-bold tracking-wide">
          Ver Todas as Proposições
        </Link>
      </section>

      {/* SEÇÃO DE FEATURES */}
      <section className="pb-16 px-4 max-w-6xl mx-auto w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-[#f0f4ff] border-2 border-blue-200 rounded-xl p-8 flex flex-col items-center text-center shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 uppercase font-serif tracking-wide mb-3">Transparência Total</h3>
            <p className="text-gray-600 text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Todos os dados são obtidos diretamente da API oficial da Câmara dos Deputados, garantindo informações atualizadas e confiáveis.
            </p>
            <ShieldCheck size={32} className="text-gray-800 mt-auto" />
          </div>

          <div className="bg-[#fffbeb] border-2 border-yellow-200 rounded-xl p-8 flex flex-col items-center text-center shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 uppercase font-serif tracking-wide mb-3">Foco Especializado</h3>
            <p className="text-gray-600 text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Filtramos apenas proposições relacionadas à proteção infantil, cyberbullying e segurança digital de menores.
            </p>
            <AlertCircle size={32} className="text-gray-800 mt-auto" />
          </div>

          <div className="bg-[#fff1f2] border-2 border-red-200 rounded-xl p-8 flex flex-col items-center text-center shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 uppercase font-serif tracking-wide mb-3">Acompanhamento em Tempo Real</h3>
            <p className="text-gray-600 text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Monitore o status de cada proposição, desde a apresentação até a aprovação ou arquivamento.
            </p>
            <TrendingUp size={32} className="text-gray-800 mt-auto" />
          </div>

        </div>
      </section>
    </div>
  );
}