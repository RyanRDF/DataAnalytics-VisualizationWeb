import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const data = [
  { name: "Jan", uploads: 40, analysis: 24 },
  { name: "Feb", uploads: 30, analysis: 13 },
  { name: "Mar", uploads: 20, analysis: 28 },
  { name: "Apr", uploads: 27, analysis: 39 },
  { name: "May", uploads: 18, analysis: 48 },
  { name: "Jun", uploads: 23, analysis: 38 },
];

export function BarChartWidget() {
  return (
    <div className="h-full">
      <h3 className="mb-4">Monthly Activity</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="uploads" fill="#2563eb" />
          <Bar dataKey="analysis" fill="#10b981" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
