export const metadata = {
  title: 'AI Trading Platform MVP',
  description: 'Paper-Trading Dashboard mit KI-Signalen und Backtesting.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
