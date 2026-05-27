import React from 'react';
import { FaGithub } from 'react-icons/fa';

export default function Footer() {
  return (
    <footer className="bg-[#242D35] text-[#E1E1E1] border-t border-[#E1E1E1]/10 px-6 pt-12 pb-6 font-serif">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 items-start mb-10 text-center md:text-left">
        
        
        <div className="flex flex-col space-y-4 items-center md:items-start">
          <div className="flex items-center text-2xl font-bold tracking-wide text-white uppercase">
            <span>Protect</span>
            <span className="bg-[#8D0000] text-white px-2 py-0.5 rounded ml-1.5 text-xl font-sans font-black tracking-normal">
              KIDS
            </span>
          </div>
          <p className="text-xs tracking-wider uppercase leading-relaxed max-w-sm text-[#E1E1E1]/80">
            Plataforma de transparência para monitoramento de legislações sobre 
            proteção infantil e combate ao cyberbullying.
          </p>
        </div>

        
        <div className="flex flex-col space-y-3 items-center md:items-start">
          <h3 className="text-sm font-bold tracking-widest uppercase text-white">
            Links Úteis
          </h3>
          <ul className="space-y-2 text-xs uppercase tracking-widest list-disc list-inside md:list-outside md:pl-4 text-[#E1E1E1]/90">
            <li>
              <a href="https://www.camara.leg.br/" target="_blank" rel="noreferrer" className="underline underline-offset-4 hover:text-white transition-colors">
                Câmara dos Deputados
              </a>
            </li>
            <li>
              <a href="https://www.gov.br/mdh/pt-br" target="_blank" rel="noreferrer" className="underline underline-offset-4 hover:text-white transition-colors">
                Ministério dos Direitos Humanos
              </a>
            </li>
            <li>
              <a href="https://www.planalto.gov.br/ccivil_03/leis/l8069.htm" target="_blank" rel="noreferrer" className="underline underline-offset-4 hover:text-white transition-colors">
                Estatuto da Criança e Adolescente
              </a>
            </li>
          </ul>
        </div>

        <div className="flex flex-col space-y-3 items-center md:items-start">
          <h3 className="text-sm font-bold tracking-widest uppercase text-white">
            Projeto
          </h3>
          <a 
            href="https://github.com/unb-mds/2026-1-ProtectKids" 
            target="_blank" 
            rel="noreferrer" 
            className="flex items-center space-x-2 text-xs uppercase tracking-widest group"
          >
            
            <FaGithub className="h-6 w-6 text-white group-hover:scale-105 transition-transform" />
            <span className="underline underline-offset-4 text-[#E1E1E1]/90 group-hover:text-white transition-colors">
              Repositório no GitHub
            </span>
          </a>
        </div>

      </div>

      
      <div className="border-t border-[#E1E1E1]/5 pt-6 text-center space-y-1 text-[10px] md:text-xs tracking-widest uppercase text-[#E1E1E1]/60">
        <p>© 2026 ProtectKids - Projeto Acadêmico de Engenharia de Software</p>
        <p>Dados obtidos via API da Câmara dos Deputados</p>
      </div>
    </footer>
  );
}