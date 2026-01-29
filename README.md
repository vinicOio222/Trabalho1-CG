# Basketball Arcade - Jogo 2D de Basquete

Um jogo arcade de basquete desenvolvido do zero usando algoritmos clássicos de Computação Gráfica, implementado em Python com Pygame.

# Menu 
![Basketball Arcade](/public/start_menu.png)
# In-game
![Basketball Arcade](/public/in-game.png)

## 📋 Descrição

Basketball Arcade é um jogo 2D onde o jogador arremessa uma bola de basquete em uma cesta usando mecânica de estilingue (slingshot). O objetivo é fazer o maior número de cestas possível sem perder as 5 vidas disponíveis. O jogo implementa física realista com gravidade, quique, atrito e rotação da bola.

### Características do Jogo

- **Mecânica de Arremesso**: Arraste e solte a bola para arremessar
- **Física Realista**: Gravidade, colisão com o chão, quique e atrito
- **Rotação da Bola**: A bola rotaciona durante o movimento
- **Sistema de Pontuação**: Ganhe pontos ao acertar a cesta
- **Sistema de Vidas**: 5 vidas, perde uma a cada erro
- **Minimap**: Visualização em tempo real da posição da bola e cesta com clipping
- **Menu Inicial**: Interface gráfica com título e botão de iniciar
- **Texturas**: Chão com textura de grama

## 🎮 Como Jogar

1. Execute o jogo: `python main.py`
2. Clique em "Start Game" no menu inicial
3. Clique e arraste a bola para definir a força e direção do arremesso
4. Solte para arremessar
5. Acerte a cesta para marcar pontos
6. Evite deixar a bola cair no chão por muito tempo (perde uma vida)

## 🛠️ Tecnologias e Ferramentas

- **Python 3.x**
- **Pygame**: Biblioteca para criação de jogos 2D
- **Algoritmos de Computação Gráfica**: Implementados do zero, sem usar funções prontas de desenho

## 🎨 Algoritmos de Computação Gráfica Implementados

Este projeto foi desenvolvido como trabalho de Computação Gráfica e implementa diversos algoritmos fundamentais **do zero**, sem uso de funções prontas de desenho:

### 1. Rasterização de Primitivas

#### Algoritmo de Bresenham para Linhas (`graphic/shapes.py`)
- Desenha linhas retas pixel a pixel de forma eficiente
- Usado para desenhar polígonos, bordas e a rede da cesta

#### Algoritmo do Ponto Médio para Círculos (`graphic/shapes.py`)
- Desenha círculos usando simetria de 8 octantes
- Usado para desenhar a bola de basquete

#### Algoritmo do Ponto Médio para Elipses (`graphic/shapes.py`)
- Desenha elipses dividindo em duas regiões
- Usado para desenhar o aro da cesta de basquete

#### Algoritmo de Arcos (`graphic/shapes.py`)
- Desenha arcos circulares com máscaras
- Usado para desenhar os detalhes da bola de basquete

### 2. Preenchimento de Polígonos

#### Scanline Fill (`graphic/scan_line.py`)
- Preenche polígonos usando o algoritmo de varredura por linhas
- Calcula interseções de cada linha horizontal com as arestas do polígono
- Usado para preencher o chão, cesta, bola e poste

#### Scanline com Clipping (`graphic/scan_line.py`)
- Versão do scanline que respeita janela de clipping
- Usado no minimap para não desenhar fora dos limites

#### Scanline com Gradiente (`graphic/scan_line.py`)
- Preenche polígonos com gradiente de cores
- Interpola cores entre vértices
- Usado para criar o céu com gradiente azul

#### Scanline com Textura (`graphic/scan_line.py`)
- Mapeia texturas em polígonos usando coordenadas UV
- Usado para aplicar textura de grama no chão

### 3. Algoritmo de Clipping de Cohen-Sutherland (`graphic/clipping.py`)

Implementa o algoritmo clássico de recorte de linhas:
- Divide o espaço em 9 regiões usando códigos binários
- Rejeita trivialmente linhas completamente fora
- Aceita trivialmente linhas completamente dentro
- Calcula interseções para linhas parcialmente visíveis
- **Aplicações no projeto**:
  - Clipping de linhas no minimap
  - Clipping de círculos (bola) no minimap
  - Clipping de elipses (cesta) no minimap
  - Clipping de polígonos (chão, poste) no minimap

### 4. Transformações Geométricas

#### Rotação (`game/ball.py`)
- Rotação de pontos ao redor do centro da bola
- Implementa matriz de rotação 2D
- Atualiza o ângulo da bola baseado na velocidade angular

#### Translação (`animation/animation.py`)
- Move objetos no espaço 2D
- Aplicado na movimentação da bola

#### Escala (`animation/animation.py`)
- Redimensiona objetos para o minimap
- Calcula fatores de escala entre mundo e viewport

### 5. Window-Viewport Transformation (`animation/animation.py`)

Implementa transformação entre sistemas de coordenadas:
- Converte coordenadas do mundo para a viewport do minimap
- Aplica translação e escala
- Usado para exibir versão reduzida do jogo no minimap

### 6. Física e Animação

#### Sistema de Física (`game/ball.py`)
- Gravidade constante
- Colisão com detecção e resposta
- Coeficiente de restituição (quique)
- Atrito para desaceleração
- Velocidade angular para rotação realista

## 📁 Estrutura do Projeto

```
Trabalho1-CG/
├── main.py                 # Arquivo principal do jogo
├── README.md              # Este arquivo
├── TODO.md                # Lista de tarefas do projeto
│
├── animation/             # Módulo de animações e transformações
│   └── animation.py       # Transformações geométricas e viewport
│
├── core/                  # Núcleo do jogo
│   └── screen.py         # Gerenciamento da tela e minimap
│
├── game/                  # Objetos do jogo
│   ├── ball.py           # Classe da bola com física e rotação
│   ├── ground.py         # Classe do chão com textura
│   ├── hoop.py           # Classe da cesta com poste
│   ├── score_board.py    # Sistema de pontuação
│   └── textures/         # Texturas do jogo
│       └── grass.jpg     # Textura de grama
│
├── graphic/               # Algoritmos gráficos
│   ├── clipping.py       # Cohen-Sutherland clipping
│   ├── floodfill.py      # Algoritmo de preenchimento
│   ├── scan_line.py      # Scanline fill e variações
│   └── shapes.py         # Primitivas (linhas, círculos, elipses)
│
└── menu/                  # Interface do menu
    └── start_screen.py   # Tela inicial do jogo
```

## 🔧 Requisitos do Trabalho Atendidos

- ✅ **Rasterização**: Linha (Bresenham), Círculo, Elipse
- ✅ **Preenchimento**: Scanline fill, Flood fill
- ✅ **Polígonos**: Preenchimento com scanline
- ✅ **Gradientes**: Céu com gradiente de cores
- ✅ **Texturas**: Chão com textura de grama
- ✅ **Transformações**: Translação, Rotação, Escala
- ✅ **Animação**: Bola rodando durante movimento
- ✅ **Minimap**: Viewport com zoom usando window-viewport
- ✅ **Clipping**: Cohen-Sutherland implementado
- ✅ **Input**: Mouse para arremessar
- ✅ **Menu**: Tela inicial com primitivas gráficas

## 🎯 Implementação Técnica

### Pixel por Pixel
Todas as primitivas gráficas foram implementadas manualmente, pixel a pixel, usando apenas:
- `surface.set_at((x, y), color)` - Para definir cor de um pixel
- `surface.get_at((x, y))` - Para ler cor de um pixel

### Sem Funções Prontas
O projeto **não utiliza** funções prontas como:
- `pygame.draw.line()`
- `pygame.draw.circle()`
- `pygame.draw.rect()`
- `pygame.draw.polygon()`

### Minimap com Clipping
O minimap implementa:
1. Window-to-Viewport transformation para escalar o mundo
2. Cohen-Sutherland para clipar todos os elementos:
   - Círculo da bola usando teste de região ponto a ponto
   - Elipses da cesta usando teste de região
   - Polígonos do chão e poste usando clipping de linhas
   - Scanline com clipping para preenchimento

## 📝 Documentação do Código

Todo o código está documentado com:
- Docstrings em funções explicando parâmetros e retorno
- Comentários explicando algoritmos complexos
- Nomes de variáveis descritivos

## 🎓 Autores e Licença

Projeto desenvolvido como trabalho da disciplina de Computação Gráfica.

## 🚀 Como Executar

1. Certifique-se de ter Python 3.x instalado
2. Instale as dependências:
   ```bash
   pip install pygame
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

## 🎮 Controles

- **Mouse**: Clique e arraste na bola para arremessar
- **ESC**: Sair do jogo (se implementado)

## 📊 Sistema de Pontuação

- Cada cesta vale 1 ponto
- O jogo começa com 5 vidas
- Perde uma vida quando a bola fica muito tempo no chão sem ser arremessada
- Game Over quando as vidas chegam a zero

---

**Nota**: Este projeto foi desenvolvido com fins educacionais para demonstrar a implementação de algoritmos fundamentais de Computação Gráfica.
