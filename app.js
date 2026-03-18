const API_BASE = "https://api.coingecko.com/api/v3";
const REFRESH_MS = 60000;

const themeToggle = document.getElementById("themeToggle");
const accountForm = document.getElementById("accountForm");
const accountMessage = document.getElementById("accountMessage");
const coinSelect = document.getElementById("coinSelect");
const converterForm = document.getElementById("converterForm");
const converterResult = document.getElementById("converterResult");
const trendingList = document.getElementById("trendingList");
const marketBody = document.getElementById("marketBody");
const lastUpdated = document.getElementById("lastUpdated");

let marketCoins = [];

function applySavedTheme() {
  const savedTheme = localStorage.getItem("theme") || "light";
  document.body.classList.toggle("dark", savedTheme === "dark");
  themeToggle.textContent = savedTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
}

function saveAccount(data) {
  localStorage.setItem("cryptoAccount", JSON.stringify(data));
}

function loadAccount() {
  const raw = localStorage.getItem("cryptoAccount");
  if (!raw) return;

  const account = JSON.parse(raw);
  accountMessage.textContent = `Eingeloggt als ${account.username} (${account.email})`;
}

function formatEUR(value) {
  return new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 8,
  }).format(value);
}

function setCoinOptions(coins) {
  coinSelect.innerHTML = coins
    .map(
      (coin) =>
        `<option value="${coin.id}">${coin.name} (${coin.symbol.toUpperCase()})</option>`
    )
    .join("");
}

function renderMarketTable(coins) {
  marketBody.innerHTML = coins
    .map((coin) => {
      const change = coin.price_change_percentage_24h ?? 0;
      const changeClass = change >= 0 ? "price-up" : "price-down";
      return `
        <tr>
          <td>${coin.market_cap_rank}</td>
          <td>${coin.name}</td>
          <td>${coin.symbol.toUpperCase()}</td>
          <td>${formatEUR(coin.current_price)}</td>
          <td class="${changeClass}">${change.toFixed(2)}%</td>
        </tr>
      `;
    })
    .join("");
}

async function fetchTopCoins() {
  const response = await fetch(
    `${API_BASE}/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=100&page=1&sparkline=false`
  );
  if (!response.ok) throw new Error("Top 100 Coins konnten nicht geladen werden.");

  marketCoins = await response.json();
  setCoinOptions(marketCoins);
  renderMarketTable(marketCoins);
  lastUpdated.textContent = `Letztes Update: ${new Date().toLocaleTimeString("de-DE")}`;
}

async function fetchTrendingCoins() {
  const response = await fetch(`${API_BASE}/search/trending`);
  if (!response.ok) throw new Error("Trending Coins konnten nicht geladen werden.");

  const data = await response.json();
  const top10 = data.coins.slice(0, 10);

  trendingList.innerHTML = top10
    .map(({ item }, index) => {
      return `<li><span>${index + 1}. ${item.name} (${item.symbol})</span><strong>Rank #${item.market_cap_rank || "-"}</strong></li>`;
    })
    .join("");
}

function handleConvert(event) {
  event.preventDefault();
  const coinId = coinSelect.value;
  const eurInput = document.getElementById("eurAmount").value;
  const eurAmount = Number(eurInput);

  if (!coinId || Number.isNaN(eurAmount) || eurAmount <= 0) {
    converterResult.textContent = "Bitte gültige Werte eingeben.";
    return;
  }

  const selectedCoin = marketCoins.find((coin) => coin.id === coinId);
  if (!selectedCoin) {
    converterResult.textContent = "Coin nicht gefunden. Bitte neu laden.";
    return;
  }

  const amount = eurAmount / selectedCoin.current_price;
  converterResult.textContent = `1 ${selectedCoin.symbol.toUpperCase()} kostet aktuell ${formatEUR(
    selectedCoin.current_price
  )}. Für ${formatEUR(eurAmount)} bekommst du ca. ${amount.toFixed(8)} ${selectedCoin.symbol.toUpperCase()}.`;
}

function bindEvents() {
  themeToggle.addEventListener("click", () => {
    const toDark = !document.body.classList.contains("dark");
    document.body.classList.toggle("dark", toDark);
    localStorage.setItem("theme", toDark ? "dark" : "light");
    applySavedTheme();
  });

  accountForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    saveAccount({ username, email, password });
    accountMessage.textContent = `Account gespeichert für ${username}.`;
    accountForm.reset();
  });

  converterForm.addEventListener("submit", handleConvert);
}

async function initialLoad() {
  try {
    await Promise.all([fetchTopCoins(), fetchTrendingCoins()]);
  } catch (error) {
    converterResult.textContent = error.message;
    lastUpdated.textContent = "Fehler beim Laden der Daten";
  }
}

function startAutoRefresh() {
  setInterval(async () => {
    try {
      await Promise.all([fetchTopCoins(), fetchTrendingCoins()]);
    } catch {
      lastUpdated.textContent = "Auto-Update fehlgeschlagen";
    }
  }, REFRESH_MS);
}

applySavedTheme();
loadAccount();
bindEvents();
initialLoad();
startAutoRefresh();
