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
      
      {/* HERO SECTION POLIDA (Baseada no Figma) */}
      <section className="bg-pk-dark text-white py-20 px-8 flex justify-center shadow-inner">
        <div className="max-w-6xl w-full flex flex-col items-start">
          
          <h1 className="font-serif text-[32px] md:text-[42px] font-bold text-white uppercase tracking-widest leading-[1.3] mb-8">
            Monitorando Leis de <span className="text-pk-neon">Proteção</span><br className="hidden md:block" />
            <span className="text-pk-neon">Infantil</span> e Combate ao Cyberbullying
          </h1>
          
          <p className="text-pk-light text-xs md:text-[13px] font-bold tracking-wider uppercase leading-loose max-w-4xl mb-12">
            Acompanhe em tempo real as proposições legislativas da Câmara dos Deputados voltadas para a segurança digital e proteção de crianças e adolescentes.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center gap-6 w-full md:w-auto">
            <Link 
              to="/leis" 
              className="w-full sm:w-auto bg-white text-pk-dark px-8 py-3.5 rounded font-bold text-sm tracking-wide flex items-center justify-center gap-3 hover:bg-gray-200 transition shadow-lg"
            >
              <Search size={18} /> Explorar Legislações
            </Link>
            
            <Link 
              to="/sobre" 
              className="w-full sm:w-auto bg-pk-red/30 text-white px-8 py-3.5 rounded font-bold text-sm tracking-wide flex items-center justify-center gap-3 hover:bg-pk-red/60 transition shadow-lg border border-white/10 backdrop-blur-sm"
            >
              <TrendingUp size={18} /> Sobre o Projeto
            </Link>
          </div>
        </div>
      </section>

      {}
      <section className="py-16 px-4 max-w-6xl mx-auto w-full flex flex-col items-center text-center">
        <h2 className="text-2xl md:text-3xl font-bold text-pk-dark mb-2 uppercase font-serif tracking-widest">
          Principais Legislações
        </h2>
        <p className="text-pk-gray font-semibold text-xs uppercase tracking-widest mb-6">
          Acompanhe as proposições mais relevantes em andamento
        </p>
        
        <span className="inline-flex items-center gap-2 bg-pk-blue/10 text-pk-blue border border-pk-blue/20 px-4 py-1.5 rounded-full text-sm font-bold mb-12 shadow-sm">
          <TrendingUp size={16} /> Proposições em Destaque
        </span>

        {}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full text-left mb-10">
          {destaques.map((lei) => (
            <div key={lei.id} className="bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow border border-gray-200 p-6 flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-pk-dark font-serif">PL {lei.numero}/{lei.ano}</h3>
                <span className={`text-[10px] font-bold px-2 py-1 rounded-full border uppercase tracking-wider ${lei.statusColor}`}>
                  {lei.status}
                </span>
              </div>
              
              <span className="inline-block bg-pk-blue/5 text-pk-blue text-xs font-bold px-3 py-1 rounded w-max mb-4 border border-pk-blue/10">
                {lei.nlp}
              </span>

              <p className="text-gray-700 text-sm mb-6 flex-grow leading-relaxed">
                {lei.ementa}
              </p>

              <div className="text-xs text-pk-gray mb-4 font-medium uppercase tracking-wider space-y-1">
                <p>Apresentada em: {lei.data}</p>
                <p>{lei.autor}</p>
              </div>

              <Link to="/leis" className="w-full bg-pk-red hover:bg-[#6b0000] text-white font-bold tracking-wide py-2.5 rounded flex justify-center items-center gap-2 transition shadow-sm text-sm">
                Ver Detalhes Completos <ArrowRight size={16} />
              </Link>
            </div>
          ))}
        </div>

        <Link to="/leis" className="bg-pk-blue hover:bg-[#1f2d36] text-white px-8 py-3.5 rounded shadow-md transition font-bold tracking-widest uppercase text-sm">
          Ver Todas as Proposições
        </Link>
      </section>

      {/* SEÇÃO DE FEATURES (Mantida com ajustes de cores) */}
      <section className="pb-16 px-4 max-w-6xl mx-auto w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-gray-50 border-2 border-pk-blue/10 rounded-xl p-8 flex flex-col items-center text-center shadow-sm hover:border-pk-blue transition-colors">
            <h3 className="text-lg font-bold text-pk-dark uppercase font-serif tracking-widest mb-3">Transparência Total</h3>
            <p className="text-pk-gray text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Todos os dados são obtidos diretamente da API oficial da Câmara dos Deputados.
            </p>
            <ShieldCheck size={32} className="text-pk-blue mt-auto" />
          </div>

          <div className="bg-gray-50 border-2 border-pk-red/10 rounded-xl p-8 flex flex-col items-center text-center shadow-sm hover:border-pk-red transition-colors">
            <h3 className="text-lg font-bold text-pk-dark uppercase font-serif tracking-widest mb-3">Foco Especializado</h3>
            <p className="text-pk-gray text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Filtramos apenas proposições relacionadas à proteção infantil e segurança digital.
            </p>
            <AlertCircle size={32} className="text-pk-red mt-auto" />
          </div>

          <div className="bg-gray-50 border-2 border-pk-neon/20 rounded-xl p-8 flex flex-col items-center text-center shadow-sm hover:border-pk-neon transition-colors">
            <h3 className="text-lg font-bold text-pk-dark uppercase font-serif tracking-widest mb-3">Tempo Real</h3>
            <p className="text-pk-gray text-xs font-semibold uppercase tracking-widest leading-relaxed mb-6">
              Monitore o status de cada proposição, da apresentação à aprovação.
            </p>
            <TrendingUp size={32} className="text-pk-neon mt-auto" />
          </div>

        </div>
      </section>
    </div>
  );
}