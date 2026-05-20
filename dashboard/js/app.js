/**
 * PetCompare - Interações do Frontend
 * Simula a busca na API e a injeção dos resultados na tela
 */

document.addEventListener("DOMContentLoaded", () => {
    
    const btnSearch = document.getElementById("btnSearch");
    const cityInput = document.getElementById("citySearch");
    const serviceSelect = document.getElementById("serviceType");
    const resultsGrid = document.getElementById("resultsGrid");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const sortFilter = document.getElementById("sortFilter");

    // Dados Mockados Simulando o Retorno dos Robôs (API)
    const mockData = [
        {
            id: 1,
            name: "Cantinho do Totó",
            type: "hotel",
            address: "Vila Mariana",
            rating: 4.9,
            reviews: 128,
            price: 80.00,
            source: "DogHero",
            image: "https://images.unsplash.com/photo-1601758228041-f3b279ce7bec?auto=format&fit=crop&w=600&q=80"
        },
        {
            id: 2,
            name: "Cão Feliz Creche",
            type: "creche",
            address: "Pinheiros",
            rating: 4.7,
            reviews: 85,
            price: 65.00,
            source: "Google Maps",
            image: "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=600&q=80"
        },
        {
            id: 3,
            name: "Pet Resort Premium",
            type: "hotel",
            address: "Moema",
            rating: 5.0,
            reviews: 312,
            price: 150.00,
            source: "DogHero",
            image: "https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993?auto=format&fit=crop&w=600&q=80"
        },
        {
            id: 4,
            name: "Ana Pet Sitter",
            type: "pet_sitter",
            address: "Itaim Bibi",
            rating: 4.8,
            reviews: 42,
            price: 50.00,
            source: "GetNinjas",
            image: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=600&q=80"
        },
        {
            id: 5,
            name: "Lar Doce Cãozinho",
            type: "hotel",
            address: "Santana",
            rating: 4.5,
            reviews: 67,
            price: 55.00,
            source: "DogHero",
            image: "https://images.unsplash.com/photo-1537151608804-ea6f1cb53cb1?auto=format&fit=crop&w=600&q=80"
        },
        {
            id: 6,
            name: "Espaço AuAu",
            type: "creche",
            address: "Tatuapé",
            rating: 4.6,
            reviews: 90,
            price: 70.00,
            source: "Google Maps",
            image: "https://images.unsplash.com/photo-1591160690555-5debfba289f0?auto=format&fit=crop&w=600&q=80"
        }
    ];

    // Função para formatar moeda (Real Brasileiro)
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
    };

    // Função para criar o HTML de um Card
    const createCardHTML = (petService) => {
        return `
            <div class="pet-card">
                <div class="card-image-wrapper">
                    <span class="badge-source"><i class="fa-solid fa-robot"></i> via ${petService.source}</span>
                    <img src="${petService.image}" alt="${petService.name}">
                </div>
                <div class="card-content">
                    <div class="card-header">
                        <h3 class="card-title">${petService.name}</h3>
                        <div class="card-rating">
                            <i class="fa-solid fa-star"></i>
                            <span>${petService.rating}</span>
                        </div>
                    </div>
                    <div class="card-location">
                        <i class="fa-solid fa-map-pin"></i>
                        <span>${petService.address}</span>
                    </div>
                    
                    <div class="card-footer">
                        <div class="price-box">
                            <span class="price-label">Menor preço por noite</span>
                            <span class="price-value">${formatCurrency(petService.price)}</span>
                        </div>
                        <button class="btn-book">Ver Oferta</button>
                    </div>
                </div>
            </div>
        `;
    };

    // Função para renderizar os cards na tela
    const renderResults = (data) => {
        resultsGrid.innerHTML = "";
        
        if (data.length === 0) {
            resultsGrid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted); font-size: 1.2rem;">Nenhum serviço encontrado para esta região.</p>`;
            return;
        }

        data.forEach(service => {
            resultsGrid.innerHTML += createCardHTML(service);
        });
    };

    // Lógica do Botão de Busca
    btnSearch.addEventListener("click", () => {
        const city = cityInput.value.trim();
        const type = serviceSelect.value;
        
        if (!city) {
            alert("Por favor, digite a sua cidade para buscar!");
            cityInput.focus();
            return;
        }

        // Limpa grid e mostra Loading (Simulando API request/Robô rodando)
        resultsGrid.innerHTML = "";
        loadingIndicator.classList.remove("hidden");
        
        // Simula delay de rede e do bot (1.5 segundos)
        setTimeout(() => {
            loadingIndicator.classList.add("hidden");
            
            // Filtra os dados mockados baseados no tipo (na vida real isso viria do backend FastAPI)
            let filteredData = mockData;
            if(type !== "all") {
               filteredData = mockData.filter(d => d.type === type);
            }
            
            renderResults(filteredData);
            
            // Rola a tela suavemente para os resultados
            document.querySelector('.main-results').scrollIntoView({ behavior: 'smooth' });

        }, 1500);
    });

    // Filtro de Ordenação
    sortFilter.addEventListener("change", (e) => {
        const type = e.target.value;
        
        // Pegar os items atuais na tela seria o ideal, mas vamos ordenar os mockData no exemplo
        let sortedData = [...mockData];
        
        if (type === "lowest_price") {
            sortedData.sort((a, b) => a.price - b.price);
        } else if (type === "highest_rating") {
            sortedData.sort((a, b) => b.rating - a.rating);
        } // "recommended" mantem a ordem original
        
        // Aplica o filtro de tipo que estiver selecionado
        const currentType = serviceSelect.value;
        if(currentType !== "all") {
            sortedData = sortedData.filter(d => d.type === currentType);
        }
        
        renderResults(sortedData);
    });

    // Opcional: Aciona busca ao apertar Enter no input de cidade
    cityInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            btnSearch.click();
        }
    });
    
    // Inicia com alguns resultados padrão
    renderResults(mockData);
});
