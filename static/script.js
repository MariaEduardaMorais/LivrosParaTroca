document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("#livroForm");
    const livrosTable = document.querySelector("#livrosTable");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const livro = {
            titulo: form.titulo.value,
            autor: form.autor.value,
            edicao: form.edicao.value,
            estado: form.estado.value
        };

        try {
            const response = await fetch("http://127.0.0.1:5000/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(livro)
            });

            if (!response.ok) throw new Error("Erro ao adicionar livro");

            const data = await response.json();
            adicionarLivroNaTabela(data);
            form.reset();
        } catch (error) {
            console.error("Erro ao adicionar livro:", error);
            alert("Erro ao adicionar livro.");
        }
    });

    function adicionarLivroNaTabela(livro) {
        const row = document.createElement("tr");
        row.dataset.id = livro.id;
        row.innerHTML = `
            <td><strong>${livro.titulo}</strong></td>
            <td>${livro.autor}</td>
            <td>${livro.edicao}</td>
            <td>${livro.estado}</td>
            <td>
                <a href="/livro/${livro.id}" class="view-btn">🔍 Ver detalhes</a>
                <button class="edit-btn" data-id="${livro.id}">✏️ Editar</button>
                <button class="delete-btn" data-id="${livro.id}">🗑 Excluir</button>
            </td>
        `;
        
        livrosTable.appendChild(row);

        row.querySelector(".delete-btn").addEventListener("click", function () {
            excluirLivro(livro.id, row);
        });

        row.querySelector(".edit-btn").addEventListener("click", function () {
            editarLivro(livro.id, row);
        });
    }

    async function excluirLivro(livroId, elemento) {
        if (!confirm("Tem certeza que deseja excluir este livro?")) return;

        try {
            const response = await fetch(`http://127.0.0.1:5000/delete/${livroId}`, { method: "DELETE" });
            if (!response.ok) throw new Error("Erro ao excluir livro");

            elemento.remove();
        } catch (error) {
            console.error("Erro ao excluir livro:", error);
            alert("Erro ao excluir livro.");
        }
    }

    function editarLivro(livroId, elemento) {
        const cells = elemento.querySelectorAll("td");
        const titulo = cells[0].innerText;
        const autor = cells[1].innerText;
        const edicao = cells[2].innerText;
        const estado = cells[3].innerText;

        const novoTitulo = prompt("Novo título:", titulo);
        const novoAutor = prompt("Novo autor:", autor);
        const novaEdicao = prompt("Nova edição:", edicao);
        const novoEstado = prompt("Novo estado:", estado);

        if (!novoTitulo || !novoAutor || !novaEdicao || !novoEstado) return;

        const livroAtualizado = {
            titulo: novoTitulo,
            autor: novoAutor,
            edicao: novaEdicao,
            estado: novoEstado
        };

        fetch(`http://127.0.0.1:5000/update/${livroId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(livroAtualizado)
        })
        .then(response => {
            if (!response.ok) throw new Error("Erro ao atualizar livro");
            return response.json();
        })
        .then(data => {
            cells[0].innerText = data.titulo;
            cells[1].innerText = data.autor;
            cells[2].innerText = data.edicao;
            cells[3].innerText = data.estado;
        })
        .catch(error => {
            console.error("Erro ao editar livro:", error);
            alert("Erro ao editar livro.");
        });
    }

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            excluirLivro(this.dataset.id, row);
        });
    });

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            editarLivro(this.dataset.id, row);
        });
    });
});