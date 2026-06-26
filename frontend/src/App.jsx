import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import TodasAsLeis from './pages/TodasAsLeis';
import Inicio from './pages/Inicio';
import DetalhesLei from './pages/DetalhesLei';
import Sobre from './pages/Sobre';
import Estatisticas from './pages/Estatisticas';
import Footer from './components/Footer';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col font-sans">
        
        {/* NAVBAR */}
        <header className="bg-[#2563EB] text-white px-6 py-5 flex flex-col md:flex-row md:items-center md:justify-between font-serif select-none">
      
      <div className="flex flex-col gap-2">
       
        <div className="flex items-center gap-2 font-sans">
          <span className="text-3xl sm:text-4xl font-bold tracking-wide uppercase">
            Protect
          </span>
          <span className="bg-[#FBBF24] text-[#1E293B] text-2xl sm:text-3xl font-black px-3 py-1 rounded-md uppercase tracking-wider">
            Kids
          </span>
        </div>
        <p className="text-[11px] sm:text-xs font-bold uppercase tracking-wider text-[#1E293B]/80 max-w-xs leading-tight">
          Monitoramento Legislativo para Proteção Infantil
        </p>
      </div>

      
      <nav className="mt-5 md:mt-0">
        <ul className="flex flex-wrap items-center gap-6 sm:gap-8 text-sm sm:text-base tracking-wide font-medium">
          <li>
            <a href="#inicio" className="uppercase hover:opacity-80 transition-opacity">
              Início
            </a>
          </li>
          <li>
            <a href="#todas-as-leis" className="uppercase hover:opacity-80 transition-opacity">
              Todas as Leis
            </a>
          </li>
          <li>
            <a href="#sobre" className="uppercase hover:opacity-80 transition-opacity">
              Sobre o Projeto
            </a>
          </li>
        </ul>
      </nav>
    </header>

        {/* CONTEÚDO DINÂMICO */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/leis" element={<TodasAsLeis />} />
            <Route path="/leis/:id" element={<DetalhesLei />} />
            <Route path="/sobre" element={<Sobre />} />
            <Route path="/estatisticas" element={<Estatisticas />} />
          </Routes>
        </main>

        <Footer />
        
      </div>
    </BrowserRouter>
  );
}

export default App;