const API_BASE = "http://127.0.0.1:8000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
    loadPage("dashboard");

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
            link.classList.add("active");
            loadPage(link.getAttribute("data-page"));
        });
    });

    document.getElementById("tenderForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            tender_number: document.getElementById("tenderNumber").value,
            title: document.getElementById("tenderTitle").value,
            institution: document.getElementById("tenderInstitution").value,
            items: []
        };

        const res = await fetch(`${API_BASE}/tenders`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            closeModal();
            loadPage("tenders");
        }
    });
});

async function loadPage(page) {
    const content = document.getElementById("content-area");
    const title = document.getElementById("page-title");

    if (page === "dashboard") {
        title.innerText = "Genel Bakış - 4M1N Bilişim";
        const stats = await fetch(`${API_BASE}/dashboard/stats`).then(r => r.json()).catch(() => ({}));
        content.innerHTML = `
            <div class="stats-grid">
                <div class="card"><div class="card-title">Toplam İhale</div><div class="card-value">${stats.total_tenders || 0}</div></div>
                <div class="card"><div class="card-title">Analiz Edilen Kalem</div><div class="card-value">${stats.analyzed_items || 0}</div></div>
                <div class="card"><div class="card-title">Bağlı Tedarikçi</div><div class="card-value">${stats.total_suppliers || 0}</div></div>
            </div>
            <div class="card">
                <h3>4M1N İhale Analiz Motoru Aktif</h3>
                <p style="margin-top:10px; color:var(--text-muted);">Sistem arka planda tam doğrulama ve sıfır-uydurma (zero-hallucination) mantığı ile çalışmaktadır.</p>
            </div>
        `;
    } else if (page === "tenders") {
        title.innerText = "İhaleler & Şartnameler";
        const tenders = await fetch(`${API_BASE}/tenders`).then(r => r.json()).catch(() => []);
        let rows = tenders.map(t => `
            <tr>
                <td><strong>${t.tender_number}</strong></td>
                <td>${t.title}</td>
                <td>${t.institution}</td>
                <td>${t.item_count} Kalem</td>
                <td><span class="badge badge-pass">${t.status}</span></td>
            </tr>
        `).join('');

        content.innerHTML = `
            <div class="table-container">
                <table class="data-table">
                    <thead><tr><th>İhale No</th><th>İhale Adı</th><th>Kurum</th><th>Kalem</th><th>Durum</th></tr></thead>
                    <tbody>${rows || '<tr><td colspan="5" style="text-align:center;">Henüz kaydedilmiş ihale bulunmuyor.</td></tr>'}</tbody>
                </table>
            </div>
        `;
    } else if (page === "suppliers") {
        title.innerText = "B2B Tedarikçi Durumları";
        const suppliers = await fetch(`${API_BASE}/suppliers`).then(r => r.json()).catch(() => []);
        let rows = suppliers.map(s => `
            <tr>
                <td><strong>${s.name}</strong></td>
                <td><a href="${s.base_url}" target="_blank">${s.base_url}</a></td>
                <td><span class="badge badge-unknown">${s.connection_status}</span></td>
                <td>${s.last_check}</td>
            </tr>
        `).join('');

        content.innerHTML = `
            <div class="table-container">
                <table class="data-table">
                    <thead><tr><th>Tedarikçi</th><th>URL</th><th>Bağlantı</th><th>Son Kontrol</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            </div>
        `;
    } else if (page === "audit") {
        title.innerText = "Audit Log (Denetim Kayıtları)";
        const logs = await fetch(`${API_BASE}/audit-logs`).then(r => r.json()).catch(() => []);
        let rows = logs.map(l => `
            <tr>
                <td>${l.timestamp}</td>
                <td><strong>${l.user}</strong></td>
                <td>${l.action}</td>
                <td>${l.details}</td>
            </tr>
        `).join('');

        content.innerHTML = `
            <div class="table-container">
                <table class="data-table">
                    <thead><tr><th>Tarih</th><th>Kullanıcı</th><th>İşlem</th><th>Detay</th></tr></thead>
                    <tbody>${rows || '<tr><td colspan="4">Henüz kayıt yok.</td></tr>'}</tbody>
                </table>
            </div>
        `;
    }
}

function openModal() { document.getElementById("tenderModal").style.display = "flex"; }
function closeModal() { document.getElementById("tenderModal").style.display = "none"; }