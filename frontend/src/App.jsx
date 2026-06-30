import { lazy, Suspense } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import ScrollToTop from './components/ScrollToTop';

const Inicio = lazy(() => import('./pages/Inicio'));
const TodasAsLeis = lazy(() => import('./pages/TodasAsLeis'));
const DetalhesLei = lazy(() => import('./pages/DetalhesLei'));
const Sobre = lazy(() => import('./pages/Sobre'));
const Estatisticas = lazy(() => import('./pages/Estatisticas'));
const DetalhesSubtema = lazy(() => import('./pages/DetalhesSubtema'));

function CarregandoPagina() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center bg-[#E5E5E5] text-[#001B5E] font-bold">
      Carregando página...
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#E5E5E5]">
        <ScrollToTop />
        <Header />

        <main className="flex-grow">
          <Suspense fallback={<CarregandoPagina />}>
            <Routes>
              <Route path="/" element={<Inicio />} />
              <Route path="/leis" element={<TodasAsLeis />} />
              <Route path="/leis/:id" element={<DetalhesLei />} />
              <Route path="/estatisticas" element={<Estatisticas />} />
              <Route path="/sobre" element={<Sobre />} />
              <Route path="/estatisticas/subtema/:slug" element={<DetalhesSubtema />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </Suspense>
        </main>

        <Footer />
      </div>
    </BrowserRouter>
  );
}