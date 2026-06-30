export default function Footer() {
  return (
    <footer className="bg-[#2563EB] text-white px-6 py-12 flex flex-col gap-10 font-sans select-none w-full relative">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 w-full items-start">
        <div className="flex flex-col gap-4 text-center md:text-left items-center md:items-start">
          <div className="flex items-center gap-2 font-sans">
            <span className="text-3xl font-bold tracking-wide uppercase">
              Protect
            </span>
            <span className="bg-[#FBBF24] text-[#1E293B] text-2xl font-black px-3 py-1 rounded-md uppercase tracking-wider">
              Kids
            </span>
          </div>
          <p className="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-[#1E293B] max-w-xs leading-relaxed">
            Plataforma de transparência para monitoramento de proposições sobre
            proteção infantil e combate ao cyberbullying.
          </p>
        </div>

        <div className="flex flex-col gap-3 items-center md:items-start">
          <h4 className="text-base sm:text-lg font-bold font-serif text-[#1E293B] tracking-wide">
            Links Úteis
          </h4>
          <ul className="list-disc list-inside md:list-outside flex flex-col gap-2 font-serif text-sm font-bold uppercase tracking-wide">
            <li>
              <a href="https://www.camara.leg.br/" target="_blank" rel="noreferrer" className="underline hover:opacity-80 transition-opacity">
                Câmara dos Deputados
              </a>
            </li>
            <li>
              <a href="https://www12.senado.leg.br/" target="_blank" rel="noreferrer" className="underline hover:opacity-80 transition-opacity">
                Senado Federal
              </a>
            </li>
            <li>
              <a href="https://www.gov.br/mdh/pt-br" target="_blank" rel="noreferrer" className="underline hover:opacity-80 transition-opacity">
                Ministério dos Direitos Humanos
              </a>
            </li>
            <li>
              <a
                href="https://www.gov.br/mdh/pt-br/assuntos/noticias/2021/julho/trinta-e-um-anos-do-estatuto-da-crianca-e-do-adolescente-confira-as-novas-acoes-para-fortalecer-o-eca/ECA2021_Digital.pdf"
                target="_blank"
                rel="noreferrer"
                className="underline hover:opacity-80 transition-opacity"
              >
                Estatuto da Criança e Adolescente
              </a>
            </li>
          </ul>
        </div>

        <div className="flex flex-col gap-3 items-center md:items-start">
          <h4 className="text-base sm:text-lg font-bold font-serif text-[#1E293B] tracking-wide">
            Projeto
          </h4>
          <a
            href="https://github.com/unb-mds/2026-1-ProtectKids"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-2 text-sm sm:text-base font-bold font-serif uppercase tracking-wide underline hover:opacity-80 transition-opacity group"
          >
            <svg className="w-6 h-6 fill-white transition-transform group-hover:scale-105" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
            Repositório no GitHub
          </a>
        </div>
      </div>

      <div className="border-t border-[#1E293B]/20 pt-6 text-center text-[11px] sm:text-xs font-bold uppercase tracking-wider text-[#1E293B]/90 font-serif flex flex-col gap-1">
        <p>© 2026 ProtectKids - Projeto Acadêmico de Engenharia de Software</p>
        <p className="opacity-80">
          Dados obtidos via APIs oficiais da Câmara dos Deputados e do Senado Federal
        </p>
      </div>
    </footer>
  );
}