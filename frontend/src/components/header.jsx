import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-[#2563EB] text-white px-6 md:px-12 py-4 border-b-4 border-[#FACC15]">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-5">
        <Link to="/" className="flex flex-col gap-1 select-none">
          <div className="flex items-center gap-1 font-serif">
            <span className="text-3xl md:text-4xl font-black uppercase tracking-wide">
              Protect
            </span>
            <span className="bg-[#FACC15] text-[#111827] px-2 rounded-sm text-2xl md:text-3xl font-black uppercase">
              Kids
            </span>
          </div>

          <p className="text-[10px] md:text-xs font-bold uppercase tracking-wide text-[#111827] max-w-xs leading-tight">
            Monitoramento Legislativo para Proteção Infantil
          </p>
        </Link>

        <nav>
          <ul className="flex flex-wrap items-center gap-6 md:gap-10 font-serif text-sm md:text-base font-bold uppercase tracking-wide">
            <li>
              <Link to="/" className="hover:text-[#FACC15] transition">
                Início
              </Link>
            </li>
            <li>
              <Link to="/leis" className="hover:text-[#FACC15] transition">
                Todas as Leis
              </Link>
            </li>
            <li>
              <Link to="/sobre" className="hover:text-[#FACC15] transition">
                Sobre o Projeto
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}