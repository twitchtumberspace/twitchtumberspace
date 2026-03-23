const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function getDashboard() {
  try {
    const response = await fetch(`${API_URL}/dashboard`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('dashboard fetch failed');
    }
    return await response.json();
  } catch {
    return {
      assets: [],
      signals: [],
      trades: [],
      backtests: [],
      insights: {
        paper_trading_only: true,
        live_trading_enabled: false,
        explainability: 'Backend nicht erreichbar – Mock-Fallback aktiv.',
      },
    };
  }
}
