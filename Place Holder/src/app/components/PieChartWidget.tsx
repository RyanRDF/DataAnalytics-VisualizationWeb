import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

const data = [
  { name: "Financial Data", value: 400 },
  { name: "Patient Data", value: 300 },
  { name: "Site Analysis", value: 300 },
  { name: "File Upload", value: 200 },
];

const COLORS = ["#2563eb", "#10b981", "#f59e0b", "#ef4444"];

export function PieChartWidget() {
  return (
    <div className="h-full">
      <h3 className="mb-4">Data Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
