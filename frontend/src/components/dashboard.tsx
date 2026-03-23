type DashboardProps = {
  data: {
    assets: Array<{ id: number; symbol: string; name: string; asset_type: string }>;
    signals: Array<{ id: number; side: string; confidence: number; probability_up: number; rationale: any }>;
    trades: Array<{ id: number; side: string; quantity: number; entry_price: number; status: string }>;
    backtests: Array<{ id: number; name: string; metrics: Record<string, number> }>;
    insights: Record<string, string | boolean>;
  };
};

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section style={{ background: '#111827', borderRadius: 16, padding: 20, color: '#f9fafb', boxShadow: '0 10px 30px rgba(0,0,0,.2)' }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {children}
    </section>
  );
}

export function Dashboard({ data }: DashboardProps) {
  return (
    <main style={{ fontFamily: 'Arial, sans-serif', background: '#030712', minHeight: '100vh', padding: 24, color: '#e5e7eb' }}>
      <header style={{ marginBottom: 24 }}>
        <h1>AI Trading Platform MVP</h1>
        <p>Paper Trading, Explainable AI, Backtesting und modulare Datenpipelines.</p>
      </header>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0,1fr))', gap: 16, marginBottom: 24 }}>
        <Card title="Assets"><strong>{data.assets.length}</strong><p>Überwachte Märkte</p></Card>
        <Card title="Signale"><strong>{data.signals.length}</strong><p>Aktuelle KI-Signale</p></Card>
        <Card title="Trades"><strong>{data.trades.length}</strong><p>Paper-Positionen</p></Card>
        <Card title="Betriebsmodus"><strong>{String(data.insights.paper_trading_only)}</strong><p>Live-Trading standardmäßig aus</p></Card>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
        <Card title="KI-Signale & Erklärung">
          {data.signals.map((signal) => (
            <div key={signal.id} style={{ borderTop: '1px solid #374151', padding: '12px 0' }}>
              <strong>{signal.side.toUpperCase()}</strong> – Confidence {signal.confidence}
              <div>Wahrscheinlichkeit Up: {signal.probability_up}</div>
              <pre style={{ whiteSpace: 'pre-wrap', fontSize: 12 }}>{JSON.stringify(signal.rationale, null, 2)}</pre>
            </div>
          ))}
        </Card>
        <Card title="Backtesting">
          {data.backtests.map((test) => (
            <div key={test.id} style={{ marginBottom: 12 }}>
              <strong>{test.name}</strong>
              <pre style={{ whiteSpace: 'pre-wrap', fontSize: 12 }}>{JSON.stringify(test.metrics, null, 2)}</pre>
            </div>
          ))}
        </Card>
      </div>
    </main>
  );
}
