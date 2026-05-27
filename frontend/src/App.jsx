import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import TodasAsLeis from './pages/TodasAsLeis';
import Inicio from './pages/Inicio';
import DetalhesLei from './pages/DetalhesLei';
import Sobre from './pages/Sobre';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col font-sans">
        
        {/* NAVBAR */}
        <nav className="bg-pk-red text-white py-4 px-8 flex justify-between items-center shadow-md">
          <div className="font-bold text-2xl tracking-tighter">
            PROTECT<span className="text-gray-300">KIDS</span>
            <p className="text-xs font-normal text-gray-300 uppercase tracking-widest mt-1">
              Monitoramento Legislativo
            </p>
          </div>
          <div className="space-x-6 text-sm font-semibold">
            <Link to="/" className="hover:text-gray-300 transition">INÍCIO</Link>
            <Link to="/leis" className="hover:text-gray-300 transition">TODAS AS LEIS</Link>
            <Link to="/sobre" className="hover:text-gray-300 transition">SOBRE O PROJETO</Link>
          </div>
        </nav>

        {/* CONTEÚDO DINÂMICO */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/leis" element={<TodasAsLeis />} />
            <Route path="/leis" element={<TodasAsLeis />} />
            <Route path="/leis/:id" element={<DetalhesLei />} />
            <Route path="/sobre" element={<Sobre />} />
          </Routes>
        </main>

        {/* FOOTER */}
        <footer className="bg-pk-dark text-white py-8 px-8 text-sm flex justify-between items-start mt-12">
          <div>
             <div className="font-bold text-xl mb-2">PROTECT<span className="text-gray-400">KIDS</span></div>
             <p className="text-gray-400 max-w-xs">Plataforma de transparência para monitoramento de legislações sobre proteção infantil.</p>
          </div>
          <div className="text-center text-gray-500 text-xs mt-8">
            © 2026 ProtectKids - Projeto Acadêmico de Engenharia de Software
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;