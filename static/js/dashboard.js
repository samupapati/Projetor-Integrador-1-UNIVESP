let produtos = [];
        let ordemAtual = {
            coluna: 'codigo', // Coluna inicial de ordenação
            direcao: 'asc'    // Ordem crescente
        };

        // Função para carregar todos os produtos na tabela
        function carregarProdutos() {
            fetch("http://localhost:5000/produtos")
                .then(response => response.json())
                .then(data => {
                    produtos = data; // Armazenar os produtos
                    ordenarProdutos(); // Ordenar os produtos inicialmente
                })
                .catch(error => console.error("Erro ao carregar produtos:", error));
        }

        // Função para ordenar os produtos
        function ordenarProdutos() {
            produtos.sort((a, b) => {
                let valorA, valorB;
                switch (ordemAtual.coluna) {
                    case 'codigo':
                        valorA = a[0]; // código do produto
                        valorB = b[0];
                        break;
                    case 'nome':
                        valorA = a[1].toLowerCase(); // nome do produto
                        valorB = b[1].toLowerCase();
                        break;
                    case 'quantidade':
                        valorA = a[2]; // quantidade
                        valorB = b[2];
                        break;
                }

                if (ordemAtual.direcao === 'asc') {
                    return valorA > valorB ? 1 : valorA < valorB ? -1 : 0;
                } else {
                    return valorA < valorB ? 1 : valorA > valorB ? -1 : 0;
                }
            });
            exibirProdutos(); // Atualiza a exibição após a ordenação
        }

        // Função para exibir os produtos na tabela
        function exibirProdutos() {
            const tbody = document.getElementById("produtoTabela").getElementsByTagName('tbody')[0];
            tbody.innerHTML = ""; // Limpa a tabela antes de repopular

            produtos.forEach(produto => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${produto[0]}</td>   <!-- código do produto -->
                    <td>${produto[1]}</td>   <!-- nome do produto -->
                    <td>${produto[2]}</td>   <!-- quantidade -->
                    <td>
                        <button class="btn btn-warning" onclick="editarProduto(${produto[0]})">Editar</button>
                        <button class="btn btn-danger" onclick="excluirProduto(${produto[0]})">Excluir</button>
                    </td>
                `;
            });
        }

        // Função para ordenar a tabela
        function ordenarTabela(coluna) {
            if (ordemAtual.coluna === coluna) {
                // Se a coluna clicada já está ordenada, inverte a direção
                ordemAtual.direcao = ordemAtual.direcao === 'asc' ? 'desc' : 'asc';
            } else {
                // Se a coluna clicada é diferente, ordena de forma crescente
                ordemAtual.coluna = coluna;
                ordemAtual.direcao = 'asc';
            }

            ordenarProdutos(); // Ordena os produtos e exibe
        }

        // Função para adicionar um produto
        document.getElementById("adicionarProdutoForm").addEventListener("submit", function(event) {
            event.preventDefault();
        
            const nome = document.getElementById("nomeProduto").value.trim();
            const qtd = document.getElementById("qtdProduto").value.trim();
        
            if (nome === "" || qtd === "") {
                alert("Preencha todos os campos!");
                return;
            }
        
            fetch("http://localhost:5000/produtos", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nome: nome, qtd: qtd })
            })
            .then(response => response.text())
            .then(data => {
                if (data === "Operação completa") {
                    carregarProdutos(); // Atualiza a tabela
                    
                    // Fecha o modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modalAdicionar'));
                    modal.hide();
        
                    // Limpa os campos do formulário
                    document.getElementById("adicionarProdutoForm").reset();
                } else {
                    document.getElementById("error").textContent = data;
                }
            })
            .catch(error => {
                console.error("Erro ao adicionar produto:", error);
            });
        });

        // Função para editar um produto
        function editarProduto(cod) {
            const nome = prompt("Novo nome do produto:");
            const qtd = prompt("Nova quantidade:");

            if (nome && qtd) {
                fetch(`http://localhost:5000/produtos/${cod}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ nome: nome, qtd: qtd })
                })
                .then(response => response.text())
                .then(data => {
                    if (data === "Operação completa") {
                        carregarProdutos();  // Recarrega a tabela com as alterações
                    } else {
                        document.getElementById("error").textContent = data;
                    }
                })
                .catch(error => console.error("Erro ao editar produto:", error));
            }
        }

        // Função para excluir um produto
        function excluirProduto(cod) {
            if (confirm("Tem certeza que deseja excluir este produto?")) {
                fetch(`http://localhost:5000/produtos/${cod}`, {
                    method: "DELETE"
                })
                .then(response => response.text())
                .then(data => {
                    if (data === "Operação completa") {
                        carregarProdutos();  // Recarrega a tabela com os produtos restantes
                    } else {
                        document.getElementById("error").textContent = data;
                    }
                })
                .catch(error => console.error("Erro ao excluir produto:", error));
            }
        }

        // Função para exibir o formulário de adicionar produto
        function mostrarFormulario() {
            document.getElementById("addProductForm").style.display = "block"; // Exibe o formulário
        }

        // Carrega os produtos quando a página for carregada
        window.onload = carregarProdutos;

        document.getElementById("logoutBtn").addEventListener("click", function() {
            window.location.href = "/";
        });