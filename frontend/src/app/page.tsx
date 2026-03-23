import { Dashboard } from '../components/dashboard';
import { getDashboard } from '../lib/api';

export default async function HomePage() {
  const data = await getDashboard();
  return <Dashboard data={data} />;
}
