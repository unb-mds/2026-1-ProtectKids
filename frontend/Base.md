# Diretrizes de Identidade Visual (Frontend) — Protect Kids

Este documento estabelece as especificações da paleta de cores oficial para o portal de notícias **Protect Kids**. A combinação foi cuidadosamente planeada para garantir um visual leve, limpo e acolhedor para as Organizações Não Governamentais (ONGs), sem perder a sobriedade, a credibilidade e o profissionalismo exigidos por um público adulto.

---

## 🎨 Paleta de Cores Oficial

| Amostra | Nome Técnico | Código Hex | Função e Uso Recomendado |
| :---: | :--- | :---: | :--- |
| <img src="https://via.placeholder.com/15/F8F9FA/000000?text=+" width="15" height="15" /> | **Branco Off-White** | `#F8F9FA` | **Fundo Principal (Background):** Proporciona máxima leveza, respiro visual e reduz o cansaço ocular durante leituras prolongadas. |
| <img src="https://via.placeholder.com/15/24285A/000000?text=+" width="15" height="15" /> | **Azul Noturno Profundo** | `#24285A` | **Elementos de Identidade e Destaques:** Usado em cabeçalhos (headers), menus de navegação ou marcas secundárias para transmitir segurança e autoridade. |
| <img src="https://via.placeholder.com/15/414141/000000?text=+" width="15" height="15" /> | **Cinza Antracite** | `#414141` | **Tipografia Principal (Texto):** Substitui o preto puro para suavizar a leitura de artigos, mantendo um contraste ideal e acessível. |
| <img src="https://via.placeholder.com/15/FFD04D/000000?text=+" width="15" height="15" /> | **Amarelo Sol / Alerta** | `#FFD04D` | **Destaques e Notificações:** Perfeito para realçar categorias importantes, botões secundários, sinalizações de apoio ou secções especiais com energia positiva. |
| <img src="https://via.placeholder.com/15/00C5EE/000000?text=+" width="15" height="15" /> | **Ciano Proteção / Ação** | `#00C5EE` | **Ações Principais (CTA) e Links:** Cor de grande visibilidade, ideal para botões de denúncia, subscrição, suporte a ONGs e links ativos. |

---

## 🛠️ Implementação Técnica (CSS Variables)

Para garantir a consistência e facilidade de manutenção no desenvolvimento do frontend, utilize o seguinte bloco de código no seu ficheiro global de estilos (`global.css` ou `variables.css`):

```css
:root {
  /* Cores de Fundo e Superfície */
  --color-bg-main: #F8F9FA;


  /* Cores de Tipografia */
  --color-text-primary: #414141;

  /* Cores de Identidade e Branding */
  --color-brand-dark: #24285A;
  
  /* Cores de Destaque e Interação */
  --color-accent-action: #00C5EE;
  --color-accent-warning: #FFD04D;
}