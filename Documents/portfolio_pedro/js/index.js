// ----------------------------------------------------
// 1. Lógica do Slideshow (Seção Sobre)
// ----------------------------------------------------
const iniciarSlideshow = () => {
    // Array com os nomes (futuros) das suas fotos
    const fotos = ['foto1.jpg', 'foto2.jpg', 'foto3.jpg'];
    let indexAtual = 0;

    console.log("Slideshow inicializado. Aguardando arquivos...");

    // A lógica do fade-in e fade-out entrará aqui
    // setInterval(() => {
    //    Trocar a classe CSS e a imagem
    // }, 4000);
};

// ----------------------------------------------------
// 2. Mock de Dados dos Arranjos (Seção Arranjos)
// ----------------------------------------------------
// Aqui criamos um "banco de dados" falso (mock) para testar o visual
const arranjosData = [
    {
        id: 1,
        titulo: "Désolée",
        descricao: `Written by Pedro Secco in October 2022.
        In this chart, the song was arranged for string quintet plus piccolo and oboe.
        Live recorded at Berklee Studio 3 by an ensemble of professional musicians hired by
        the school.`,
        thumb: "../assets/thumb/Desolee_FullScore/1",
        pdf: "../assets/score/Desolee_FullScore.pdf",
        audio: "../assets/audio/Desolee_Master" 
    },
    {
        id: 2,
        titulo: "Noturno Boreal",
        descricao: "Arranjo intimista para piano e violoncelo, focado na expressividade.",
        thumb: "https://dummyimage.com/300x400/f3eed9/570202.png&text=Partitura+2",
        audio: "#"
    }
];

const renderizarArranjos = () => {
    const container = document.getElementById('container-arranjos');
    
    // Trava de segurança: se a div não existir na página, o código para aqui
    if (!container) return; 

    // Limpa o contêiner por precaução
    container.innerHTML = '';

    // Percorre cada item da nossa lista de dados
    arranjosData.forEach(arranjo => {
        // Cria o HTML do card usando as variáveis do nosso array
        const cardHTML = `
            <article class="item-arranjo">
                <div class="imagem-partitura">
                    <img src="${arranjo.thumb}" alt="Partitura de ${arranjo.titulo}">
                </div>
                <div class="info-arranjo">
                    <h3 class="titulo-arranjo">${arranjo.titulo}</h3>
                    <p>${arranjo.descricao}</p>
                    
                    <audio controls class="player-audio">
                        <source src="${arranjo.audio}" type="audio/mpeg">
                        Seu navegador não suporta o elemento de áudio.
                    </audio>
                </div>
            </article>
        `;

        // Injeta o bloco gerado dentro do contêiner
        container.insertAdjacentHTML('beforeend', cardHTML);
    });
};

document.addEventListener("DOMContentLoaded", () => {
    iniciarSlideshow();
    renderizarArranjos();
});