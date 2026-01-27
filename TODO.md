# Jogo 2D:
Menu inicial usando rasterização de reta, circunferência e elipse, e as figuras desse menu devem usar flood fill ou boundary fill pra preenchimento;
Jogo baseado em polígonos preenchidos com scanline e polígonos preenchidos com gradientes de cores (definidas por vértice?) e texturas de imagens;
deve usar translação, escala e rotação, e pelo menos uma animação;
deve ter minimapa de zoom (viewport usando zoom), e tem que ter corte de Cohen-Sutherland (clipping)
Terá input de mouse e menu de pausa;
Nada de usar funções prontas exceto as que fazem o set pixel, que exibem matrizes numéricas como imagens ou que carreguem imagens para as matrizes (recomenda-se PyGame, SDL2 e Canvas (html5));


### Feito:
- Reta no jogo, circunferência no jogo, elipse no jogo  (reta usando bresenham, e scanline pra pintar)
- Input mouse
- Primitivas
- rotação (bola rodando)

### Falta:
- escala
- personagem
- boneco pulando (animação)
- Viewport com zoom (minimapa focando a cara do personagem, usando clipping)
- cenário (provavelmente um png do ceu azul e um chão)
- viewport com minimap (usando clipping)
- Menu inicial
- Função scanline (falta adicionar no menu e no título)
- clipping (is_out_of_bound, mas tem que melhorar pra usar as funções do professor)
- Translação (precisa melhorar como está apresentado/implementado)