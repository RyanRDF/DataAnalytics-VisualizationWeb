import { useState, useCallback } from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { DashboardHeader } from "./components/DashboardHeader";
import { DraggableChart } from "./components/DraggableChart";
import { PieChartWidget } from "./components/PieChartWidget";
import { BarChartWidget } from "./components/BarChartWidget";
import { LineChartWidget } from "./components/LineChartWidget";

interface ChartItem {
  id: string;
  component: React.ReactNode;
  span?: string;
}

export default function App() {
  const [charts, setCharts] = useState<ChartItem[]>([
    { id: "pie", component: <PieChartWidget />, span: "md:col-span-1" },
    { id: "bar", component: <BarChartWidget />, span: "md:col-span-1" },
    { id: "line", component: <LineChartWidget />, span: "md:col-span-2" },
  ]);

  const moveChart = useCallback((dragIndex: number, hoverIndex: number) => {
    setCharts((prevCharts) => {
      const newCharts = [...prevCharts];
      const [removed] = newCharts.splice(dragIndex, 1);
      newCharts.splice(hoverIndex, 0, removed);
      return newCharts;
    });
  }, []);

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <DashboardHeader />
          
          {/* Draggable Charts Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {charts.map((chart, index) => (
              <div key={chart.id} className={chart.span}>
                <DraggableChart
                  id={chart.id}
                  index={index}
                  moveChart={moveChart}
                >
                  {chart.component}
                </DraggableChart>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DndProvider>
  );
}