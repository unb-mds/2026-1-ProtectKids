import { Search, TrendingUp, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Inicio() {
 return (
   <>
    <div className="w-full select-none">
      <div className="w-full select-none">
        {/* Linha azul superior */}
        <div className="h-2 bg-[#1E3A8A]"></div>
        
        {/* Banner amarelo com o título */}
        <div className="bg-[#FBBF24] py-6 px-4 flex justify-center items-center">
          <h1 className="text-[#1E3A8A] text-2xl sm:text-3xl md:text-4xl font-bold uppercase tracking-wide font-serif text-center">
            Dashboard Analítico
          </h1>
        </div>
      </div>

      <section className="bg-[#F8FAFC] p-4 md:p-6 w-full min-h-screen font-sans">
        <div className="max-w-7xl mx-auto flex flex-col gap-6">
        
        {/* 1. Card: Nuvem de Palavras */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-4">
          <div className="flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
            {/* Ícone representando Nuvem / Nuvem de Palavras */}
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15a4.5 4.5 0 0 0 4.5 4.5H18a3.75 3.75 0 0 0 1.332-7.257 3 3 0 0 0-3.758-3.848 5.25 5.25 0 0 0-10.233 2.33A4.502 4.502 0 0 0 2.25 15z" />
            </svg>
            <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-700">
              Nuvem de Palavras
            </h2>
          </div>
          {/* Container para a API de Nuvem de Palavras */}
          <div className="w-full min-h-[160px] flex items-center justify-center text-gray-400 text-sm italic bg-slate-50/50 rounded-xl border border-dashed border-gray-200">
            Espaço para o gráfico da API (Nuvem de Palavras)
          </div>
        </div>

        {/* 2. Card: Volume de Proposições por Subtema (NLP) */}
        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-4">
          <div className="flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
            {/* Ícone de Relógio / Histórico */}
            <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-700">
              Volume de Proposições por Subtema (NLP)
            </h2>
          </div>
          {/* Subgrid interno para os dois gráficos lado a lado */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 min-h-[300px]">
            <div className="flex items-center justify-center text-gray-400 text-sm italic bg-slate-50/50 rounded-xl border border-dashed border-gray-200 p-4">
              API: Gráfico de Barras (Quantidade)
            </div>
            <div className="flex items-center justify-center text-gray-400 text-sm italic bg-slate-50/50 rounded-xl border border-dashed border-gray-200 p-4">
              API: Gráfico de Rosca (Distribuição %)
            </div>
          </div>
        </div>

        {/* 3. Grid Inferior: Top Parlamentares e Engajamento por Partido */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          {/* Card: Top Parlamentares */}
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
              {/* Ícone de Medalha / Rank */}
              <svg className="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 0 1 3 3h-15a3 3 0 0 1 3-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-6.75a1.125 1.125 0 0 0-1.125 1.125v3.375m9 0ZM9 10.5h.008v.008H9V10.5Zm6 0h.008v.008H15V10.5Z" />
              </svg>
              <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-700">
                Top Parlamentares
              </h2>
            </div>
            {/* Container para a API do Top List */}
            <div className="w-full min-h-[220px] flex items-center justify-center text-gray-400 text-sm italic bg-slate-50/50 rounded-xl border border-dashed border-gray-200">
              API: Lista / Gráfico de Barras de Parlamentares
            </div>
          </div>

          {/* Card: Engajamento por Partido */}
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3 mb-4">
              {/* Ícone de Usuários / Partido */}
              <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
              </svg>
              <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-700">
                Engajamento por Partido
              </h2>
            </div>
            {/* Container para a API de Partidos */}
            <div className="w-full min-h-[220px] flex items-center justify-center text-gray-400 text-sm italic bg-slate-50/50 rounded-xl border border-dashed border-gray-200">
              API: Gráfico de Pizza + Tabela de Partidos
            </div>
          </div>

        </div>

        </div>
      </section>
    </div>

    <section className="bg-[#FF7A1A] text-white w-full min-h-[500px] flex items-center px-4 sm:px-8 md:px-16 py-12 select-none font-sans">
      {/* Alterado para max-w-full e justify-between para colar os blocos nas extremidades */}
      <div className="w-full max-w-full grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
        
        {/* Lado Esquerdo: Textos e Botões (Ocupa 7 das 12 colunas em telas grandes) */}
        <div className="flex flex-col gap-6 lg:col-span-7">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold uppercase tracking-wide leading-tight text-slate-900 font-serif">
            Monitorando Leis de{' '}
            <span className="text-[#0038A8]">Proteção Infantil</span> e Combate ao{' '}
            <span className="block xl:inline">Cyberbullying</span>
          </h1>
          
          <p className="text-base sm:text-lg md:text-xl font-bold text-slate-900 max-w-3xl leading-relaxed font-sans">
            Acompanhe em tempo real as proposições legislativas da Câmara dos Deputados voltadas para a segurança digital e proteção de crianças e adolescentes.
          </p>
          
          {/* Container dos Botões */}
          <div className="flex flex-wrap gap-4 mt-2">
            {/* Botão Principal (Azul) */}
            <a 
              href="#proposicoes" 
              className="bg-[#0038A8] hover:bg-[#002b80] text-white font-serif font-bold text-sm sm:text-base px-6 py-3.5 rounded-lg flex items-center gap-2 transition-all shadow-md group uppercase tracking-wider"
            >
              Ver as proposições 
              <span className="inline-block transform group-hover:translate-x-1 transition-transform">→</span>
            </a>
            
            {/* Botão Secundário (Roxo Cinzento) */}
            <a 
              href="#sobre" 
              className="bg-[#5D4E6D] hover:bg-[#4d405a] border border-slate-700 text-white font-serif font-bold text-sm sm:text-base px-6 py-3.5 rounded-lg flex items-center gap-2 transition-all shadow-md uppercase tracking-wider"
            >
              Sobre o projeto 
              <span className="text-gray-300 font-mono">&lt;/&gt;</span>
            </a>
          </div>
        </div>

        {/* Lado Direito: Espaço para a Imagem (Ocupa 5 das 12 colunas em telas grandes) */}
        <div className="w-full h-[300px] sm:h-[400px] lg:h-[450px] lg:col-span-5 relative rounded-2xl overflow-hidden shadow-xl border border-white/10 bg-orange-600/30 flex items-center justify-center">
          {/* Substitua a tag abaixo pelo seu componente de imagem final.
            Exemplo: <img src="/caminho-da-sua-imagem.png" alt="Crianças brincando" className="w-full h-full object-cover" />
          */}
          <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center text-white/80 border-4 border-dashed border-white/20 rounded-2xl">
            <svg className="w-14 h-14 mb-3 opacity-60" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
            </svg>
            <span className="text-sm font-semibold uppercase tracking-wider">Espaço reservado para a Imagem</span>
            <span className="text-xs opacity-60 mt-1">(Preenchimento total da lateral)</span>
          </div>
        </div>

      </div>
     </section>

     <section className="bg-[#EFEFEF] py-12 px-6 w-full flex justify-center items-center font-sans select-none">
      <div className="w-full max-w-7xl grid grid-cols-1 md:grid-cols-3 gap-30">
        
        {/* Card 1: Transparência Total (Amarelo) */}
        <div className="bg-[#EAB308] border-[3px] border-[#6B7280] rounded-[24px] p-6 flex flex-col items-center text-center justify-between min-h-[250px] shadow-sm">
          <div className="flex flex-col gap-3">
            <h3 className="text-white text-lg sm:text-xl font-bold font-serif uppercase tracking-wider">
              Transparência Total
            </h3>
            <p className="text-white text-xs sm:text-sm font-medium uppercase tracking-wide leading-relaxed max-w-xs opacity-90">
              Todos os dados são obtidos diretamente da API oficial da Câmara dos Deputados, garantindo informações atualizadas e confiáveis.
            </p>
          </div>
          {/* Ícone de Escudo com Check */}
          <div className="mt-4">
            <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.745 3.745 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
            </svg>
          </div>
        </div>

        {/* Card 2: Foco Especializado (Azul) */}
        <div className="bg-[#1D4ED8] border-[3px] border-[#6B7280] rounded-[24px] p-6 flex flex-col items-center text-center justify-between min-h-[250px] shadow-sm">
          <div className="flex flex-col gap-3">
            <h3 className="text-white text-lg sm:text-xl font-bold font-serif uppercase tracking-wider">
              Foco Especializado
            </h3>
            <p className="text-white text-xs sm:text-sm font-medium uppercase tracking-wide leading-relaxed max-w-xs opacity-90">
              Filtramos apenas proposições relacionadas à proteção infantil, cyberbullying e segurança digital de menores.
            </p>
          </div>
          {/* Ícone de Exclamação/Alerta */}
          <div className="mt-4">
            <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
          </div>
        </div>

        {/* Card 3: Acompanhamento em Tempo Real (Laranja) */}
        <div className="bg-[#EA580C] border-[3px] border-[#6B7280] rounded-[24px] p-6 flex flex-col items-center text-center justify-between min-h-[250px] shadow-sm">
          <div className="flex flex-col gap-3">
            <h3 className="text-white text-lg sm:text-xl font-bold font-serif uppercase tracking-wider">
              Acompanhamento em Tempo Real
            </h3>
            <p className="text-white text-xs sm:text-sm font-medium uppercase tracking-wide leading-relaxed max-w-xs opacity-90">
              Monitore o status de cada proposição, desde a apresentação até a aprovação ou arquivamento.
            </p>
          </div>
          {/* Ícone de Gráfico de Tendência para Cima */}
          <div className="mt-4">
            <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
            </svg>
          </div>
        </div>

      </div>
    </section>
    </>
   );

}