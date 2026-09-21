let responseChart = null;
let monitoringTimer = null;

function setResult(id, data) {
    const el = document.getElementById(id);
    const ok = data.status === "success";
    const status = data.status || "failed";
    const error = data.error || "No response received";
    const time = data.response_time_ms != null ? `${data.response_time_ms} ms` : "—";
    el.innerHTML = `<span class="status ${ok ? "ok" : "bad"}">${status.toUpperCase()}</span><br><span>${escapeHtml(data.error || data.banner || data.welcome_message || data.ip_address || "Response received")}</span><br><span class="muted">Response: ${time}</span>`;
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[ch]));
}

async function api(path) {
    const response = await fetch(path);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed");
    return data;
}

async function checkBackend() {
    try {
        const data = await api("/api/health");
        const badge = document.getElementById("statusBadge");
        badge.textContent = data.message;
        badge.className = "badge ok-bg";
    } catch {
        const badge = document.getElementById("statusBadge");
        badge.textContent = "Backend unavailable";
        badge.className = "badge bad-bg";
    }
}

async function checkDNS() {
    const host = document.getElementById("dnsHost").value.trim();
    if (!host) return alert("Enter a hostname.");
    try { setResult("dnsResult", await api(`/api/dns?hostname=${encodeURIComponent(host)}`)); await loadDashboard(); }
    catch (e) { setResult("dnsResult", {status:"failed", error:e.message}); }
}

async function checkTCP() {
    const host = document.getElementById("tcpHost").value.trim();
    const port = document.getElementById("tcpPort").value;
    if (!host || !port) return alert("Enter host and port.");
    try { setResult("tcpResult", await api(`/api/tcp?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}`)); await loadDashboard(); }
    catch (e) { setResult("tcpResult", {status:"failed", error:e.message}); }
}

async function checkUDP() {
    const host = document.getElementById("udpHost").value.trim();
    const port = document.getElementById("udpPort").value;
    if (!host || !port) return alert("Enter host and port.");
    try { setResult("udpResult", await api(`/api/udp?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}`)); await loadDashboard(); }
    catch (e) { setResult("udpResult", {status:"failed", error:e.message}); }
}

async function checkQoS() {
    const host = document.getElementById("qosHost").value.trim();
    const port = document.getElementById("qosPort").value;
    const count = document.getElementById("qosCount").value || 5;
    if (!host || !port) return alert("Enter host and port.");
    try {
        const data = await api(`/api/qos?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}&count=${count}`);
        document.getElementById("qosResult").innerHTML = `<span class="status ${data.status === "success" ? "ok" : "bad"}">${data.status.toUpperCase()}</span><br>Average: ${data.average_latency_ms ?? "—"} ms<br>Min: ${data.minimum_latency_ms ?? "—"} ms<br>Max: ${data.maximum_latency_ms ?? "—"} ms<br>Probe failure: ${data.packet_loss_percent}%`;
        await loadDashboard();
    } catch (e) { setResult("qosResult", {status:"failed", error:e.message}); }
}

async function checkHTTP() {
    const url = document.getElementById("httpUrl").value.trim();
    if (!url) return alert("Enter a URL.");
    try { setResult("httpResult", await api(`/api/http?url=${encodeURIComponent(url)}`)); await loadDashboard(); }
    catch (e) { setResult("httpResult", {status:"failed", error:e.message}); }
}

async function checkSMTP() {
    const host = document.getElementById("smtpHost").value.trim();
    const port = document.getElementById("smtpPort").value || 587;
    if (!host) return alert("Enter an SMTP host.");
    try { setResult("smtpResult", await api(`/api/smtp?host=${encodeURIComponent(host)}&port=${port}`)); await loadDashboard(); }
    catch (e) { setResult("smtpResult", {status:"failed", error:e.message}); }
}

async function checkFTP() {
    const host = document.getElementById("ftpHost").value.trim();
    const port = document.getElementById("ftpPort").value || 21;
    if (!host) return alert("Enter an FTP host.");
    try { setResult("ftpResult", await api(`/api/ftp?host=${encodeURIComponent(host)}&port=${port}`)); await loadDashboard(); }
    catch (e) { setResult("ftpResult", {status:"failed", error:e.message}); }
}

async function checkSNMP() {
    const host = document.getElementById("snmpHost").value.trim();
    const port = document.getElementById("snmpPort").value || 161;
    const community = document.getElementById("snmpCommunity").value;
    if (!host) return alert("Enter an SNMP device.");
    try { setResult("snmpResult", await api(`/api/snmp?host=${encodeURIComponent(host)}&port=${port}&community=${encodeURIComponent(community)}`)); await loadDashboard(); }
    catch (e) { setResult("snmpResult", {status:"failed", error:e.message}); }
}

async function loadSummary() {
    const data = await api("/api/summary");
    document.getElementById("totalTests").textContent = data.total;
    document.getElementById("successfulTests").textContent = data.successful;
    document.getElementById("failedTests").textContent = data.failed;
    document.getElementById("availability").textContent = `${data.availability_percent}%`;
    document.getElementById("averageResponse").textContent = `${data.average_response_time_ms} ms`;
}

async function loadHistory() {
    const data = await api("/api/history");
    const body = document.getElementById("historyBody");
    body.textContent = "";
    const labels = [], values = [];
    data.results.forEach(item => {
        const row = document.createElement("tr");
        [item.created_at, item.monitor_type, item.target, item.port ?? "—", item.status, item.response_time_ms ?? "—", item.details || "—"].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });
        body.appendChild(row);
        if (item.response_time_ms != null) {
            labels.push(`${item.monitor_type} #${item.id}`);
            values.push(item.response_time_ms);
        }
    });
    drawResponseChart(labels.reverse(), values.reverse());
}

function drawResponseChart(labels, values) {
    const ctx = document.getElementById("responseChart");
    if (responseChart) responseChart.destroy();
    responseChart = new Chart(ctx, {
        type: "line",
        data: { labels, datasets: [{ label: "Response Time (ms)", data: values, tension: 0.25 }] },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

async function loadDashboard() {
    try { await loadSummary(); await loadHistory(); }
    catch (error) { console.error(error); }
}

async function runAutomaticTest() {
    const host = document.getElementById("autoHost").value.trim();
    const port = document.getElementById("autoPort").value;
    if (!host || !port) return;
    try { await api(`/api/tcp?host=${encodeURIComponent(host)}&port=${encodeURIComponent(port)}`); await loadDashboard(); }
    catch (error) { console.error(error); }
}

function startMonitoring() {
    const host = document.getElementById("autoHost").value.trim();
    const port = document.getElementById("autoPort").value;
    const interval = Number(document.getElementById("autoInterval").value);
    if (!host || !port) return alert("Enter host and port.");
    if (!interval || interval < 10) return alert("Interval must be at least 10 seconds.");
    stopMonitoring();
    runAutomaticTest();
    monitoringTimer = setInterval(runAutomaticTest, interval * 1000);
    document.getElementById("monitorStatus").textContent = `Running: ${host}:${port} every ${interval}s`;
}

function stopMonitoring() {
    if (monitoringTimer !== null) clearInterval(monitoringTimer);
    monitoringTimer = null;
    const status = document.getElementById("monitorStatus");
    if (status) status.textContent = "Stopped";
}

window.addEventListener("DOMContentLoaded", async () => {
    await checkBackend();
    await loadDashboard();
});
