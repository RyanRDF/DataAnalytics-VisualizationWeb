import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const data = [
  { name: "Week 1", financial: 4000, patient: 2400, site: 2400 },
  { name: "Week 2", financial: 3000, patient: 1398, site: 2210 },
  { name: "Week 3", financial: 2000, patient: 9800, site: 2290 },
  { name: "Week 4", financial: 2780, patient: 3908, site: 2000 },
  { name: "Week 5", financial: 1890, patient: 4800, site: 2181 },
  { name: "Week 6", financial: 2390, patient: 3800, site: 2500 },
  { name: "Week 7", financial: 3490, patient: 4300, site: 2100 },
];

export function LineChartWidget() {
  return (
    <div className="h-full">
      <h3 className="mb-4">Trend Analysis</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="financial" stroke="#2563eb" strokeWidth={2} />
          <Line type="monotone" dataKey="patient" stroke="#10b981" strokeWidth={2} />
          <Line type="monotone" dataKey="site" stroke="#f59e0b" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
