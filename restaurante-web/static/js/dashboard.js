document.addEventListener("DOMContentLoaded", () => {
    loadSummary();
    loadTopProducts();
    loadOrderStatus();
    loadUsersTable();
});

async function loadSummary() {
    try {
        const response = await fetch('/api/stats/summary');
        const data = await response.json();
        document.getElementById('lbl-total-sales').innerText = `$${data.total_sales.toLocaleString('es-MX', {minimumFractionDigits: 2})}`;
        document.getElementById('lbl-active-orders').innerText = data.active_orders;
    } catch (e) { console.error(e); }
}

async function loadTopProducts() {
    try {
        const response = await fetch('/api/stats/top-products');
        const data = await response.json();
        const ctx = document.getElementById('chart-products').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                datasets: [{ 
                    label: 'Gastos Diarios ($)', 
                    data: [480, 520, 510, 650, 600, 780, 610], 
                    borderColor: '#e63946',
                    backgroundColor: 'rgba(230, 57, 70, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            }
        });
    } catch (e) { console.error(e); }
}

async function loadOrderStatus() {
    try {
        const response = await fetch('/api/stats/order-status');
        const data = await response.json();
        const ctx = document.getElementById('chart-status').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                datasets: [{ 
                    label: 'Ganancias Diarias ($)', 
                    data: [860, 1040, 920, 1180, 1140, 1390, 1070], 
                    borderColor: '#2a9d8f',
                    backgroundColor: 'rgba(42, 157, 143, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            }
        });
    } catch (e) { console.error(e); }
}

async function loadUsersTable() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        const tbody = document.getElementById('table-users-body');
        tbody.innerHTML = "";
        
        const defaultEmails = {
            "Admin": "juan@cafeteria.com",
            "Mesero": "ana@cafeteria.com",
            "Chef": "carlos@cafeteria.com",
            "Cajero": "maria@cafeteria.com"
        };

        users.forEach(user => {
            const email = default_email_or_user(user.role, user.username);
            const statusText = user.id % 4 === 0 ? "INACTIVO" : "ACTIVO";
            const statusClass = statusText.toLowerCase();

            const row = `<tr>
                <td><strong>${user.username}</strong></td>
                <td>${email}</td>
                <td><span class="badge-role">${user.role}</span></td>
                <td><span class="badge-status status-${statusClass}">${statusText}</span></td>
                <td><button style="background:none; border:none; color:#e63946; cursor:pointer; font-weight:bold;">Eliminar</button></td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (e) { console.error(e); }
}

function default_email_or_user(role, username) {
    if (username.includes("@")) return username;
    return `${username.toLowerCase()}@cafeteria.com`;
}

function switchTab(tabId, buttonElement) {
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
    buttonElement.classList.add('active');
}
document.getElementById('form-add-user').addEventListener('submit', addUser);

function openModal() {
    document.getElementById('modal-user').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal-user').style.display = 'none';
    document.getElementById('form-add-user').reset();
}

async function addUser(event) {
    event.preventDefault();
    const username = document.getElementById('txt-username').value;
    const role = document.getElementById('sel-role').value;
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, role })
        });
        if(response.ok) {
            alert("Usuario registrado exitosamente");
            closeModal();
            loadUsersTable();
            loadSummary();
        }
    } catch (e) { console.error(e); }
}

window.onclick = function(event) {
    const modal = document.getElementById('modal-user');
    if (event.target == modal) {
        closeModal();
    }
}